import psycopg2
from collections import defaultdict

conn = psycopg2.connect(
    dbname="vulnsight",
    user="postgres",
    password="madrid77",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def build_sessions():
    # نسحب packets من DB
    cur.execute("""
        SELECT src_ip, dst_ip, src_port, dst_port, protocol, packet_length
        FROM packet
    """)

    packets = cur.fetchall()

    print(f"Total packets fetched: {len(packets)}")

    sessions = defaultdict(lambda: {
        "total_packets": 0,
        "total_bytes": 0
    })

    # grouping
    for pkt in packets:
        key = (pkt[0], pkt[1], pkt[2], pkt[3], pkt[4])

        sessions[key]["total_packets"] += 1
        sessions[key]["total_bytes"] += pkt[5]

    print(f"Total sessions created: {len(sessions)}")

    # إدخال sessions في DB
    for key, data in sessions.items():
        src_ip, dst_ip, src_port, dst_port, protocol = key

        cur.execute("""
            INSERT INTO network_session
            (start_time, src_ip, dst_ip, src_port, dst_port, protocol, total_packets, total_bytes)
            VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s)
        """, (
            src_ip, dst_ip, src_port, dst_port,
            protocol, data["total_packets"], data["total_bytes"]
        ))

    conn.commit()
    print("✅ Sessions inserted successfully!")

if __name__ == "__main__":
    build_sessions()

    cur.close()
    conn.close()