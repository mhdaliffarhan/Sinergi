from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import models
import database
import schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# ... (kode CORS tidak berubah)
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Hapus response_model_by_alias karena kita sudah menangani alias di skema
@app.get("/api/aktivitas", response_model=List[schemas.Aktivitas])
def get_semua_aktivitas(db: Session = Depends(get_db)):
    semua_aktivitas = db.query(models.Aktivitas).order_by(models.Aktivitas.id.desc()).all()
    return semua_aktivitas

@app.post("/api/aktivitas", response_model=schemas.Aktivitas)
def create_aktivitas(aktivitas: schemas.AktivitasCreate, db: Session = Depends(get_db)):
    # Buat dictionary baru untuk memastikan pemetaan yang benar
    # dari camelCase (Pydantic) ke snake_case (SQLAlchemy)
    aktivitas_data_for_db = {
        "nama_aktivitas": aktivitas.namaAktivitas,
        "deskripsi": aktivitas.deskripsi,
        "tim_penyelenggara": aktivitas.timPenyelenggara,
        "tanggal_mulai": aktivitas.tanggalMulai,
        "tanggal_selesai": aktivitas.tanggalSelesai,
        "jam_mulai": aktivitas.jamMulai,
        "jam_selesai": aktivitas.jamSelesai,
    }

    # Buat objek database dari dictionary di atas
    db_aktivitas = models.Aktivitas(**aktivitas_data_for_db)
    
    db.add(db_aktivitas)
    db.commit()
    db.refresh(db_aktivitas)
    return db_aktivitas

# --- ENDPOINT MENGAMBIL DETAIL AKTIVITAS ---
@app.get("/api/aktivitas/{aktivitas_id}", response_model=schemas.Aktivitas)
def get_aktivitas_by_id(aktivitas_id: int, db: Session = Depends(get_db)):
    # Query database untuk mencari aktivitas dengan ID yang sesuai
    db_aktivitas = db.query(models.Aktivitas).filter(models.Aktivitas.id == aktivitas_id).first()
    
    # Jika aktivitas tidak ditemukan, kirim error 404
    if db_aktivitas is None:
        raise HTTPException(status_code=404, detail="Aktivitas tidak ditemukan")
        
    # Jika ditemukan, kembalikan datanya
    return db_aktivitas

# --- ENDPOINT MENGUPDATE AKTIVITAS ---
@app.put("/api/aktivitas/{aktivitas_id}", response_model=schemas.Aktivitas)
def update_aktivitas(aktivitas_id: int, aktivitas: schemas.AktivitasCreate, db: Session = Depends(get_db)):
    db_aktivitas = db.query(models.Aktivitas).filter(models.Aktivitas.id == aktivitas_id).first()

    if db_aktivitas is None:
        raise HTTPException(status_code=404, detail="Aktivitas tidak ditemukan")

    # Perbarui field satu per satu secara eksplisit
    db_aktivitas.nama_aktivitas = aktivitas.namaAktivitas
    db_aktivitas.deskripsi = aktivitas.deskripsi
    db_aktivitas.tim_penyelenggara = aktivitas.timPenyelenggara
    
    # Logika untuk tanggal
    if aktivitas.useDateRange:
        db_aktivitas.tanggal_mulai = aktivitas.tanggalMulai
        db_aktivitas.tanggal_selesai = aktivitas.tanggalSelesai
    else:
        db_aktivitas.tanggal_mulai = aktivitas.tanggalMulai
        db_aktivitas.tanggal_selesai = None

    # Logika untuk jam
    if aktivitas.useTime:
        db_aktivitas.jam_mulai = aktivitas.jamMulai
        db_aktivitas.jam_selesai = aktivitas.jamSelesai
    else:
        db_aktivitas.jam_mulai = None
        db_aktivitas.jam_selesai = None
        
    db.commit()
    db.refresh(db_aktivitas)
    return db_aktivitas