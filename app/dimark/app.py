""" whatever is dumped to syslog is visible in simulator's host Console """
import os
import sys
import runpy
import syslog
import logging


class SyslogFile:
    def write(self, s):
        if s.strip():
            syslog.syslog(syslog.LOG_ERR, s.strip())


def handler():
    return logging.StreamHandler(stream=SyslogFile())


logging.basicConfig(level=logging.DEBUG, handlers=[handler()])
logging.debug("bootstrap logging initialised")

# sources: <your-project-dir>/app_packages
# runtime: <path-to>/com.domain.shortname/app_packages
libs = os.path.realpath("%s/../../../app_packages" % __file__)
sys.path.append(libs)

try:
    runpy.run_module("ui")
except:
    logging.exception("something went wrong")
    raise
