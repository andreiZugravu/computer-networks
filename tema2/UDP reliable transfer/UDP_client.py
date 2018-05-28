#UDP client
#sliding window
import socket
import logging
import sys
import time
#logging.info('Content primit: "%s"', data)
logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 4000
adresa = '172.111.0.2' #server IP
server_address = (adresa, port)

sending_window_start = 1
sending_window_size = 10
confirmed = 0
sending_buffer = []
time_buffer = []
expiring_time = 1;
sending_buffer_start = 0
for i in range(0, sending_window_size):
    sending_buffer.append(0)
for i in range(1, sending_window_size):
    mesaj = str(i + 1);
    logging.info('sent: %s', mesaj)
    sent = sock.sendto(mesaj, server_address)
    time_buffer.append(time.time());
    
mesaj = str(1);
logging.info('sent: %s', mesaj)
sent = sock.sendto(mesaj, server_address)
time_buffer.append(time.time());

total = 1000
while confirmed < total: 
    try:
        data, server = sock.recvfrom(4096)
        nr = int(data)
        if sending_window_start <= nr and nr < sending_window_start+sending_window_size:
            sending_buffer[(sending_buffer_start + nr - sending_window_start) % sending_window_size] = 1;
            if sending_buffer[sending_buffer_start] == 0 and time.time() - time_buffer[sending_buffer_start] > expiring_time:
                mesaj = str(sending_window_start + sending_window_size - 1)
                sent = sock.sendto(mesaj, server_address)                
            while sending_buffer[sending_buffer_start] == 1 and confirmed < total:
                sending_buffer[sending_buffer_start] = 0
                sending_buffer_start = (sending_buffer_start + 1) % sending_window_size;
                confirmed = confirmed + 1
                logging.info('confirmed: %d', sending_window_start)
                if sending_window_start < total:
                    sending_window_start = sending_window_start + 1;                 
                logging.info('new window: %d -> %d', sending_window_start, min(total, sending_window_start + sending_window_size))                
                if sending_window_start + sending_window_size - 1<= total:
                    mesaj = str(sending_window_start + sending_window_size - 1)
                    sent = sock.sendto(mesaj, server_address)
                    logging.info('sent: %d', sending_window_start + sending_window_size - 1)               
                
    finally:
        confirmed
sock.close()