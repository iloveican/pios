import nslog
import logging
import functools

from rubicon.objc import objc_method, ObjCClass, get_selector, send_message
from rubicon.objc.types import CGSize, CGRect, CGPoint, NSTimeInterval

import game


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

UIViewAnimationOptionTransitionFlipFromBottom  = 7 << 20


def rect(x, y, w, h):
    """ A la CGRectMake """
    return CGRect(CGPoint(x, y), CGSize(w, h))


def pylist(a):
    return [a.objectAtIndex_(i) for i in range(a.count)]


def py(o):
    logging.debug("input %s", o.__dict__)
    return o


def test_py():
    a = NSArray.alloc().init()
    logging.info("NSArray %s", (a, py(a)))

    m = NSMutableArray.alloc().init()
    logging.info("NSMutableArray %s", (m, py(m)))

    d = NSDictionary.alloc().init()
    logging.info("NSDictionary %s", (d, py(d)))


def all_views(v):
    yield v
    for vv in pylist(v.subviews()):
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
        # TODO how to get rid of title?
        # root.title = "Root title"
        # root.titleView = None
        # root.titleView.setHidden(True)
        # root.titleView = UIView.alloc().initWithFrame_(rect(0, 0, 0, 0))
        # root.title = ""

        nav = UINavigationController.alloc().initWithRootViewController_(root)

        win = UIWindow.alloc().initWithFrame_(UIScreen.mainScreen.bounds)
        win.rootViewController = nav
        win.makeKeyAndVisible()

        root.view = NSBundle.mainBundle.loadNibNamed_owner_options_("main", self, NSDictionary.alloc().init()).firstObject()
        coll = find_view(root.view, "collectionview")
        logging.info("coll %s", coll)
        coll.registerClass_forCellWithReuseIdentifier_(UICollectionViewCell, "knob")
        self.cant = CantRoller.new()
        self.cant.reset()
        coll.setDataSource_(self.cant)
        coll.setDelegate_(self.cant)

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("old orientation %s", oldStatusBarOrientation)

logging.debug("yippie, %s defined", PythonAppDelegate)


labels = dict()


def logged(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            logging.exception("%s", f)
            raise
    return inner


class CantRoller(UIViewController):
    """ Implements following protocols:
        * UICollectionViewDataSource and output 3x3 array of cells
        * UICollectionViewDelegate and gets notified when cell is clicked
    """
    # def __init__(self): init is not ran, as this is instantiated via ObjC runtime
    size = open = None

    @objc_method
    def reset(self):
        self.size = 16
        self.open = [False] * self.size
        self.solved = [False] * self.size
        self.tiles = game.get_tiles(self.size)
        self.tapmap = dict()
        self.cells = dict()
        self.closed = dict()
        self.opened = dict()

    @objc_method
    def collectionView_numberOfItemsInSection_(self, view, section: int) -> int:
        logging.debug("el in sec called %s", section)
        return 16

    @objc_method
    @logged
    def collectionView_cellForItemAtIndexPath_(self, view, path):
        i = path.item
        rv = view.dequeueReusableCellWithReuseIdentifier_forIndexPath_("knob", path)
        self.cells[i] = rv
        self.closed[i] = NSBundle.mainBundle.loadNibNamed_owner_options_("knob", self, NSDictionary.alloc().init()).firstObject()
        self.opened[i] = NSBundle.mainBundle.loadNibNamed_owner_options_("open", self, NSDictionary.alloc().init()).firstObject()
        self.closed[i].retain()
        self.opened[i].retain()
        rv.addSubview_(self.closed[i])
        rec = UITapGestureRecognizer.alloc().initWithTarget_action_(self, get_selector("tap:"))
        self.tapmap[rec.ptr.value] = i
        rv.addGestureRecognizer_(rec)
        return rv

    @objc_method
    @logged
    def tap_(self, rec):
        i = self.tapmap[rec.ptr.value]
        logging.info("tap %s %s", i, self.open[i])
        old, new = (self.opened[i], self.closed[i]) if self.open[i] else (self.closed[i], self.opened[i])
        logging.info("%s -> %s", old, new)
        send_message(UIView,
                     b"transitionFromView:toView:duration:options:completion:",
                     old,
                     new,
                     NSTimeInterval(3),
                     UIViewAnimationOptionTransitionFlipFromBottom,
                     None)
        self.open[i] ^= True

    @objc_method
    def collectionView_didSelectItemAt_(self, view, indexPath):
        logging.debug("selected cell at %s %s", indexPath, indexPath.item)


""" Code example from Ruby:
        alert = UIAlertView.new
        alert.message = "Hello iOS!"
        alert.show
"""
