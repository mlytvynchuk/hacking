import scapy.all as scapy
import os
def scan(ip):
    arp_request = scapy.ARP(pdst = ip) # get an ip of our computer
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") # get a mac address of our computer
    arp_request_brodcast = broadcast/arp_request # arp_request + broadcast
    answered, unanswered = scapy.srp(arp_request_brodcast, timeout=1)
    print(answered.summary())

scan("10.0.2.1/24")