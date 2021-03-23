"""
src/watcher.py

written by: Oliver Cordes 2021-03-23
changed by: Oliver Cordes 2021-03-23
"""

import rumps

from helper import isDarkMode

class MacVPNWatcherApp(object):
    def __init__(self):
        #self.app = rumps.App('MacVPNWatcher', '🍅')

        if isDarkMode:
            icon='../icons/appicon-dark.icns'
        else:
            icon='../icons/appicon.icns'
        self.app = rumps.App('MacVPNWatcher', icon=icon)

    def run(self):
        self.app.run()

