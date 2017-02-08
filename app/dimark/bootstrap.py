import logging
import syslog
syslog.syslog(syslog.LOG_ERR, "LINE------------")


class SyslogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__()
        self.stream = self

    def write(self, s):
        syslog.syslog(syslog.LOG_ERR, s.strip())


logging.basicConfig(level=logging.DEBUG, handlers=[SyslogHandler])

logging.debug("yippiiii")
