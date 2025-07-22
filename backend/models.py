from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Time, ForeignKey
from sqlalchemy.orm import relationship
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

    dokumen = relationship("Dokumen", back_populates="aktivitas", cascade="all, delete-orphan")

    # Relasi ke tabel daftar dokumen wajib
    daftar_dokumen_wajib = relationship("DaftarDokumen", back_populates="aktivitas", cascade="all, delete-orphan")

    # --- KELAS UNTUK TABEL DOKUMEN ---
class Dokumen(Base):
    __tablename__ = "dokumen"

    id = Column(Integer, primary_key=True, index=True)
    keterangan = Column(Text, nullable=False)
    tipe = Column(String(10), nullable=False)
    path_atau_url = Column(Text, nullable=False)
    nama_file_asli = Column(String, nullable=True)
    tipe_file_mime = Column(String, nullable=True)
    diunggah_pada = Column(TIMESTAMP(timezone=True), server_default='now()')
    
    # Kunci asing yang menghubungkan ke tabel aktivitas
    aktivitas_id = Column(Integer, ForeignKey("aktivitas.id"))

    # Tambahkan relasi ini untuk menghubungkan kembali ke Aktivitas
    aktivitas = relationship("Aktivitas", back_populates="dokumen")

class DaftarDokumen(Base):
    __tablename__ = "daftar_dokumen"

    id = Column(Integer, primary_key=True, index=True)
    nama_dokumen = Column(String, nullable=False)
    status = Column(String(50), nullable=False, default='Wajib Diunggah')
    dokumen_id = Column(Integer, ForeignKey("dokumen.id"), nullable=True)

    # Hubungkan kembali ke model Aktivitas
    aktivitas_id = Column(Integer, ForeignKey("aktivitas.id"))
    aktivitas = relationship("Aktivitas", back_populates="daftar_dokumen_wajib")
