# =========================
# Imports
# =========================
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

# Base class
Base = declarative_base()


# =========================
# جدول ملفات PCAP
# =========================
class PcapFile(Base):
    __tablename__ = "pcap_file"

    id = Column(String, primary_key=True)

    filename = Column(String)      # اسم الملف
    filepath = Column(String)      # مكان الملف

    # ✅ لازم نفس أسماء الداتا بيز
    file_size = Column(Integer)
    uploaded_at = Column(DateTime)

    source = Column(String)        # مصدر الملف


# =========================
# جدول Sessions
# =========================
class NetworkSession(Base):
    __tablename__ = "network_session"

    id = Column(String, primary_key=True)

    src_ip = Column(String)
    dst_ip = Column(String)

    src_port = Column(Integer)
    dst_port = Column(Integer)

    protocol = Column(String)

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    # Foreign Key
    pcap_id = Column(String, ForeignKey("pcap_file.id"))


# =========================
# جدول Packets
# =========================
class Packet(Base):
    __tablename__ = "packet"

    id = Column(String, primary_key=True)

    timestamp = Column(DateTime)

    src_ip = Column(String)
    dst_ip = Column(String)

    src_port = Column(Integer)
    dst_port = Column(Integer)

    protocol = Column(String)

    # هنا التعديل
    packet_length = Column(Integer)

    tcp_flags = Column(String)

    pcap_id = Column(String, ForeignKey("pcap_file.id"))
    session_id = Column(String, ForeignKey("network_session.id"))