import nslog
import logging

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


# define PythonAppDelegate

# implement the protocol:
# * applicationDidBecomeActive (to test)
# * application:didFinishLaunchingWithOptions: (where you create window and view)
# * application:didChangeStatusBarOrientation: (test screen orientation)

# Resources:
# https://oleb.net/blog/2012/02/app-launch-sequence-ios-revisited/
# https://stackoverflow.com/questions/7520971/applications-are-expected-to-have-a-root-view-controller-at-the-end-of-applicati

# Figure out window size
# Create a window
# Create a view controller
# Set window's root view controller
# Create a view
# Set controller's view
# display something in the view (to see that it works)


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

        win = UIWindow.alloc().initWithFrame(UIScreen.mainScreen.bounds)
        win.rootViewController = root
        win.makeKeyAndVisible()

        root.view = UIView.new()
        lab = UILabel.alloc().initWithFrame(rect(50, 50, 200, 200))
        lab.text = "Blah-blah yada-yada"
        lab.setBackgroundColor(UIColor.whiteColor)
        root.view.addSubview(lab)

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("old orientation %s", oldStatusBarOrientation)
