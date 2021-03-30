"""
src/watcher.py

written by: Oliver Cordes 2021-03-23
changed by: Oliver Cordes 2021-03-29
"""

import os, sys
import logging
import time

import rumps

from AppKit import NSMutableParagraphStyle, NSCenterTextAlignment, NSLineBreakByTruncatingMiddle, NSFontAttributeName, \
    NSFont, NSForegroundColorAttributeName, NSColor, NSParagraphStyleAttributeName, NSAttributedString, \
    NSString, NSTextTab, NSRightTextAlignment, NSSizeFromString

from helper import isDarkMode

from vpn import list_of_vpn_connections, connect_vpn, disconnect_vpn


AppName = 'MacVPNWatcher'
sleep_timeout_trigger  = 60
sleep_reaction_trigger = 60

#rumps.debug_mode(True)

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
    return text


def string_size_on_screen(s):
    paragraph = NSMutableParagraphStyle.alloc().init()
    attributes = {
        NSParagraphStyleAttributeName: paragraph,
    }
    text = NSAttributedString.alloc().initWithString_attributes_(s, attributes)

    return text.size().width


class Event(object):
    def __init__(self):
        self._state = False
        self._time  = 0

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val
        if val:
            self._time = time.time()
        else:
            self._time = 0

    def changed(self):
        return time.time() - self._time



class MacVPNWatcherApp(object):
    def __init__(self):
        #self.app = rumps.App('MacVPNWatcher', '🍅')

        if isDarkMode:
            icon='icons/appicon-dark.icns'
        else:
            icon='icons/appicon.icns'
        self.app = rumps.App(AppName, icon=icon)

        # internal variables
        self._connections = {}
        self._menu_items = {}
        self._menu_maxlen = 0
        #self._is_connected = None
        self._trigger_action = False
        self._last_checked = 0
        #self._sleep_detected = False

        self._last_connection = None
        self._ev_connected = Event()
        self._ev_awake = Event()

        # generate the main menu
        self.generate_menu()

        self._app_supportdir = rumps.application_support(AppName)

        logging.basicConfig(level=logging.DEBUG, 
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=os.path.join(self._app_supportdir, 'app.log'),
                            format='%(asctime)s %(levelname)s - %(message)s'
                            )
        logging.debug('App started...')

        # setup the watch timer
        self.timer = rumps.Timer(self.check_status, 5)
        self.timer.start()


    def generate_menu(self):
        conns = list_of_vpn_connections()
        # add connections from VPN list                      
        self._menu_maxlen = max([string_size_on_screen(f'{i} (Disconnecting)') for i in conns.keys()])
        for conn in sorted(conns.keys()):
            if conn not in self._connections:
                title = conn
                atitle = format_string(f'{conn}\t({conns[conn]["status"]})', self._menu_maxlen)
                menuitem = rumps.MenuItem(title,
                    callback=callback_template(conn, self.clicked_connection))
                menuitem._menuitem.setAttributedTitle_(atitle)
                self._menu_items[conn] = menuitem
                self._connections[conn] = conns[conn]

                # remember the item for which the connection is connected
                if conns[conn]['status'] == 'Connected':
                    self._is_connected = conn
                    self._ev_connected.state = True
                    self._last_connection = conn


        # look for removed connections
        for conn in self._connections:
            if conn not in conns:
                self._connections.pop(conn)

        #self._slider = rumps.SliderMenuItem(dimensions=(180, 30))
        self.app.menu = [self._menu_items[i] for i in self._menu_items] + [rumps.separator]#+ [self._slider]

        # update the icon
        self.update_icon()


    def sleep_detection(self):
        timenow = time.time()
        timediff = timenow - self._last_checked
        sleep_detected = (timediff > sleep_timeout_trigger) and (
            self._last_checked != 0)
        if sleep_detected:
            logging.info(f'Sleep > {timediff} seconds detected!')
            self._ev_awake.state = True
        self._last_checked = timenow


    def update_menu(self):
        self.sleep_detection()
            
        conns = list_of_vpn_connections()

        # save the variable
        was_connected = self._ev_connected.state

        # nothing is connected
        self._ev_connected.state = False
        for conn in conns:
            if conn in self._connections:
                # change the variables if something is connected
                if conns[conn]['status'] == 'Connected':
                    #self._is_connected = conn
                    self._ev_connected.state = True
                    self._last_connection = conn

                # has a connection changed?
                if self._connections[conn]['status'] != conns[conn]['status']:
                    # status has changed
                    # update the internal connection data
                    self._connections[conn] = conns[conn]
                    # update the menu item
                    menuitem = self._menu_items[conn]
                    atitle = format_string(
                        f'{conn}\t({conns[conn]["status"]})', self._menu_maxlen)
                    menuitem._menuitem.setAttributedTitle_(atitle)
                    logging.info(f'Status changed: {conn} -> {conns[conn]["status"]}')

                    if self._trigger_action:
                        if conns[conn]["status"] in ('Connected', 'Disconnected'):
                            self._trigger_action = False
                            #self._sleep_detected = False
                        if conns[conn]['status'] == 'Disconnected' and self._last_connection == conn:
                            self._last_connection = None
                    #else:
                    #    logging.warning('VPN status has changed without app trigger!')
                    #    if (was_connected == conn) and (conns[conn]["status"] == 'Disconnected'):
                    #        logging.warning(f'VPN connection {conn} was interrupted!')
                    #        if self._sleep_detected:
                    #            logging.info(f'Want to reestablish connection for {conn}!')
                    #            self._sleep_detected = False
                    #            # reconnect the VPN
                    #            connect_vpn(conn)
                    #            self._trigger_action = True


        # so the status is:
        # self._last_connection has the old connection
        # self._ev_connected.state shows if connected or not
        if not self._ev_connected.state:
            if self._last_connection and (conns[self._last_connection]['status'] == 'Disconnected'):
                # a connection was interrupted
                logging.warning(f'VPN connection {self._last_connection} was interrupted!')
                if self._ev_awake.state and (self._ev_awake.changed < sleep_reaction_trigger):
                    # was there an awake event 
                    logging.warning(f'Want to reestablish connection for {self._last_connection}!')
                    # reconnect
                    connect_vpn(self._last_connection)
                    self._trigger_action = True
                else:
                    logging.warning(f'No wakeup detected! Must be another program!')
                # there is no last connection anymore
                self._last_connection = None

        # clear the awake event
        if self._ev_awake.state and (self._ev_awake.changed >= sleep_reaction_trigger):
            self._ev_awake.state = False

        # update icons if necessary
        #logging.info(f'{self._ev_connected.state} vs. {was_connected}')
        if self._ev_connected.state != was_connected:
            logging.info(f'Updating icons ...')
            self.update_icon()



    def update_icon(self):
        if self._ev_connected.state:
            if isDarkMode:
                self.app.icon = 'icons/appicon-dark.icns'
            else:
                self.app.icon = 'icons/appicon.icns'
        else:
            if isDarkMode:
                self.app.icon = 'icons/appicon-offline-dark.icns'
            else:
                self.app.icon = 'icons/appicon-offline.icns'


    def click(self, sender):
        print('click', sender)



    def clicked_connection(self, name, sender):
        #print('clicked:', name)
        if name in self._connections:
            if self._connections[name]['status'] == 'Connected':
                logging.info(f'Disconnecting {name} ...')
                disconnect_vpn(name)
            else:
                if self._ev_connected.state:
                    logging.info(f'Disconnecting {self._last_connection} ...')
                    disconnect_vpn(self._last_connection)
                logging.info(f'Connecting {name} ...')
                connect_vpn(name)
        self._trigger_action = True


    def check_status(self, sender):
        #logging.debug('check_status')
        self.update_menu()


    def run(self):
        self.app.run()


