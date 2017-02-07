import syslog
import sys
syslog.syslog(syslog.LOG_ERR, "X11")
# syslog.syslog(syslog.LOG_ERR, "sys.path %s" % sys.path)
syslog.syslog(syslog.LOG_ERR, "sys.path %s" % "\n".join(sys.path))
import os
syslog.syslog(syslog.LOG_ERR, "ls dimark:\n%s" % "\n".join(os.listdir(sys.path[0])))
try:
    import bootstrap
except Exception as e:
    syslog.syslog(syslog.LOG_ERR, "X11 %r" % e)
except BaseException:
    syslog.syslog(syslog.LOG_ERR, "X11.... %r" % e)
# import logging
try:
    from rubicon.objc import objc_method
except Exception:
    pass
except BaseException:
    pass

try:
    import ctypes
    self = ctypes.CDLL(None)
    self.printf("X\n" * 100)
    # self.fprintf(self.fdopen(2, "a"), "Y" * 100)
except Exception:
    pass
except BaseException:
    pass

try:
    import ctypes
    import ctypes.util

    # Need to do this to load the NSSpeechSynthesizer class, which is in AppKit.framework
    appkit = ctypes.cdll.LoadLibrary(ctypes.util.find_library('AppKit'))
    objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))

    objc.objc_getClass.restype = ctypes.c_void_p
    objc.sel_registerName.restype = ctypes.c_void_p
    objc.objc_msgSend.restype = ctypes.c_void_p
    objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

    # Without this, it will still work, but it'll leak memory
    NSAutoreleasePool = objc.objc_getClass('NSAutoreleasePool')
    pool = objc.objc_msgSend(NSAutoreleasePool, objc.sel_registerName('alloc'))
    pool = objc.objc_msgSend(pool, objc.sel_registerName('init'))

    NSSpeechSynthesizer = objc.objc_getClass('NSSpeechSynthesizer')
    availableVoices = objc.objc_msgSend(NSSpeechSynthesizer, objc.sel_registerName('availableVoices'))

    count = objc.objc_msgSend(availableVoices, objc.sel_registerName('count'))
    voiceNames = [
        ctypes.string_at(
            objc.objc_msgSend(
                objc.objc_msgSend(availableVoices, objc.sel_registerName('objectAtIndex:'), i),
                objc.sel_registerName('UTF8String')))
              for i in range(count)]
# print voiceNames

    objc.objc_msgSend(pool, objc.sel_registerName('release'))
except Exception:
    pass
except BaseException:
    pass


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
