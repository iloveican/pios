""" whatever is dumped to syslog is visible in simulator's host Console """
import runpy
import syslog
import logging


class SyslogFile:
    """ Low-level debug, visible in Simulator -> Debug -> Open System Log… """
    def write(self, s):
        if s.strip():
            syslog.syslog(syslog.LOG_ERR, s.strip())


def handler():
    return logging.StreamHandler(stream=SyslogFile())


logging.basicConfig(level=logging.DEBUG, handlers=[handler()])
logging.debug("bootstrap logging initialised")

try:
    runpy.run_module("ui")
except:
    logging.exception("something went wrong")
