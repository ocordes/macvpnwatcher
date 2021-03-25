"""
src/watcher.py

written by: Oliver Cordes 2021-03-23
changed by: Oliver Cordes 2021-03-25
"""

import rumps

from helper import isDarkMode

from vpn import list_of_vpn_connections

rumps.debug_mode(True)

# mimik a callback_template to feed the connection name 
# as a parameter
def callback_template(name, func):
    def callback(sender):
        func(name, sender)

    return callback


class MacVPNWatcherApp(object):
    def __init__(self):
        #self.app = rumps.App('MacVPNWatcher', '🍅')

        if isDarkMode:
            icon='icons/appicon-dark.icns'
        else:
            icon='icons/appicon.icns'
        self.app = rumps.App('MacVPNWatcher', icon=icon)

        self._connections = {}
        self._menu_items = {}
        self.update_menu()


    def update_menu(self):
        conns = list_of_vpn_connections()
        # add connections from VPN list
        for conn in sorted(conns.keys()):
            if conn not in self._connections:
                menuitem = rumps.MenuItem(conn, callback=callback_template(conn, self.clicked_connection))
                #menuitem = rumps.MenuItem(conn, callback=self.click)
                self._menu_items[conn] = menuitem
                self._connections[conn] = conns[conn]

        # look for removed connections
        for conn in self._connections:
            if conn not in conns:
                self._connections.pop(conn)

        print(self._connections)

        self.app.menu = [self._menu_items[i] for i in self._menu_items]


    def click(self, sender):
        print('click', sender)



    def clicked_connection(self, name, sender):
        print('clicked:', name)


    def run(self):
        self.app.run()

