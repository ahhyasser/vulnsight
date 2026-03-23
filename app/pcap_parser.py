from scapy.all import rdpcap, IP, TCP, UDP
import psycopg2
from datetime import datetime

# اتصال بالداتابيز
conn = psycopg2.connect(
    dbname="vulnsight",
    user="postgres",
    password="madrid77",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def read_pcap(file_path):
    packets = rdpcap(file_path)

    print(f"Total packets: {len(packets)}")

    for pkt in packets:
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            protocol = "OTHER"
            src_port = None
            dst_port = None

            if TCP in pkt:
                protocol = "TCP"
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport

            elif UDP in pkt:
                protocol = "UDP"
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport

            packet_length = len(pkt)
            timestamp = datetime.now()

            # إدخال في DB
            cur.execute("""
                INSERT INTO packet 
                (timestamp, src_ip, dst_ip, src_port, dst_port, protocol, packet_length)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (timestamp, src_ip, dst_ip, src_port, dst_port, protocol, packet_length))

    conn.commit()
    print("✅ Packets inserted into database!")

if __name__ == "__main__":
    read_pcap("uploads/test.pcap")

    cur.close()
    conn.close()