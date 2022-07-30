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


def get_current_mac(interface, new_mac):
    ifconfig_result = subprocess.check_output(
        ['ifconfig', interface])
    mac_search_result = re.search(
        r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', str(ifconfig_result))
    if mac_search_result:
        return mac_search_result.group(0)
    return '[-] Could not find a MAC address for ' + interface + '.'


arguments = get_arguments()
change_mac(arguments.interface, arguments.new_mac)
current_mac = get_current_mac(arguments.interface, arguments.new_mac)

if (current_mac == arguments.new_mac):
    print('[+] MAC successfully changed to ' + arguments.new_mac)
else:
    print('[-] MAC address was *not* changed!')
