"""
src/config.py

written by: Oliver Cordes 2021-03-31
changed by: Oliver Cordes 2022-08-27
"""

import os
import configparser
import logging

AppName = 'MacVPNWatcher'

__version__ = '0.1.5'
__author__ = 'Oliver Cordes'
__author_email__ = 'ocordes@astro.uni-bonn.de'
__copyright__ = '(C) Copyright 2021,2022'

debug = True
sleep_timeout_trigger = 60   # minimum must be > 20 seonds
sleep_reaction_trigger = 60



default_config_file = f"""# this is an example config file
# you can adjust everything you want!
#
#
[DEFAULT]
debug = False                 # True|False

# sleep_timeout_trigger
#
# time to detect real sleeps, if a sleep is below the trigger,
# MacOS will reconnect VPN automatically, if not, then reduce
# the time. A minimum > 20 seconds is necessary for the program
sleep_timeout_trigger  = {sleep_timeout_trigger}

# sleep_reaction_trigger
#
# time in which the program should react to a wakeup event
# DEPRECATED
sleep_reaction_trigger = {sleep_reaction_trigger}
"""


def read_config(filename):
    global debug, sleep_timeout_trigger, sleep_reaction_trigger
    if os.access(filename, os.R_OK):
        config = configparser.ConfigParser(inline_comment_prefixes=('#',';',','))
        config.read(filename)
        defaults = config['DEFAULT']
        debug = defaults.getboolean('debug', debug)
        sleep_timeout_trigger = defaults.getint('sleep_timeout_trigger', sleep_timeout_trigger)
        sleep_reaction_trigger = defaults.getint('sleep_reaction_trigger', sleep_reaction_trigger)
    else:
        logging.info(f'No config file detected \'{filename}\'! Create a default config file!')
        with open(filename, 'w') as f:
            f.write(default_config_file)

