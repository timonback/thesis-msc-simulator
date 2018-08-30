import logging
import sys


def setup_logging(filename, level=logging.INFO, level_file=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level_file)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)

    fh = logging.FileHandler(filename)
    fh.setLevel(level_file)
    fh.setFormatter(formatter)
    root.addHandler(fh)

    root.info("Logging is starting...")
