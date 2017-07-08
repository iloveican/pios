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

        root.view = UIView.new()  # spans entire area

        # show something as a test, feel free to remove
        lab = UILabel.alloc().initWithFrame(rect(50, 50, 200, 200))
        lab.text = "Blah-blah yada-yada"
        lab.setBackgroundColor(UIColor.whiteColor)
        root.view.addSubview(lab)

        # create a collection view

        # come up with cell views and register its class (a factory)

        # here's how register an empty (not customised) cell view class
        # xxx.registerClass(UICollectionViewCell, forCellWithReuseIdentifier="knob")

        # set data source

    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        logging.debug("old orientation %s", oldStatusBarOrientation)


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


class CantRoller(UIViewController):
    """ Data source for collection view
        Implement following protocol:
        * UICollectionViewDataSource and output NxN array of cells
        * [opt] UICollectionViewDelegate and gets notified when cell is clicked
    """
    # def __init__(self): init is not ran, as this is instantiated via ObjC runtime

    @objc_method
    def collectionView_numberOfItemsInSection_(self, view, section: int) -> int:
        ...

    @objc_method
    @logged
    def collectionView_cellForItemAtIndexPath_(self, view, path):
        i = path.item  # actual index
        # see "foobar" in the application delegate
        rv = view.dequeueReusableCellWithReuseIdentifier("foobar", forIndexPath=path)
        # reset this cell (in case it was reused)
        # fill this cell with whatever needs to be shown
        return rv
