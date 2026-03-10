import socket
from datetime import datetime, timezone
import json


def listen_for_ping():
    # ustvarimo raw socket za ICMP promet (ping)
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    # neskončna zanka - program stalno posluša pakete
    while True:
        # počaka da pride paket, shrani ga v packet, addr so informacije o pošiljatelju
        packet, addr = sock.recvfrom(1024) # prebere max 1024B

        # ustvarimo zapis za log
        log_entry = {
            "time": datetime.now(timezone.utc).isoformat(),  # čas dogodka
            "event": "ICMP_PING",  # tip dogodka
            "src_ip": addr[0]  # IP naslov pošiljatelja
        }
        # zapis dodamo v log file
        with open("/app/logs/requests.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")