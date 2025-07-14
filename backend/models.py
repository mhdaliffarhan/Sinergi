from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Time
from database import Base

class Aktivitas(Base):
    __tablename__ = "aktivitas"

    id = Column(Integer, primary_key=True, index=True)
    nama_aktivitas = Column(String, index=True)
    deskripsi = Column(Text, nullable=True)
    tim_penyelenggara = Column(String, index=True)
    tanggal_mulai = Column(TIMESTAMP, nullable=True)
    tanggal_selesai = Column(TIMESTAMP, nullable=True)
    jam_mulai = Column(Time, nullable=True)
    jam_selesai = Column(Time, nullable=True)
    dibuat_pada = Column(TIMESTAMP(timezone=True), server_default='now()')