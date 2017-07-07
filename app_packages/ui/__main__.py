import nslog
import logging


# 1 / 0  # Crash for now


if __name__.split(".")[-1] == "__main__":
    # I'm ran as a module
    # drop low-level logging handler
    # set up logging properly
    del logging.root.handlers[:]
    logging.basicConfig(level=logging.DEBUG, handlers=[nslog.handler()])
    import sys
    logging.warn("%s", sys.path)
    logging.warn("%s", __file__)
    logging.debug("yep, I'm ran as a module")
    1 / 0
