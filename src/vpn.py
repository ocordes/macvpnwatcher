"""
src/vpn.py

written by: Oliver Cordes 2021-03-24
changed by: Oliver Cordes 2021-03-28
"""

import re
import subprocess

def execute_command(cmd):
    p = subprocess.Popen(cmd, shell=True, bufsize=-1, close_fds=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT)

    # read all lines and convert to utf-8 and split into lines
    return p.stdout.read().decode('utf-8').split('\n')


    

def list_of_vpn_connections():
    conns = {}
    result = execute_command('scutil --nc list')
    rex = re.compile(r'.*[(](?P<status>[a-zA-Z]+)[)].*[\"](?P<name>[a-zA-Z0-9_-]+)[\"].*(\[)(?P<type>[a-zA-Z0-9]+)(\])')
    for line in result:
        if line != '' and line[0] == '*':  # enabled connection
            m = rex.search(line)
            if m is not None:
                conns[m.group('name')] = m.groupdict()

    return conns


def status_vpn_connection(name):
    result = execute_command(f'scutil --nc status {name}')


def disconnect_vpn(name):
    result = execute_command(f'scutil --nc stop {name}')
    #print(result)


def connect_vpn(name):
    result = execute_command(f'scutil --nc start {name}')
    #print(result)



if __name__ == '__main__':
    print(list_of_vpn_connections())
    print('Done.')
