FROM python:3.9-slim
RUN apt-get update && apt-get install -y iptables libnetfilter-queue-dev build-essential net-tools tcpdump iproute2
RUN pip install scapy NetfilterQueue
COPY . /app
WORKDIR /app