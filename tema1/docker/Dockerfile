FROM kalilinux/kali-linux-docker

MAINTAINER Sergiu Nisioi <sergiu.nisioi@fmi.unibuc.ro>

USER root

RUN apt-get update 
RUN apt-get install -y build-essential git net-tools arp-scan nmap rtpflood python python-pip tcpdump
RUN pip install scapy

RUN useradd -u 1000 -m rtuser

RUN mv /usr/sbin/tcpdump /usr/local/bin

ENV PATH="/usr/local/bin:${PATH}"

USER rtuser
WORKDIR /home/rtuser

USER root
