import nslog
import logging
import functools

from rubicon.objc import objc_method, ObjCClass
from rubicon.objc.types import CGSize, CGRect, CGPoint

import game


if __name__.split(".")[-1] == "__main__":
    # I'm ran as a module
    logging.root.addHandler(nslog.handler())
    logging.debug("yep, in main")

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
UICollectionViewFlowLayout = ObjCClass("UICollectionViewFlowLayout")
NSBundle = ObjCClass("NSBundle")
NSArray = ObjCClass("NSArray")
NSMutableArray = ObjCClass("NSMutableArray")
NSDictionary = ObjCClass("NSDictionary")


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
        root.title = "Root title"
        nav = UINavigationController.alloc().initWithRootViewController_(root)

        win = UIWindow.alloc().initWithFrame_(UIScreen.mainScreen.bounds)
        win.rootViewController = nav
        win.makeKeyAndVisible()

        root.view = NSBundle.mainBundle.loadNibNamed_owner_options_("main", self, NSDictionary.alloc().init()).firstObject()
        coll = find_view(root.view, "collectionview")
        logging.info("coll %s", coll)
        coll.registerClass_forCellWithReuseIdentifier_(UICollectionViewCell, "knob")
        self.cant = cant = CantRoller.new()
        coll.setDataSource_(cant)
        coll.setDelegate_(cant)

        #    try:
        #        lay = UICollectionViewFlowLayout.new()
        #        lay.itemSize = CGSize(100, 100)
        #        coll = UICollectionView.alloc().initWithFrame_collectionViewLayout_(rect(0, 60, 320, 320), lay)
        #        coll.registerClass_forCellWithReuseIdentifier_(UICollectionViewCell, "knob")
        #        self.cant = cant = CantRoller.new()
        #        coll.setDataSource_(cant)
        #        coll.setDelegate_(cant)
        #        # UIApplication.sharedApplication.keyWindow.addSubview_(coll)
        #    except:
        #        logging.exception("just bad")

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


    def reset(self):
        self.size = 16
        self.open = [False] * self.size
        self.solved = [False] * self.size
        self.tiles = game.get_tiles(self.size)

    @objc_method
    def collectionView_numberOfItemsInSection_(self, view, section: int) -> int:
        logging.debug("el in sec called %s", section)
        return 16

    @objc_method
    # @logged
    def collectionView_cellForItemAtIndexPath_(self, view, path):
        rv = view.dequeueReusableCellWithReuseIdentifier_forIndexPath_("knob", path)
        view = NSBundle.mainBundle.loadNibNamed_owner_options_("knob", self, NSDictionary.alloc().init()).firstObject()
        rv.addSubview_(view)
        logging.info("created cell %s", rv)
        return rv

    @objc_method
    def collectionView_didSelectItemAt_(self, view, indexPath):
        logging.debug("selected cell at %s %s", indexPath, indexPath.item)


""" Code example from Ruby:
        alert = UIAlertView.new
        alert.message = "Hello iOS!"
        alert.show
"""
