import nslog
import logging
import functools

from rubicon.objc import objc_method, ObjCClass
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

        # TODO
        # create a nib called "main" that represents the main view
        # it should contain a collection view tagged "collectionview"

        # NOTE if nib is not defined, this call will crash, see
        # https://stackoverflow.com/questions/22322528/find-out-if-xib-exists-at-runtime
        nib = NSBundle.mainBundle.loadNibNamed("main", owner=self, options=NSDictionary.new())
        assert nib
        root.view = nib.firstObject()
        assert root.view

        # "collectionview" is the resotrarion id of some element in the nib
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
    ...


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
        # content.retain()  # will be discussed later

        # "text" is the resotration id of some element in the nib
        label = find_view(content, "text")
        label.text = str(i)

        # fill this cell with whatever needs to be shown
        rv.addSubview(content)
        return rv
