#UDP server
#sliding window
import socket
import logging

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 4000
adresa = '0.0.0.0'
server_address = (adresa, port)
sock.bind(server_address)
total = 1000;
receiving_window_start = 1
receiving_window_size = 10
received = 0
receiving_buffer = []
receiving_buffer_start = 0
for i in range(0, receiving_window_size):
    receiving_buffer.append(0)

while received < total:
    data, address = sock.recvfrom(4096)
    if data:
        nr = int(data);
        logging.info('received: %d', nr)
        if receiving_window_start <= nr and nr < receiving_window_start + receiving_window_size:
            receiving_buffer[(receiving_buffer_start + nr - receiving_window_start) % receiving_window_size] = 1;    
            while receiving_buffer[receiving_buffer_start] == 1 and received < total:
                receiving_buffer[receiving_buffer_start] = 0
                receiving_buffer_start = (receiving_buffer_start + 1) % receiving_window_size;
                received = received + 1;
                logging.info('processed: %d', receiving_window_start)
                sent = sock.sendto(str(receiving_window_start), address)
                if receiving_window_start < total:
                    receiving_window_start = receiving_window_start + 1;                 
                logging.info('new window: %d -> %d', receiving_window_start, min(total, receiving_window_start + receiving_window_size))                
