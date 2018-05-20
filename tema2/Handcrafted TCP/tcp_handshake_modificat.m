# inainte de toate trebuie adaugata o regula de ignorare 
# a pachetelor RST pe care ni le livreaza kernelul automat
# iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
from scapy.all import *
from struct import *

ip = IP()
ip.src = '198.13.0.15' # sursa - container md1
ip.dst = '198.13.0.14' # destinatia - container rt1
ip.tos = int('011110' + '11', 2) #setam DSCP cu cod AF32(binar) pt vs si ECN cu notif de congestie, from git !!

tcp = TCP()
tcp.sport = 7991 # un port la alegere
tcp.dport = 10000 # portul destinatie pe care ruleaza serverul

#setam MSS la 2

op_index = TCPOptions[1]['MSS']
op_format = TCPOptions[0][op_index]
valoare = struct.pack(op_format[1],2) # punem valoarea 2 in string de 2 bytes
tcp.options = [('MSS',valoare)] # setam [MSS,2]

tcp.seq = 100 # un sequence number la alegere
tcp.flags = 'S' #SYN - I want to SYNc

raspuns_SYN_ACK = sr1(ip/tcp) #SYN,ACK - I got it ACK, want to SYN also

tcp.seq += 1
tcp.ack = raspuns_SYN_ACK.seq + 1

tcp.flags = 'A' #ACK - Acknoledgement - Good, connection established
send(ip/tcp)

#CONNECTION ON

string = 'testabcd'
for i in range(0,3):
    tcp.flags = 'PAEC' #flagurile PSH, ACK, ECE, CWR
    tcp.ack = raspuns_SYN_ACK.seq + 1
    caracter = string[i]
    recv = sr1(ip/tcp/caracter)
    tcp.seq += 1

tcp.flags = 'R' # RST
send(ip/tcp)
