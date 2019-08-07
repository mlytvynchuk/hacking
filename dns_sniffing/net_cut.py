# to start doing dns sniff we should create a queue for packets to modify them
# write in terminal:
# iptables -I FORWARD -j NFQUEUE --queue-num 0

import netfilterqueue
import subprocess
import scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    print(scapy_packet.show())
    packet.accept()


subprocess.call(["iptables",'-I',"FORWARD","-j","NFQUEUE","--queue-num", "0"])
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
try:
    queue.run()
except KeyboardInterrupt:
    print("  Quiting...")
    subprocess.call(["iptables","--flush"])
