import nslog
import logging

from rubicon.objc import objc_method, ObjCClass, send_message
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
UIResponder = ObjCClass('UIResponder')
UIViewController = ObjCClass("UIViewController")
UIColor = ObjCClass("UIColor")
UINavigationController = ObjCClass("UINavigationController")
UIWindow = ObjCClass("UIWindow")
UIScreen = ObjCClass("UIScreen")
UICollectionViewFlowLayout = ObjCClass("UICollectionViewFlowLayout")
UICollectionView = ObjCClass("UICollectionView")
UIApplication = ObjCClass("UIApplication")


class PythonAppDelegate(UIResponder):
    def __init__(self):
        logging.debug("instance created")

    @objc_method
    def applicationDidBecomeActive(self) -> None:
        logging.debug("became active")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("finished launching %s %s", application, oldStatusBarOrientation)

        try:
            root = UIViewController.new()
            root.title = "Hello"
            root.view.backgroundColor = UIColor.blueColor()
            # root.view.backgroundColor = UIColor.alloc().initWithWhite_alpha_(0.5, 0.5)
            nav = UINavigationController.alloc().initWithRootViewController_(root)

            win = UIWindow.alloc().initWithFrame_(UIScreen.mainScreen().bounds)
            win.rootViewController = nav
            win.makeKeyAndVisible()
        except:
            logging.exception("terrible")

        try:
            lay = UICollectionViewFlowLayout.new()
            lay.itemSize = CGSize(300, 300)
            view = UICollectionView.alloc().initWithFrame_collectionViewLayout_(CGRect(CGPoint(3, 53),  # debug :)
                                                                                       CGSize(1000, 1000)), lay)
            UIApplication.sharedApplication().keyWindow.addSubview_(view)
        except:
            logging.exception("just bad")

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("or ch %s %s", application, oldStatusBarOrientation)

logging.debug("yippie, %s defined", PythonAppDelegate)


""" Code example from Ruby:
        alert = UIAlertView.new
        alert.message = "Hello iOS!"
        alert.show
"""
