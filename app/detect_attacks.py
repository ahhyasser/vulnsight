import psycopg2
import pandas as pd
import joblib
from datetime import datetime

# تحميل الموديل
model = joblib.load("model.pkl")

# اتصال بالداتا بيز
conn = psycopg2.connect(
    host="localhost",
    database="vulnsight",
    user="postgres",
    password="madrid77"
)

cur = conn.cursor()


def detect_attacks():
    query = """
    SELECT id, duration, packet_per_sec, bytes_per_sec, avg_packet_size
    FROM network_session
    WHERE duration IS NOT NULL 
AND id NOT IN (SELECT session_id FROM alert);
    """

    df = pd.read_sql(query, conn)

    print(f"Sessions loaded: {len(df)}")

    if df.empty:
        print("No data found.")
        return

    # Features
    features = df[['duration', 'packet_per_sec', 'bytes_per_sec', 'avg_packet_size']]

    # Predictions + Probabilities
    predictions = model.predict(features)
    probabilities = model.predict_proba(features)

    alerts = []

    for i in range(len(df)):
        if predictions[i] == 1:
            confidence = float(max(probabilities[i]))

            alerts.append((
                datetime.now(),
                5,
                "ML Attack",
                confidence,
                "Detected by ML model",
                int(df.iloc[i]['id'])
            ))

    if alerts:
        cur.executemany("""
            INSERT INTO alert (
                timestamp,
                severity,
                label,
                confidence,
                description,
                session_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, alerts)

        conn.commit()

    print(f"🚨 Alerts created: {len(alerts)}")


if __name__ == "__main__":
    detect_attacks()