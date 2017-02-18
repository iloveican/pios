import re
import logging
from rubicon.objc import ObjCClass, ObjCInstance, send_message


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


class NSLogFile:
    def write(self, s):
        if s.strip():
            NSLog(re.sub('File "[^"\n]*/site-packages/', 'File "', s.strip()))


def handler():
    return logging.StreamHandler(stream=NSLogFile())
