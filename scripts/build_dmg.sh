#!/bin/bash

set -x

TMPDIR=/tmp/MacVPNWatcher

mkdir $TMPDIR
cp -rvp ../dist/* $TMPDIR
#cp -rvp ../dmg_template/.[a-zA-Z]* $TMPDIR
cp -rvp ../dmg_template/.background $TMPDIR/.background
cp -rvp ../dmg_template/DS_Store $TMPDIR/.DS_Store
(cd $TMPDIR; ln -s /Applications .)
#hdiutil create /tmp/tmp.dmg -ov -volname "MacVPNWatcher" -fs HFS+ -srcfolder "/tmp/tmpapp"
hdiutil makehybrid -hfs -hfs-volume-name MacVPNWatcher -hfs-openfolder $TMPDIR $TMPDIR  -o /tmp/tmp.dmg
hdiutil convert /tmp/tmp.dmg -format UDZO -o MacVPNWatcher.dmg
rm -f /tmp/tmp.dmg
rm -rf $TMPDIR
