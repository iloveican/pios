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

        # nav = UINavigationController.alloc().initWithRootViewController_(root)
        # win.rootViewController = nav

        win = UIWindow.alloc().initWithFrame_(UIScreen.mainScreen.bounds)
        win.rootViewController = root
        win.makeKeyAndVisible()

        root.view = NSBundle.mainBundle.loadNibNamed_owner_options_("main", self, NSDictionary.new()).firstObject()
        coll = find_view(root.view, "collectionview")
        logging.info("coll %s", coll)
        coll.registerClass_forCellWithReuseIdentifier_(UICollectionViewCell, "knob")
        self.cant = get_cant_roller()
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


def get_cant_roller():
    size = 16
    tiles = game.get_tiles(size)
    solved = [False] * size
    closed = dict()
    opened = dict()
    tapmap = dict()
    cells = dict()
    last = None

    def flip(cant, i, back=False):
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
            * UICollectionViewDataSource and output 3x3 array of cells
            * UICollectionViewDelegate and gets notified when cell is clicked
        """
        # def __init__(self): init is not ran, as this is instantiated via ObjC runtime

        @objc_method
        def reset(self):
            pass

        @objc_method
        def collectionView_numberOfItemsInSection_(self, view, section: int) -> int:
            logging.debug("el in sec called %s", section)
            return 16

        @objc_method
        @logged
        def collectionView_cellForItemAtIndexPath_(self, view, path):
            i = path.item
            rv = view.dequeueReusableCellWithReuseIdentifier_forIndexPath_("knob", path)
            cells[i] = rv
            closed[i] = NSBundle.mainBundle.loadNibNamed_owner_options_("knob", self, NSDictionary.new()).firstObject()
            opened[i] = NSBundle.mainBundle.loadNibNamed_owner_options_("open", self, NSDictionary.new()).firstObject()
            closed[i].retain()
            opened[i].retain()
            rv.addSubview_(closed[i])
            rec = UITapGestureRecognizer.alloc().initWithTarget_action_(self, get_selector("tap:"))
            tapmap[rec.ptr.value] = i
            rv.addGestureRecognizer_(rec)
            return rv

        @objc_method
        @logged
        def tap_(self, rec):
            i = tapmap[rec.ptr.value]
            if solved[i]:
                return

            nonlocal last
            if last is not None:
                flip(self, last, back=True)

            flip(self, i)
            last = i

        @objc_method
        def collectionView_didSelectItemAt_(self, view, indexPath):
            logging.debug("selected cell at %s %s", indexPath, indexPath.item)

    return CantRoller.new()


""" Code example from Ruby:
        alert = UIAlertView.new
        alert.message = "Hello iOS!"
        alert.show
"""
