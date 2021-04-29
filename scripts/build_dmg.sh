#!/bin/bash

#set -x

TMPDIR=/tmp/MacVPNWatcher

rm -f MacVPNWatcher-*.dmg

pkg_version=$(plutil -p ../dist/MacVPNWatcher.app/Contents/Info.plist | grep "CFBundleShortVersionString.*$ApplicationVersionNumber" | grep -o '"[[:digit:].]*"' | sed s/\"//g)

dmg_file="MacVPNWatcher-${pkg_version}.dmg"

mkdir $TMPDIR
mkdir -p ../releases
cp -rvp ../dist/* $TMPDIR
#cp -rvp ../dmg_template/.[a-zA-Z]* $TMPDIR
cp -rvp ../dmg_template/.background $TMPDIR/.background
cp -rvp ../dmg_template/DS_Store $TMPDIR/.DS_Store
(cd $TMPDIR; ln -s /Applications .)
hdiutil makehybrid -hfs -hfs-volume-name MacVPNWatcher -hfs-openfolder $TMPDIR $TMPDIR  -o /tmp/tmp.dmg
hdiutil convert /tmp/tmp.dmg -format UDZO -o ${dmg_file}
rm -f /tmp/tmp.dmg
rm -rf $TMPDIR
cp ${dmg_file} ../releases
