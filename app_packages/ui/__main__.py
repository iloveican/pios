import nslog
import logging

from rubicon.objc import objc_method, ObjCClass


if __name__.split(".")[-1] == "__main__":
    # I'm ran as a module
    logging.root.addHandler(nslog.handler())
    logging.debug("yep, in main")


class PythonAppDelegate(ObjCClass('UIResponder')):
    def __init__(self):
        logging.debug("instance created")

    @objc_method
    def applicationDidBecomeActive(self) -> None:
        logging.debug("became active")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("finished launching %s %s", application, oldStatusBarOrientation)

        try:
            root = ObjCClass("UIViewController").alloc().init()
            root.title = "Hello"
            root.view.backgroundColor = ObjCClass("UIColor").blueColor()
            # root.view.backgroundColor = ObjCClass("UIColor").alloc().initWithWhite_alpha_(0.5, 0.5)
            nav = ObjCClass("UINavigationController").alloc().initWithRootViewController_(root)
        except:
            logging.exception("terrible")

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("or ch %s %s", application, oldStatusBarOrientation)

logging.debug("yippie, %s defined", PythonAppDelegate)


""" Code example from Ruby:

class AppDelegate
    def application(application, didFinishLaunchingWithOptions:launchOptions)
        rootViewController = UIViewController.alloc.init
        rootViewController.title = 'Hello'
        rootViewController.view.backgroundColor = UIColor.whiteColor

        navigationController = UINavigationController.alloc.initWithRootViewController(rootViewController)

        @window = UIWindow.alloc.initWithFrame(UIScreen.mainScreen.bounds)
        @window.rootViewController = navigationController
        @window.makeKeyAndVisible

        alert = UIAlertView.new
        alert.message = "Hello iOS!"
        alert.show

        true
    end
end
"""