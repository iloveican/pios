import nslog
import logging


if __name__.split(".")[-1] == "__main__":
    # I'm ran as a module
    # drop low-level logging handler
    # set up logging properly
    del logging.root.handlers[:]
    logging.basicConfig(level=logging.DEBUG, handlers=[nslog.handler()])

    # Interesting code goes here
    1 / 0
