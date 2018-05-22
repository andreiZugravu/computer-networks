from scapy.all import *

eth = Ether(dst = "ff:ff:ff:ff:ff:ff")
arp = ARP(pdst = "198.13.13.0/16")
ans, unans = srp(eth / arp, timeout = 5)

if len(ans):
    print ans[0][1].pdst + " -- " + ans[0][1].hwdst

for answer in ans:
    print answer[1].psrc + " -- " + answer[1].hwsrc
