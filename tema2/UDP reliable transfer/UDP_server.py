# UDP Server
import socket
import logging
from random import randint
import sys

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10009
adresa = 'localhost'
server_address = (adresa, port)
sock.bind(server_address)

total = 10000

wstart = 1
wend = 1000
wsize = wend;

received = [];
for i in range(0,wsize):
  received.append(0)

while True:
  data, address = sock.recvfrom(4096)
  if data:
    if data == "stop":
      break
    nr = int(data)
    if nr <= wend:
      sent = sock.sendto(data, address)     
    if wstart <= nr and nr <= wend:
      logging.info("received: %d", nr)
      received[(nr - 1) % wsize] = 1;     
      while received[(wstart - 1) % wsize] == 1:
        if wstart <= total:
          logging.info("processed: %d", wstart)
          received[(wstart - 1) % wsize] = 0
          wstart = wstart + 1;
          if wstart > total:
            try:
              data, address = sock.recvfrom(4096)
            except socket.timeout:
              sock.close();
              sys.exit(0);
        if wend < total:
          wend = wend + 1;
sock.close();