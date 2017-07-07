import nslog
import logging
import functools

from rubicon.objc import objc_method, ObjCClass, SEL, send_message
from rubicon.objc.types import CGSize, CGRect, CGPoint, NSTimeInterval

import game
import sound


if __name__.split(".")[-1] == "__main__":
    # I'm ran as a module
    logging.root.addHandler(nslog.handler())
    logging.debug("yep, in main")

UIView = ObjCClass("UIView")
UILabel = ObjCClass("UILabel")
UIColor = ObjCClass("UIColor")
UIWindow = ObjCClass("UIWindow")
UIScreen = ObjCClass("UIScreen")
UIResponder = ObjCClass('UIResponder')
UIApplication = ObjCClass("UIApplication")
UIViewController = ObjCClass("UIViewController")
UICollectionView = ObjCClass("UICollectionView")
UICollectionViewCell = ObjCClass("UICollectionViewCell")
UINavigationController = ObjCClass("UINavigationController")
UITapGestureRecognizer = ObjCClass("UITapGestureRecognizer")
UICollectionViewFlowLayout = ObjCClass("UICollectionViewFlowLayout")
NSBundle = ObjCClass("NSBundle")
NSArray = ObjCClass("NSArray")
NSMutableArray = ObjCClass("NSMutableArray")
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


class PythonAppDelegate(UIResponder):
    # def __init__(self): init is not ran, as this is instantiated by ObjC runtime

    @objc_method
    def applicationDidBecomeActive(self) -> None:
        logging.debug("became active")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("finished launching %s %s", application, oldStatusBarOrientation)

        root = UIViewController.new()

        win = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)
        win.rootViewController = root
        win.makeKeyAndVisible()

        root.view = NSBundle.mainBundle.loadNibNamed("main", owner=self, options=NSDictionary.new()).firstObject()
        coll = find_view(root.view, "collectionview")
        logging.info("coll %s", coll)
        coll.registerClass(UICollectionViewCell, forCellWithReuseIdentifier="knob")
        self.cant = get_cant_roller()
        coll.setDataSource(self.cant)

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("old orientation %s", oldStatusBarOrientation)


logging.debug("yippie, %s defined", PythonAppDelegate)


def logged(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            logging.exception("%s", f)
            raise
    return inner


def get_cant_roller():
    size = 16
    tiles = None
    solved = [False] * size
    closed = dict()
    opened = dict()
    tapmap = dict()
    cells = dict()
    last = None

    def reset():
        nonlocal size, last, tiles
        size = 16
        tiles = game.get_tiles(size)
        solved[:] = [False] * size
        last = None

        # FIXME ugly hack
        for i, view in opened.items():
            label = find_view(view, "text")
            label.text = tiles[i][1]

        # same here
        for i in cells:
            flip(i, back=True)

    def flip(i, back=False):
        old, new = (opened[i], closed[i]) if back else (closed[i], opened[i])
        send_message(UIView,
                     b"transitionFromView:toView:duration:options:completion:",
                     old,
                     new,
                     NSTimeInterval(0.3),
                     UIViewAnimationOptionTransitionFlipFromBottom,
                     None)

    class CantRoller(UIViewController):
        """ Implements following protocols:
            * UICollectionViewDataSource and output 4x4 array of cells
            * UICollectionViewDelegate and gets notified when cell is clicked
        """
        # def __init__(self): init is not ran, as this is instantiated via ObjC runtime

        @objc_method
        def collectionView_numberOfItemsInSection_(self, view, section: int) -> int:
            logging.debug("numberOfItemsInSection %s", section)
            return 16

        @objc_method
        @logged
        def collectionView_cellForItemAtIndexPath_(self, view, path):
            i = path.item
            rv = view.dequeueReusableCellWithReuseIdentifier("knob", forIndexPath=path)
            cells[i] = rv
            closed[i] = NSBundle.mainBundle.loadNibNamed("knob", owner=self, options=NSDictionary.new()).firstObject()
            opened[i] = NSBundle.mainBundle.loadNibNamed("open", owner=self, options=NSDictionary.new()).firstObject()
            label = find_view(opened[i], "text")
            label.text = tiles[i][1]
            closed[i].retain()
            opened[i].retain()
            rv.addSubview(closed[i])
            rec = UITapGestureRecognizer.alloc().initWithTarget(self, action=SEL("tap:"))
            tapmap[rec.ptr.value] = i
            rv.addGestureRecognizer(rec)
            return rv

        @objc_method
        @logged
        def tap_(self, rec):
            nonlocal last
            i = tapmap[rec.ptr.value]

            # block already solved tiles; block current open tile
            if solved[i] or last == i:
                return

            if last is not None and tiles[last][0] == tiles[i][0]:
                solved[last] = True
                solved[i] = True
                last = None
                flip(i)
                if all(solved):
                    sound.victory()
                    self.performSelector(SEL("reset:"), withObject=None, afterDelay=NSTimeInterval(1))
                    return
                else:
                    sound.match()
                    return

            # after solving a tile or at the start of the game
            if last is not None:
                flip(last, back=True)

            flip(i)
            last = i
            sound.tap()

        @objc_method
        def reset_(self):
            reset()

    reset()  # or load saved state
    return CantRoller.new()
