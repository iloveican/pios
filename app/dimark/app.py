""" whatever is dumped to syslog is visible in simulator's host Console """
import os
import sys
import syslog
import logging


class SyslogFile:
    def write(self, s):
        if s.strip():
            syslog.syslog(syslog.LOG_ERR, s.strip())


logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler(stream=SyslogFile())])
logging.debug("bootstrap logging initialised")

# sources: <your-project-dir>/app_packages
# runtime: <path-to>/com.domain.shortname/app_packages
libs = os.path.realpath("%s/../../../app_packages" % __file__)
sys.path.append(libs)

import nslog

from rubicon.objc import objc_method, ObjCClass
logging.debug("yippie, loaded objc")

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
            nav = ObjCClass("UINavigationController").alloc().initWithRootViewController(root)
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
