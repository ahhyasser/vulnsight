from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# غير الباسورد هنا 👇
DATABASE_URL = "postgresql://postgres:madrid77@localhost:5432/vulnsight"

# إنشاء connection بالداتابيز
engine = create_engine(DATABASE_URL)

# Session للتعامل مع DB
SessionLocal = sessionmaker(bind=engine)

# إنشاء الجداول (لو مش موجودة)
def init_db():
    Base.metadata.create_all(bind=engine)