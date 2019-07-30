import scapy.all sa scapy

def scan(ip):
    scapy.airping(ip)

scan("10.0.2.1")