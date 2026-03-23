from fastapi import FastAPI
import psycopg2
import pandas as pd
import joblib
from datetime import datetime

app = FastAPI()

# =============================
# DB Connection
# =============================
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="vulnsight",
        user="postgres",
        password="madrid77"
    )

# =============================
# Load ML Model
# =============================
model = joblib.load("model.pkl")

# =============================
# Home
# =============================
@app.get("/")
def home():
    return {"message": "VulnSight API is running 🔥"}

# =============================
# Get Alerts
# =============================
@app.get("/alerts")
def get_alerts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM alert ORDER BY timestamp DESC")
    rows = cur.fetchall()

    alerts = []
    for r in rows:
        alerts.append({
            "id": str(r[0]),
            "timestamp": str(r[1]),
            "severity": r[2],
            "label": r[3],
            "confidence": float(r[4]),
            "description": r[5],
            "session_id": str(r[6])
        })

    conn.close()
    return alerts

# =============================
# Run Detection (🔥 أهم Endpoint)
# =============================
@app.post("/run-detection")
def run_detection():
    conn = get_connection()

    query = """
    SELECT id, duration, packet_per_sec, bytes_per_sec, avg_packet_size
    FROM network_session
    WHERE duration IS NOT NULL
    """

    df = pd.read_sql(query, conn)

    if df.empty:
        return {"message": "No sessions found"}

    features = df[['duration', 'packet_per_sec', 'bytes_per_sec', 'avg_packet_size']]
    predictions = model.predict(features)

    cur = conn.cursor()
    alerts_created = 0

    for i, row in df.iterrows():
        if predictions[i] == 1:
            cur.execute("""
                INSERT INTO alert (
                    timestamp,
                    severity,
                    label,
                    confidence,
                    description,
                    session_id
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                datetime.now(),
                5,
                "ML Attack",
                0.95,
                "Detected by API",
                int(row['id'])
            ))
            alerts_created += 1

    conn.commit()
    conn.close()

    return {
        "message": "Detection completed",
        "alerts_created": alerts_created
    }