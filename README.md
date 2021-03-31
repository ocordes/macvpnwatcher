# macvpnwatcher
Watch a VPN connection and reconnects whenever possible.



## Installation procedure:

```bash
python setup.py py2app
```

In ```dist``` there is the MacVPNWatcher App, which you can copy into your ```/Application``` folder.


For Running the App you don't need a developer account from Apple. All necessary entitlements are free.


## Development:

For development, clone this repo on your local hard disk:

```bash
python3 -m venv macvpnwatcher
source macvpnwatcher/bin/activate
pip3 install -r requirements-dev.txt
```

use 
```bash
deactivate
```
to leave the environment.

