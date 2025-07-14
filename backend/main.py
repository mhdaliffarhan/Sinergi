from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import database
import schemas

# Perintah ini akan membuat tabel di database jika belum ada
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Fungsi untuk mengelola sesi database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Selamat datang di API SINERGI BPS NTB"}

# Endpoint untuk mengambil semua data aktivitas
@app.get("/api/aktivitas")
def get_semua_aktivitas(db: Session = Depends(get_db)):
    semua_aktivitas = db.query(models.Aktivitas).all()
    return semua_aktivitas

# --- ENDPOINT MEMBUAT AKTIVITAS ---
@app.post("/api/aktivitas", response_model=schemas.Aktivitas)
def create_aktivitas(aktivitas: schemas.AktivitasCreate, db: Session = Depends(get_db)):
    # Buat objek SQLAlchemy dari data Pydantic
    db_aktivitas = models.Aktivitas(
        nama_aktivitas=aktivitas.nama_aktivitas,
        deskripsi=aktivitas.deskripsi,
        tim_penyelenggara=aktivitas.tim, # sesuaikan dengan nama field di form vue
        tanggal_mulai=aktivitas.tanggalMulai,
        tanggal_selesai=aktivitas.tanggalSelesai,
        jam_mulai=aktivitas.jamMulai,
        jam_selesai=aktivitas.jamSelesai
        # kita bisa tambahkan logika untuk tanggal tunggal vs rentang di sini nanti
    )
    db.add(db_aktivitas)
    db.commit()
    db.refresh(db_aktivitas)
    return db_aktivitas