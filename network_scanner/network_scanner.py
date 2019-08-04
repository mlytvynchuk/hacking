
import scapy.all as scapy
import argparse


def print_client_list(clients_list):
    print("_________________________________________________________")
    print("IP\t\t\t\t\tMAC\n---------------------------------------------------------")
    if len(clients_list) > 0:
        for client in clients_list:
            print(client["ip"]+"\t\t\t\t"+client["mac"])
    else:
        print ("no mac address with this ip")
    print("---------------------------------------------------------")


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="client_ip", help="Client ip for getting mac address")
    options = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst = ip) # get an ip of our computer
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") # get a mac address of our computer
    arp_request_brodcast = broadcast/arp_request # arp_request + broadcast
    print ("Scanning...")
    answered_list = scapy.srp(arp_request_brodcast, timeout=1, verbose=False)[0]
    clients_list = []

    for el in answered_list:
        client_dict = {
            "ip": el[1].psrc,
            "mac": el[1].hwsrc
        }
        clients_list.append(client_dict)

    return clients_list


options = get_arguments()
client_ip = options.client_ip
if client_ip:
    scan_list = scan(client_ip)
    print_client_list(scan_list)
else:
    print("[-] Write --help to watch instructions")
