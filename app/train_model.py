import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# =========================
# DB Connection
# =========================
conn = psycopg2.connect(
    host="localhost",
    database="vulnsight",
    user="postgres",
    password="madrid77"
)

# =========================
# Load Data
# =========================
query = """
SELECT 
    duration,
    packet_per_sec,
    bytes_per_sec,
    avg_packet_size
FROM network_session
WHERE duration IS NOT NULL
"""

df = pd.read_sql(query, conn)

print("Data loaded:", df.shape)
print("Columns:", df.columns)

# =========================
# Better Label Creation (IMPORTANT)
# =========================

# هنستخدم أكتر من feature علشان يبقى realistic
df['label'] = (
    (df['packet_per_sec'] > df['packet_per_sec'].quantile(0.75)) |
    (df['bytes_per_sec'] > df['bytes_per_sec'].quantile(0.75))
).astype(int)

# نشوف توزيع البيانات
print("\nLabel distribution:")
print(df['label'].value_counts())

# =========================
# Features / Target
# =========================
X = df[['duration', 'packet_per_sec', 'bytes_per_sec', 'avg_packet_size']]
y = df['label']

# =========================
# Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# =========================
# Model
# =========================
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# Evaluation
# =========================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

# =========================
# Save Model
# =========================
joblib.dump(model, "model.pkl")

print("✅ Model saved as model.pkl")