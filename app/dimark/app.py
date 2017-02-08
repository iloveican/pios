import logging
import bootstrap

try:
    from rubicon.objc import objc_method
    logging.debug("yippie, loaded objc")
except (Exception, BaseException):
    logging.exception("oh no")

try:
    # class PythonAppDelegate():
  class xxPythonAppDelegate(UIResponder):
    def __init__(self):
        print("starting")
        logging.warn("hahaha")

    @objc_method
    def applicationDidBecomeActive(self) -> None:
        print("became active")

    @objc_method
    def application_didFinishLaunchingWithOptions_(self, application, oldStatusBarOrientation: int) -> None:
        print("finished launching", application, oldStatusBarOrientation)


    @objc_method
    def application_didChangeStatusBarOrientation_(self, application, oldStatusBarOrientation: int) -> None:
        print("or ch", application, oldStatusBarOrientation)
except Exception:
    pass
except BaseException:
    pass
