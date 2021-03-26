"""
src/watcher.py

written by: Oliver Cordes 2021-03-23
changed by: Oliver Cordes 2021-03-25
"""

import rumps

from AppKit import NSMutableParagraphStyle, NSCenterTextAlignment, NSLineBreakByTruncatingMiddle, NSFontAttributeName, \
    NSFont, NSForegroundColorAttributeName, NSColor, NSParagraphStyleAttributeName, NSAttributedString, \
    NSString, NSTextTab, NSRightTextAlignment, NSSizeFromString

from helper import isDarkMode

from vpn import list_of_vpn_connections

rumps.debug_mode(True)

# mimik a callback_template to feed the connection name 
# as a parameter
def callback_template(name, func):
    def callback(sender):
        func(name, sender)

    return callback

def format_string(s, size):
    paragraph = NSMutableParagraphStyle.alloc().init()
    #paragraph.setAlignment_(NSCenterTextAlignment)
    #paragraph.setLineBreakMode_(NSLineBreakByTruncatingMiddle)
    tabstop = NSTextTab.alloc().initWithTextAlignment_location_options_(NSRightTextAlignment, size*1.2, None)
    paragraph.setTabStops_([tabstop])
    attributes = {
        #NSFontAttributeName: NSFont.systemFontOfSize_(10.0),
        #NSForegroundColorAttributeName: NSColor.colorWithCalibratedRed_green_blue_alpha_(.22, .22, .27, 1.0),
        NSParagraphStyleAttributeName: paragraph,
    }
    text = NSAttributedString.alloc().initWithString_attributes_(s, attributes)

    print(text.size())

    return text


def string_size_on_screen(s):
    paragraph = NSMutableParagraphStyle.alloc().init()
    attributes = {
        NSParagraphStyleAttributeName: paragraph,
    }
    text = NSAttributedString.alloc().initWithString_attributes_(s, attributes)

    return text.size().width


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
        maxlen = max([string_size_on_screen(f'{i} (Disconnected)') for i in conns.keys()])
        print(maxlen)
        for conn in sorted(conns.keys()):
            if conn not in self._connections:
                title = conn
                atitle = format_string(f'{conn}\t({conns[conn]["status"]})', maxlen)
                menuitem = rumps.MenuItem(title,
                    callback=callback_template(conn, self.clicked_connection))
                menuitem._menuitem.setAttributedTitle_(atitle)
                #menuitem = rumps.MenuItem(conn, callback=self.click)
                self._menu_items[conn] = menuitem
                self._connections[conn] = conns[conn]

        # look for removed connections
        for conn in self._connections:
            if conn not in conns:
                self._connections.pop(conn)

        print(self._connections)

        #self._slider = rumps.SliderMenuItem(dimensions=(180, 30))
        self.app.menu = [self._menu_items[i] for i in self._menu_items] + [rumps.separator]#+ [self._slider]



    def click(self, sender):
        print('click', sender)



    def clicked_connection(self, name, sender):
        print('clicked:', name)


    def run(self):
        self.app.run()

