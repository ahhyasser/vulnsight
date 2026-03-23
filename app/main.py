from fastapi import FastAPI, Query, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.database import SessionLocal
from app.models import Packet, PcapFile

app = FastAPI()

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# Root
# =========================
@app.get("/")
def root():
    return {"message": "VulnSight API running 🚀"}


# =========================
# Get all PCAP files
# =========================
@app.get("/pcap")
def get_pcap_files(db: Session = Depends(get_db)):
    return db.query(PcapFile).all()


# =========================
# Get all packets
# =========================
@app.get("/packets")
def get_packets(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    packets = db.query(Packet).offset(offset).limit(limit).all()
    return packets


# =========================
# Filter packets
# =========================
@app.get("/packets/filter")
def filter_packets(
    src_ip: str = Query(None),
    dst_ip: str = Query(None),
    protocol: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Packet)

    if src_ip:
        query = query.filter(Packet.src_ip == src_ip)

    if dst_ip:
        query = query.filter(Packet.dst_ip == dst_ip)

    if protocol:
        query = query.filter(Packet.protocol == protocol)

    return query.all()


# =========================
# Packet statistics
# =========================
@app.get("/packets/stats")
def packet_stats(db: Session = Depends(get_db)):

    packets = db.query(Packet).all()

    stats = {}

    for pkt in packets:
        stats[pkt.src_ip] = stats.get(pkt.src_ip, 0) + 1

    return stats


# =========================
# Detect SYN Flood
# =========================
@app.get("/packets/detect")
def detect_attacks(db: Session = Depends(get_db)):

    packets = db.query(Packet).all()

    syn_count = {}

    for pkt in packets:
        if pkt.tcp_flags == "SYN":
            syn_count[pkt.src_ip] = syn_count.get(pkt.src_ip, 0) + 1

    suspicious = {ip: count for ip, count in syn_count.items() if count > 5}

    return {
        "suspicious_ips": suspicious,
        "message": "IPs with high SYN packets (possible SYN flood)"
    }


# =========================
# Upload PCAP
# =========================
@app.post("/upload")
def upload_pcap(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": file_path
    }