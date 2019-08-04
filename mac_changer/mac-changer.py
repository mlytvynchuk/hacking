import subprocess
import optparse
import re


def get_current_mac(interface):
    ifconfig_result = ""
    try:
        ifconfig_result = subprocess.check_output(['ifconfig', interface])
        mac_address = re.search(
            r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)
        if mac_address:
            return mac_address.group(0)
        else:
            print("[-] Could not read mac address ")
    except:
        pass


def get_options():
    parser = optparse.OptionParser()
    parser.add_option("-i", '--interface', dest='interface',
                      help='Interface to change MAC Address')
    parser.add_option('-m', '--mac', dest='new_mac',
                      help='New MAC Address to change')
    (options, arguments) = parser.parse_args()
    return options


def change_mac(interface, new_mac):
    if(options.interface and options.new_mac):
        print("[......] Changing a MAC Address for " +
              interface + " to " + new_mac)
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
        subprocess.call(["ifconfig", interface, "up"])

    elif options.interface:
        print ("[-] Try to do it again, you forget to add new mac address. The right example: -i <your interface> -m <your new mac>")
    elif options.new_mac:
        print ("[-] Try to do it again, you forget to add your interface. The right example: -i <your interface> -m <your new mac>")
    else:
        print ("[-] Try it again, you forget to add an interface and a mac adress. The right example: -i <your interface> -m <your new mac>")


options = get_options()
current_mac = get_current_mac(options.interface)
if current_mac:
    change_mac(options.interface, options.new_mac)
    current_mac = get_current_mac(options.interface)
    if current_mac == options.new_mac:
        print("[+] Mac Address was saccuessfully changed to " + current_mac)
    else:
        print("[-] Mac Address was not changed")
