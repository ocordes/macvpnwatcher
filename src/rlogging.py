"""
src/rlogging.py

written by: Oliver Cordes 2021-04-29
changed by: Oliver Cordes 2021-04-29

"""

import os
import logging
import logging.handlers
import gzip


# name the compressed file
def namer(name):
    return name + ".gz"

# read the data from source, compress it, write it to dest and delete source
def rotator(source, dest):
    with open(source, "rb") as sf:
        data = sf.read()
        with gzip.open(dest, "wb", compresslevel=9) as df:
            df.write(data)
    os.remove(source)



def setup_logging(logdir):
    format = '%(asctime)s %(levelname)s - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(format, datefmt)
    logfilename = os.path.join(logdir, 'app.log')

    # get the root logger
    logger = logging.getLogger()

    # Creates at most 5 backup whenever the filesize equals to or exceeds 250 bytes
    handler = logging.handlers.RotatingFileHandler(filename=logfilename,
                                                   maxBytes=1024*1024,
                                                   #maxBytes=250,
                                                   backupCount=5)

    # configure the logger
    handler.setFormatter(formatter)
    handler.rotator = rotator
    handler.namer = namer
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger
