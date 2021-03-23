"""
src/helper.py

written by: Oliver Cordes 2021-03-23
changed by: Oliver Cordes 2021-03-23
"""

import AppKit


def getInterfaceStyle():
    defaults = AppKit.NSUserDefaults.standardUserDefaults()

    return defaults.get('AppleInterfaceStyle')


def isDarkMode():
    return getInterfaceStyle() == 'Dark'

