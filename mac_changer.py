#!/usr/bin/env python3

import subprocess
import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface',
        help='Interface to change its MAC address.')
    parser.add_argument('-m', '--mac', dest='new_mac', help='New MAC address.')
    (arguments) = parser.parse_args()

    if not arguments.interface:
        parser.error('[-] Please specify an interface (-i, --interface).')
    elif not arguments.new_mac:
        parser.error('[-] Please specify a new MAC address (-m, --mac).')
    return arguments

def change_mac(interface, new_mac):
    print('[+] Changing MAC address for ' + interface + ' to ' + new_mac + '.')
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])

arguments = get_arguments()
# change_mac(arguments.interface, arguments.new_mac)

ifconfig_result = subprocess.check_output(['ifconfig', arguments.interface])
mac_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result.decode('utf-8'))

if mac_search_result:
    print(mac_search_result.group(0))
else:
    print('[-] Could not find a MAC address for ' + arguments.interface + '.')
