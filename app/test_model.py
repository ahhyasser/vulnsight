import joblib
import pandas as pd

# تحميل الموديل
model = joblib.load("model.pkl")

# session جديدة (تجربة)
data = {
    "duration": [10],
    "packet_per_sec": [20],  # عالي → attack
    "bytes_per_sec": [5000],
    "avg_packet_size": [250]
}

df = pd.DataFrame(data)

# prediction
prediction = model.predict(df)

if prediction[0] == 1:
    print("🚨 Attack Detected")
else:
    print("✅ Normal Traffic")