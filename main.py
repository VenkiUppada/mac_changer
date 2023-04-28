from ast import arguments
import subprocess as sb
import optparse as opp
import re
from click import option

from yaml import parse

def get_arg():# Parsers and ERROR messages
    parser = opp.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help=" Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help=" New mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        #code to handel error
        parser.error("[-] Please specify an interface, use --help for more info")
    elif not options.new_mac:
        #code to handel error
        parser.error("[-] Please specify a new mac, use --help for more info")
    return options

def change_mac(interface, new_mac): #Commands to change MAC address
    print("[+] Changing MAC address of " + interface + " to " + new_mac)
    sb.run(["ifconfig", interface, "down"])
    sb.run(["ifconfig", interface, "hw", "ether", new_mac])
    sb.run(["ifconfig", interface, "up"])

def get_mac(interface): #Checks and Prints the current MAC address of the interface
    ifcon_result = sb.check_output(["ifconfig", interface])
    mac_addr_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifcon_result))

    if mac_addr_search_result:
        return mac_addr_search_result.group(0)
    else:
        print("[-] Could not read MAC address")


options = get_arg()

getMAC = get_mac(options.interface)
print("Current MAC = " + str(getMAC))

change_mac(options.interface, options.new_mac)

getMAC = get_mac(options.interface)
if getMAC == get_mac(options.interface):
    print("[+] MAC address was successfully changed to " + getMAC)
else:
    print("[-] MAC address did not get changed")


