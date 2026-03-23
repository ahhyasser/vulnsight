from app.database import SessionLocal
from app.models import PcapFile
from datetime import datetime
import uuid

# إنشاء Session
db = SessionLocal()

# إنشاء سجل جديد
pcap = PcapFile(
    id=str(uuid.uuid4()),
    filename="test_file.pcap",
    filepath="/files/test_file.pcap",
    file_size=123456,
    uploaded_at=datetime.now(),
    source="Python Test"
)

# حفظ في الداتا بيز
db.add(pcap)
db.commit()

print("Inserted successfully!")