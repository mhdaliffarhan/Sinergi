from fastapi import FastAPI, Depends, HTTPException, status, Response,  File, UploadFile, Form
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload  
from typing import List,  Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import uuid

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

UPLOAD_DIRECTORY = "./uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Hapus response_model_by_alias karena kita sudah menangani alias di skema
@app.get("/api/aktivitas", response_model=List[schemas.Aktivitas])
def get_semua_aktivitas(db: Session = Depends(get_db), q: Optional[str] = None):
    # Query dasar dengan eager loading dokumen
    query = db.query(models.Aktivitas).options(joinedload(models.Aktivitas.dokumen))

    # Jika ada parameter pencarian 'q'
    if q:
        search_term = f"%{q}%"
        # Lakukan join dengan tabel dokumen agar bisa mencari di sana
        query = query.outerjoin(models.Dokumen)
        # Filter berdasarkan beberapa kolom sekaligus
        query = query.filter(
            or_(
                models.Aktivitas.nama_aktivitas.ilike(search_term),
                models.Aktivitas.deskripsi.ilike(search_term),
                models.Aktivitas.tim_penyelenggara.ilike(search_term),
                models.Dokumen.keterangan.ilike(search_term),
                models.Dokumen.nama_file_asli.ilike(search_term)
            )
        ).distinct() # Gunakan distinct agar aktivitas tidak muncul berulang

    # Urutkan berdasarkan ID terbaru dan ambil semua hasilnya
    semua_aktivitas = query.order_by(models.Aktivitas.id.desc()).all()
    return semua_aktivitas

@app.post("/api/aktivitas", response_model=schemas.Aktivitas)
def create_aktivitas(aktivitas: schemas.AktivitasCreate, db: Session = Depends(get_db)):
    # 1. Buat objek utama Aktivitas, mapping dari camelCase ke snake_case
    # Kita belum menyimpannya, hanya membuat objeknya di Python
    db_aktivitas = models.Aktivitas(
        nama_aktivitas=aktivitas.namaAktivitas,
        deskripsi=aktivitas.deskripsi,
        tim_penyelenggara=aktivitas.timPenyelenggara,
        jam_mulai=aktivitas.jamMulai,
        jam_selesai=aktivitas.jamSelesai
    )

    # Logika untuk tanggal
    if aktivitas.useDateRange:
        db_aktivitas.tanggal_mulai = aktivitas.tanggalMulai
        db_aktivitas.tanggal_selesai = aktivitas.tanggalSelesai
    else:
        db_aktivitas.tanggal_mulai = aktivitas.tanggalMulai
    
    # 2. Loop melalui daftar nama dokumen dan tambahkan ke relasi
    for nama_dok in aktivitas.daftarDokumenWajib:
        if nama_dok: # Pastikan string tidak kosong
            db_daftar_dokumen = models.DaftarDokumen(nama_dokumen=nama_dok)
            # Hubungkan langsung ke objek aktivitas utama
            db_aktivitas.daftar_dokumen_wajib.append(db_daftar_dokumen)

    # 3. Simpan semuanya ke database dalam SATU KALI transaksi
    db.add(db_aktivitas)
    db.commit()
    db.refresh(db_aktivitas)
    
    return db_aktivitas

# --- ENDPOINT MENGAMBIL DETAIL AKTIVITAS ---
@app.get("/api/aktivitas/{aktivitas_id}", response_model=schemas.Aktivitas)
def get_aktivitas_by_id(aktivitas_id: int, db: Session = Depends(get_db)):
    # Query database untuk mencari aktivitas dengan ID yang sesuai
    db_aktivitas = db.query(models.Aktivitas).options(
        joinedload(models.Aktivitas.dokumen),
        joinedload(models.Aktivitas.daftar_dokumen_wajib)
    ).filter(models.Aktivitas.id == aktivitas_id).first()
    
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

# --- ENDPOINT MENGHAPUS AKTIVITAS ---
@app.delete("/api/aktivitas/{aktivitas_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aktivitas(aktivitas_id: int, db: Session = Depends(get_db)):
    # 1. Cari aktivitas yang akan dihapus
    aktivitas_query = db.query(models.Aktivitas).filter(models.Aktivitas.id == aktivitas_id)
    # Jika tidak ditemukan, kirim error 404
    if aktivitas_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aktivitas tidak ditemukan")
        
    # 2. Hapus data dari database
    aktivitas_query.delete(synchronize_session=False)
    
    # 3. Simpan perubahan
    db.commit()
    
    # 4. Kembalikan respons tanpa konten (standar untuk DELETE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- ENDPOINT UPLOAD DOKUMEN ---
@app.post("/api/aktivitas/{aktivitas_id}/dokumen", response_model=schemas.Dokumen)
def upload_dokumen_untuk_aktivitas(
    aktivitas_id: int,
    keterangan: str = Form(...),
    file: UploadFile = File(...), # Menerima file
    db: Session = Depends(get_db)
):
    # Cek dulu apakah aktivitasnya ada
    aktivitas = db.query(models.Aktivitas).filter(models.Aktivitas.id == aktivitas_id).first()
    if not aktivitas:
        raise HTTPException(status_code=404, detail="Aktivitas tidak ditemukan")

    # Buat nama file yang unik untuk menghindari duplikasi
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    # Simpan file ke server
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    finally:
        file.file.close()

    # Simpan informasi file ke database
    db_dokumen = models.Dokumen(
        aktivitas_id=aktivitas_id,
        keterangan=keterangan,
        tipe='FILE',
        path_atau_url=file_location,
        nama_file_asli=file.filename,
        tipe_file_mime=file.content_type
    )

    db.add(db_dokumen)
    db.commit()
    db.refresh(db_dokumen)
    
    return db_dokumen

# --- ENDPOIN MENGHAPUS DOKUMEN ---
@app.delete("/api/dokumen/{dokumen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dokumen(dokumen_id: int, db: Session = Depends(get_db)):
    
    # 1. Cari data dokumen di database
    db_dokumen = db.query(models.Dokumen).filter(models.Dokumen.id == dokumen_id).first()
    
    # Jika tidak ditemukan, kirim error 404
    if db_dokumen is None:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan")

    # 2. Hapus file fisik dari folder 'uploads' jika tipenya 'FILE'
    if db_dokumen.tipe == 'FILE':
        file_path = db_dokumen.path_atau_url
        if os.path.exists(file_path):
            os.remove(file_path)
            
    # 3. Hapus data dari database
    db.delete(db_dokumen)
    db.commit()
    
    # 4. Kembalikan respons tanpa konten
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- ENDPOINT MENAMBAHKAN LINK ---
@app.post("/api/aktivitas/{aktivitas_id}/link", response_model=schemas.Dokumen)
def add_link_untuk_aktivitas(


    aktivitas_id: int,
    link_data: schemas.DokumenCreate, # Kita akan gunakan kembali skema ini
    db: Session = Depends(get_db)
):
    # Cek dulu apakah aktivitasnya ada
    aktivitas = db.query(models.Aktivitas).filter(models.Aktivitas.id == aktivitas_id).first()
    if not aktivitas:
        raise HTTPException(status_code=404, detail="Aktivitas tidak ditemukan")

    # Buat entri dokumen baru dengan tipe 'LINK'
    db_dokumen = models.Dokumen(
        aktivitas_id=aktivitas_id,
        keterangan=link_data.keterangan,
        tipe='LINK',
        path_atau_url=link_data.pathAtauUrl # Kita asumsikan frontend mengirim URL di field ini
    )

    db.add(db_dokumen)
    db.commit()
    db.refresh(db_dokumen)
    
    return db_dokumen

#--- ENDPOINT MENGUNGGAH FILE KE CHECKLIST ---
@app.post("/api/checklist/{item_id}/upload", response_model=schemas.Dokumen)
def upload_for_checklist_item(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Cari item checklist di database
    db_checklist_item = db.query(models.DaftarDokumen).filter(models.DaftarDokumen.id == item_id).first()
    if not db_checklist_item:
        raise HTTPException(status_code=404, detail="Item checklist tidak ditemukan")

    # 2. Simpan file fisik (logika ini sama seperti sebelumnya)
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    finally:
        file.file.close()

    # 3. Buat entri baru di tabel 'dokumen'
    db_dokumen = models.Dokumen(
        aktivitas_id=db_checklist_item.aktivitas_id,
        keterangan=db_checklist_item.nama_dokumen, # Gunakan nama checklist sebagai keterangan default
        tipe='FILE',
        path_atau_url=file_location,
        nama_file_asli=file.filename,
        tipe_file_mime=file.content_type
    )
    db.add(db_dokumen)
    db.commit()
    db.refresh(db_dokumen)

    # 4. Perbarui item checklist dengan status baru dan ID dokumen
    db_checklist_item.status = 'Selesai'
    db_checklist_item.dokumen_id = db_dokumen.id
    db.commit()
    
    return db_dokumen