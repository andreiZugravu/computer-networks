eth = Ether(dst = "ff:ff:ff:ff:ff:ff") - Setup ethernet to broadcast

arp = ARP(pdst = "198.13.13.0/16") - ARP to the subnet address 

ans, unans = srp(eth / arp, timeout = 5) - send packages to all machines in the network awaiting for a response with a timeout of 5 milliseconds. Ans will hold answered requests and unans, unanswered requests.

print ans[0][1].pdst + " -- " + ans[0][1].hwdst - First, print the source machine IP and MAC address

for answer in ans:
    print answer[1].psrc + " -- " + answer[1].hwsrc - print all other IPs and Addreses gathered from machines who responded to our requests.
