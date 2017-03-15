import ctypes
import ctypes.util
audio = ctypes.cdll.LoadLibrary(ctypes.util.find_library("AudioToolbox"))
audio.AudioServicesPlaySystemSound.restype = None
audio.AudioServicesPlaySystemSound.argtypes = (ctypes.c_int, )


def tap():
    audio.AudioServicesPlaySystemSound(1305)


def match():
    audio.AudioServicesPlaySystemSound(1006)


def victory():
    audio.AudioServicesPlaySystemSound(1020)
