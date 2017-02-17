import logging

from rubicon.objc import objc_method, ObjCClass, ObjCInstance, send_message
logging.debug("yippie, loaded objc")

class NSString(ObjCInstance):
    @classmethod
    def from_python(cls, s):
        b = s.encode('utf8')
        obj = send_message(ObjCClass("NSString"), b'stringWithUTF8String:', b)
        return cls(obj)

    def __str__(self):
        s = ctypes.string_at(self.send(b'UTF8String', raw=True))
        return s.decode('utf8')

import ctypes
import ctypes.util
extension = ctypes.cdll.LoadLibrary(ctypes.util.find_library("extension"))
extension.NSLog.restype = None
extension.NSLog.argtypes = (ctypes.c_void_p, )


def NSLog(s):
    extension.NSLog(NSString.from_python(s))


for i in range(10):
    NSLog("foobarbazgoogoooooo\N{EURO SIGN} %s" % i)
