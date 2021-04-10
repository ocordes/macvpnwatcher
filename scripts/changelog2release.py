"""
changelog2release.py

reads a CHANGELOG.md and creates a Release file

"""

import sys, os

def get_releases(filename):
    releases = {}
    if os.access(filename, os.R_OK) == False:
        print(f'File {filename} cannot be opened!', file=sys.stderr)
        return releases
    with open(filename, 'r') as f:
        r = None
        version = None
        for line in f:
            line = line.strip()
            if line == '':
                continue
            if line.startswith('###'):
                if r:
                    # save the previous release
                    releases[version] = r
                version = line.split()[1]
                r = []
            else:
                if r is not None:
                    r.append(line)
        if r is not None:
            # save the last release
            releases[version] = r

    return releases
    

# main
if len(sys.argv) > 1:
    release = sys.argv[1]
else:
    release = None

if len(sys.argv) > 2:
    filename = sys.argv[2]
else:
    filename = 'CHANGELOG.md'

releases = get_releases(filename)
if releases:
    print('Valid releases found!', file=sys.stderr)
    if release is None:
        keys = sorted(releases.keys())
        release = keys[-1]

if release in releases.keys():
    for i in releases[release]:
        print(i)
