# UDP client
import socket
import logging
import sys
from random import randint
logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(.1);
port = 10009
adresa = 'localhost'
server_address = (adresa, port)
to_send = 1
total = 10000

wstart = 1
wend = 1000
wsize = wend
confirmed = [];
for i in range(0,wsize):
    confirmed.append(0)
    
while to_send <= total:
    try:
        while True:
            data, server = sock.recvfrom(4096)
            nr = int(data)
            if wstart <= nr and nr <= wend:
                break
        confirmed[(nr - 1) % wsize] = 1;
        while confirmed[(wstart - 1) % wsize] == 1:
            if wstart <= total:
                logging.info("confirmed: %d", wstart)
                confirmed[(wstart - 1) % wsize] = 0
                wstart = wstart + 1;
                to_send = to_send + 1;
            if wend < total:
                wend = wend + 1;            
    except socket.timeout:
        for i in range(wstart, wend + 1):
            if confirmed[(i - 1) % wsize] == 0:
                sent = sock.sendto(str(i), server_address)
                logging.info("(re)sent: " + str(i))  


sent = sock.sendto("stop", server_address)
sent = sock.sendto("stop", server_address)
sent = sock.sendto("stop", server_address)        