#!/usr/local/bin/python3.8

import sys

import routeros_api
from routeros_api.exceptions import RouterOsApiCommunicationError


def get_interfaces():
    return router.get_resource('/interface/ethernet')


class FoundSFPInterfaceException(Exception):
    pass


def find_target_interface_by_mac(mac):
    ethernet_interfaces = get_interfaces()
    target_interface = ethernet_interfaces.get(mac_address=mac)[0]

    if "sfp" in target_interface['name']:
        raise FoundSFPInterfaceException("Interface is an SFP interface.")

    return target_interface


def set_disabled_by_interface_id(interface_id, value):
    ethernet_interfaces = get_interfaces()
    ethernet_interfaces.set(id=interface_id, disabled=value)


def set_poe_out_by_interface_id(interface_id, value):
    ethernet_interfaces = get_interfaces()
    ethernet_interfaces.set(id=interface_id, poe_out=value)




if __name__ == '__main__':
    try:
        global router = routeros_api.RouterOsApiPool('10.0.64.4', username='apiuser', password='apiuser',
                                              use_ssl=False, plaintext_login=True).get_api()
        mac = sys.argv[1]
        action = sys.argv[2]
        value = sys.argv[3]

        if action == 'disabled':
            target_interface = find_target_interface_by_mac(mac)
            print("Setting " + target_interface['name'] + "'s disabled value to " + value)
            set_disabled_by_interface_id(target_interface['id'], value)
        elif action == 'poe':
            target_interface = find_target_interface_by_mac(mac)
            print("Setting " + target_interface['name'] + "'s disabled value to " + value)
            set_poe_out_by_interface_id(target_interface['id'], value)

        exit(0)
    except IndexError:
        print("Cannot find target interface.")
        exit(1)
    except FoundSFPInterfaceException:
        print("Interface found was SFP, exiting.")
        exit(1)
    except RouterOsApiCommunicationError:
        print("Something went wrong talking to the router.")
        exit(1)
