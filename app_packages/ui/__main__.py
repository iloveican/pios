import nslog
import logging
import functools

from rubicon.objc import objc_method, ObjCClass, SEL
from rubicon.objc.types import CGSize, CGRect, CGPoint


if __name__.split(".")[-1] == "__main__":
    # I'm ran as a module
    # drop low-level logging handler
    # set up logging properly
    del logging.root.handlers[:]
    logging.basicConfig(level=logging.DEBUG, handlers=[nslog.handler()])


UIView = ObjCClass("UIView")
UILabel = ObjCClass("UILabel")
UIColor = ObjCClass("UIColor")
UIWindow = ObjCClass("UIWindow")
UIScreen = ObjCClass("UIScreen")
UIResponder = ObjCClass("UIResponder")
UIViewController = ObjCClass("UIViewController")
UICollectionViewCell = ObjCClass("UICollectionViewCell")
UITapGestureRecognizer = ObjCClass("UITapGestureRecognizer")
NSBundle = ObjCClass("NSBundle")
NSDictionary = ObjCClass("NSDictionary")

UIViewAnimationOptionTransitionFlipFromBottom = 7 << 20


def rect(x, y, w, h):
    """ A la CGRectMake """
    return CGRect(CGPoint(x, y), CGSize(w, h))


def all_views(v):
    yield v
    for vv in v.subviews():
        yield from all_views(vv)


def find_view(v, id="something"):
    for vv in all_views(v):
        if vv.restorationIdentifier == id:
            return vv


# If a callback fails, ObjC runtime will crash and debugger is not particularly useful
# it's a good idea to get a traceback logged before handing control over to ObjC
def logged(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            logging.exception("%s", f)
            raise
    return inner


class PythonAppDelegate(UIResponder):
    # def __init__(self): init is not ran, as this is instantiated by ObjC runtime

    @objc_method
    def applicationDidBecomeActive(self) -> None:
        logging.debug("became active")

    @objc_method
    @logged
    def application_didFinishLaunchingWithOptions_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("finished launching %s %s", application, oldStatusBarOrientation)

        root = UIViewController.new()

        win = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)
        win.rootViewController = root
        win.makeKeyAndVisible()

        nib = NSBundle.mainBundle.loadNibNamed("main", owner=self, options=NSDictionary.new())
        assert nib
        root.view = nib.firstObject()
        assert root.view

        coll = find_view(root.view, "collectionview")
        assert coll

        coll.registerClass(UICollectionViewCell, forCellWithReuseIdentifier="foobar")
        cant = CantRoller.new()
        coll.setDataSource(cant)

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("old orientation %s", oldStatusBarOrientation)


class state:
    """ Keeps controller state """
    opened = dict()
    closed = dict()
    current = {i: False for i in range(16)}


class CantRoller(UIViewController):
    """ Data source for collection view
        Implement following protocol:
        * UICollectionViewDataSource and output NxN array of cells
        * [opt] UICollectionViewDelegate and gets notified when cell is clicked
    """
    # def __init__(self): init is not ran, as this is instantiated via ObjC runtime

    @objc_method
    def collectionView_numberOfItemsInSection_(self, view, section: int) -> int:
        return 16

    @objc_method
    @logged
    def collectionView_cellForItemAtIndexPath_(self, view, path):
        i = path.item  # actual index
        rv = view.dequeueReusableCellWithReuseIdentifier("foobar", forIndexPath=path)

        # FIXME reset this cell (in case it was reused)
        content = NSBundle.mainBundle.loadNibNamed("knob", owner=self, options=NSDictionary.new()).firstObject()
        content.retain()  # so that ObjC runtime doesn't garbage-collect it, when/if it's not displayed
        state.closed[i] = content

        # "text" is the resotration id of some element in the nib
        label = find_view(content, "text")
        label.text = str(i)

        # TODO create another version of "knob", for example same size different look
        ...
        state.opened[i] = ...

        # fill this cell with whatever needs to be shown
        rv.addSubview(content)

        # NEW: register a callback when a knob is clicked
        rec = UITapGestureRecognizer.alloc().initWithTarget(self, action=SEL("tap:"))
        # TODO record somewhere which knob it was
        # state. ...
        rv.addGestureRecognizer(rec)
        return rv

    @objc_method
    @logged
    def tap_(self, rec):
        # TODO figure out which knob was clicked
        i = 0  # not the real value

        # transition from current view to new view
        new = state.closed[i] if state.current[i] else state.opened[i]
        logging.debug("new view %s", new)

        # transition type example: UIViewAnimationOptionTransitionFlipFromBottom

        # update state.current
        state.current[i] = not state.current[i]

        # play a sound
