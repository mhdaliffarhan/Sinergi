from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Time, ForeignKey, Table, Boolean, DATE
from sqlalchemy.orm import relationship
from database import Base

user_team_link = Table('user_team_link', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True)
)

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
    aktivitas_id = Column(Integer, ForeignKey("aktivitas.id"))
    aktivitas = relationship("Aktivitas", back_populates="dokumen")

class DaftarDokumen(Base):
    __tablename__ = "daftar_dokumen"
    id = Column(Integer, primary_key=True, index=True)
    nama_dokumen = Column(String, nullable=False)
    status = Column(String(50), nullable=False, default='Wajib Diunggah')
    dokumen_id = Column(Integer, ForeignKey("dokumen.id"), nullable=True)
    aktivitas_id = Column(Integer, ForeignKey("aktivitas.id"))
    aktivitas = relationship("Aktivitas", back_populates="daftar_dokumen_wajib")
    dokumen_terkait = relationship("Dokumen")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    nama_lengkap = Column(String)
    is_active = Column(Boolean, default=True)
    sistem_role_id = Column(Integer, ForeignKey("sistem_roles.id"))
    jabatan_id = Column(Integer, ForeignKey("jabatan.id"))
    sistem_role = relationship("SistemRole")
    jabatan = relationship("Jabatan")
    teams = relationship("Team", secondary=user_team_link, back_populates="users")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    nama_tim = Column(String, unique=False, index=True)
    valid_from = Column(DATE, nullable=True)
    valid_until = Column(DATE, nullable=True)
    ketua_tim_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ketua_tim = relationship("User", foreign_keys=[ketua_tim_id])
    users = relationship("User", secondary=user_team_link, back_populates="teams")

class SistemRole(Base):
    __tablename__ = "sistem_roles"
    id = Column(Integer, primary_key=True)
    nama_role = Column(String, unique=True, nullable=False)

class Jabatan(Base):
    __tablename__ = "jabatan"
    id = Column(Integer, primary_key=True)
    nama_jabatan = Column(String, unique=True, nullable=False)
