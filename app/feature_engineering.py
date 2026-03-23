import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="vulnsight",
    user="postgres",
    password="madrid77"
)

cur = conn.cursor()

def generate_features():
    cur.execute("""
        SELECT id, start_time, end_time,
               total_packets, total_bytes
        FROM network_session
    """)

    sessions = cur.fetchall()

    print(f"Total sessions: {len(sessions)}")

    for s in sessions:
        session_id, start_time, end_time, packets, bytes_ = s

        # ✅ حل مشكلة None (دي كانت بتكسر الكود)
        if end_time is None or start_time is None:
            duration = 1
        else:
            duration = (end_time - start_time).total_seconds()

        if duration == 0:
            duration = 1

        # ✅ حساب الفيتشرز
        packet_per_sec = packets / duration
        bytes_per_sec = bytes_ / duration
        avg_packet_size = bytes_ / packets if packets != 0 else 0

        # ✅ تحديث الداتا
        cur.execute("""
            UPDATE network_session
            SET duration=%s,
                packet_per_sec=%s,
                bytes_per_sec=%s,
                avg_packet_size=%s
            WHERE id=%s
        """, (
            duration,
            packet_per_sec,
            bytes_per_sec,
            avg_packet_size,
            session_id
        ))

    conn.commit()
    print("✅ Features generated successfully!")

if __name__ == "__main__":
    generate_features()