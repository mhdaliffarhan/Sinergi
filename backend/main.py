from fastapi import FastAPI, Depends
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