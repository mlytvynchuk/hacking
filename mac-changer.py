import subprocess
import optparse

def change_mac(interface, new_mac):
    print("[+] Changing a MAC Address for " + interface + " to "+ new_mac)
    subprocess.call(["ifconfig",interface,"down" ])
    subprocess.call(['ifconfig', interface,'hw','ether', new_mac]) 
    subprocess.call(["ifconfig",interface,"up" ])

parser = optparse.OptionParser()
parser.add_option("-i", '--interface', dest='interface', help='Interface to change MAC Address')
parser.add_option('-m', '--mac', dest='new_mac', help='New MAC Address to change')

(options, arguments) = parser.parse_args()

change_mac(options.interface, options.new_mac)


