import nslog
import random
import logging
import functools

from rubicon.objc import objc_method, ObjCClass
from rubicon.objc.types import CGSize, CGRect, CGPoint


if __name__.split(".")[-1] == "__main__":
    # I'm ran as a module
    logging.root.addHandler(nslog.handler())
    logging.debug("yep, in main")


# class Knob(ObjCClass("UICollectionViewCell")):
#     @objc_method
#     # def collectionView(self, cellForItemAtIndexPath: indexPath):
#     def collectionView(self, indexPath):
#         logging.debug("collection view %s", [self, indexPath])
# 
# 
# class Knobs(ObjCClass("UICollectionView")):
#     @objc_method
#     def numberOfSections(self) -> int:
#         return 3
# 
#     @objc_method
#     def collectionView(self, section: int) -> int:
#         return 4
# 
#     @objc_method
#     # def collectionViewWithReuseIdentifier(self, index_path) -> ObjCClass("UICollectionViewCell"):
#     def collectionViewWithReuseIdentifier(self, index_path):
#         logging.debug("viewee used")
#         self.dequeueReusableCell("thumb", indexPath)
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

NSCenterTextAlignment = 2


def rect(x, y, w, h):
    """ A la CGRectMake """
    return CGRect(CGPoint(x, y), CGSize(w, h))


class PythonAppDelegate(UIResponder):
    # def __init__(self): init is not ran, as this is instantiated by ObjC runtime

    @objc_method
    def applicationDidBecomeActive(self) -> None:
        logging.debug("became active")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("finished launching %s %s", application, oldStatusBarOrientation)

        root = UIViewController.new()
        root.title = "Hello"
        root.view.backgroundColor = UIColor.blueColor()
        # root.view.backgroundColor = UIColor.alloc().initWithWhite_alpha_(0.5, 0.5)
        nav = UINavigationController.alloc().initWithRootViewController_(root)

        win = UIWindow.alloc().initWithFrame_(UIScreen.mainScreen().bounds)
        win.rootViewController = nav
        win.makeKeyAndVisible()

        try:
            lay = UICollectionViewFlowLayout.new()
            lay.itemSize = CGSize(30, 30)
            view = UICollectionView.alloc().initWithFrame_collectionViewLayout_(rect(3, 53, 300, 300), lay)
            view.registerClass_forCellWithReuseIdentifier_(UICollectionViewCell, "knob")
            self.cant = cant = CantRoller.new()
            view.setDataSource_(cant)
            view.setDelegate_(cant)
            UIApplication.sharedApplication().keyWindow.addSubview_(view)
        except:
            logging.exception("just bad")

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

    # @objc_method
    # def collectionView_numberOfSections_(self) -> int:
        # logging.debug("no sec called")
        # return 3

    @objc_method
    def collectionView_numberOfItemsInSection_(self, view, section: int) -> int:
        logging.debug("el in sec called %s", section)
        return 9

    @objc_method
    # @logged
    def collectionView_cellForItemAtIndexPath_(self, view, path):
        rv = view.dequeueReusableCellWithReuseIdentifier_forIndexPath_("knob", path)
        rv.backgroundColor = UIColor.alloc().initWithRed_green_blue_alpha_(random.random(),
                                                                           random.random(),
                                                                           random.random(), 1)
        la = labels[path.item] = UILabel.alloc().initWithFrame_(rect(0, 0, 30, 30))
        la.text = str(path.item)
        rv.addSubview_(la)
        return rv

    @objc_method
    def collectionView_didSelectItemAt_(self, view, indexPath):
        logging.debug("selected cell at %s %s", indexPath, indexPath.item)


""" Code example from Ruby:
        alert = UIAlertView.new
        alert.message = "Hello iOS!"
        alert.show
"""
