# inainte de toate trebuie adaugata o regula de ignorare 
# a pachetelor RST pe care ni le livreaza kernelul automat
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
from scapy.all import *
from struct import *
import sys

ip = IP()
ip.src = '198.13.0.15' # sursa - container md1
ip.dst = '198.13.0.14' # destinatia - container rt1
ip.tos = int('011110' + '11', 2) #setam DSCP cu cod AF32(binar) pt vs si ECN cu notif de congestie
#DSCP && ECN

tcp = TCP()
tcp.sport = 7991 # un port la alegere
#tcp.dport = 10000 # portul destinatie pe care ruleaza serverul
tcp.dport = int(sys.argv[1])

#setam MSS la 2

op_index = TCPOptions[1]['MSS']
op_format = TCPOptions[0][op_index]
valoare = struct.pack(op_format[1],2) # punem valoarea 2 in string de 2 bytes
tcp.options = [('MSS',valoare)] # setam [MSS,2]

tcp.seq = 100 # un sequence number la alegere
tcp.flags = 'S' #SYN - I want to SYNc

raspuns_syn_ack = sr1(ip/tcp) #SYN,ACK - I got it ACK, want to SYN also

tcp.seq += 1
tcp.ack = raspuns_syn_ack.seq + 1

tcp.flags = 'A' #ACK - Acknoledgement - Good, connection established
ACK = ip / tcp
send(ACK)

#CONNECTION ON

for ch in "hey":
    tcp.flags = 'PAEC'
    tcp.ack = raspuns_syn_ack.seq + 1
    print "Am trimis: " + ch
    rcv = sr1(ip/tcp/ch)
    #rcv
    tcp.seq += 1
    #print "Am primit: " + rcv[0].content()

tcp.flags = 'R'
RES = ip/tcp
send(RES)
