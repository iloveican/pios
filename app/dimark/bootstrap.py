""" whatever is dumperd to syslog is visible in simulator's host Console """
import logging
import syslog


class SyslogFile:
    def write(self, s):
        if s.strip():
            syslog.syslog(syslog.LOG_ERR, s.strip())


logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler(stream=SyslogFile())])
logging.debug("bootstrap logging initialised")
