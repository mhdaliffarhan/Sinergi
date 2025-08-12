
from fastapi import (FastAPI, Depends, HTTPException, status, Response, File,
                     UploadFile, Form)
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload  
from typing import List,  Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import timedelta

import models, database, schemas, security
import os, shutil, uuid, io, zipfile

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIRECTORY = "./uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# --- OTENTIKASI & USER ---
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = security.get_user(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username atau password salah")
    
    token = security.create_access_token(data={"sub": user.username})
    content = {"accessToken": token, "tokenType": "bearer"}
    return JSONResponse(content=content)

@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    return current_user

# --- MANAJEMEN ADMIN ---
@app.post("/api/users", response_model=schemas.User, response_model_by_alias=True, dependencies=[Depends(security.require_role(["Superadmin"]))])
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Membuat pengguna baru (hanya Superadmin)."""
    db_user = security.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username sudah terdaftar")
    
    hashed_password = security.get_password_hash(user.password)
    
    # --- PERBAIKAN DI SINI ---
    # Saat membuat objek database (models.User), kita harus mengambil data dari
    # atribut snake_case yang ada di objek Pydantic 'user'.
    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        nama_lengkap=user.nama_lengkap,      # Gunakan user.nama_lengkap (snake_case)
        sistem_role_id=user.sistem_role_id, # Gunakan user.sistem_role_id (snake_case)
        jabatan_id=user.jabatan_id          # Gunakan user.jabatan_id (snake_case)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/api/users", response_model=List[schemas.User], dependencies=[Depends(security.require_role(["Superadmin", "Admin"]))])
def get_all_users(db: Session = Depends(database.get_db)):
    """Mengambil daftar semua pengguna (Admin dan Superadmin)."""
    # 1. Ambil semua data pengguna dari database
    users_db = db.query(models.User).all()
    
    # 2. Siapkan list kosong untuk menampung hasil
    response_data = []

    # 3. Loop melalui setiap pengguna dan buat dictionary manual dengan camelCase
    for user in users_db:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "namaLengkap": user.nama_lengkap,
            "isActive": user.is_active,
            "sistemRole": {
                "id": user.sistem_role.id,
                "namaRole": user.sistem_role.nama_role
            } if user.sistem_role else None,
            "jabatan": {
                "id": user.jabatan.id,
                "namaJabatan": user.jabatan.nama_jabatan
            } if user.jabatan else None,
            "teams": [{"id": team.id, "namaTim": team.nama_tim} for team in user.teams]
        }
        response_data.append(user_dict)
    
    # 4. Kembalikan data sebagai JSONResponse untuk kontrol penuh
    return JSONResponse(content=response_data)

@app.put("/api/users/{user_id}", response_model=schemas.User, response_model_by_alias=True, dependencies=[Depends(security.require_role(["Superadmin"]))])
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    """Memperbarui data pengguna (hanya Superadmin)."""
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    
    # Ambil data yang dikirim sebagai dictionary snake_case, abaikan field yang kosong (None)
    update_data = user_update.dict(exclude_unset=True)

    # Perbarui setiap field di objek database
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # Simpan perubahan
    db.commit()
    db.refresh(db_user)
    
    return db_user

# --- ENDPOINT BARU UNTUK MENGHAPUS USER ---
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.require_role(["Superadmin"]))])
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    """Menghapus pengguna berdasarkan ID (hanya Superadmin)."""
    
    # Cari pengguna di database
    user_query = db.query(models.User).filter(models.User.id == user_id)
    db_user = user_query.first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
        
    # Hapus pengguna
    user_query.delete(synchronize_session=False)
    db.commit()
    
    # Kembalikan respons tanpa konten
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/api/teams", response_model=List[schemas.Team], dependencies=[Depends(security.require_role(["Superadmin", "Admin"]))])
def get_all_teams(db: Session = Depends(database.get_db)):
    teams_db = db.query(models.Team).all()
    response_data = [schemas.Team.from_orm(team) for team in teams_db]
    return response_data

@app.post("/api/teams", response_model=schemas.Team, response_model_by_alias=True, dependencies=[Depends(security.require_role(["Superadmin"]))])
def create_team(team: schemas.TeamCreate, db: Session = Depends(database.get_db)):
    """Membuat tim baru (hanya Superadmin)."""
    team_data = team.dict(by_alias=False)
    db_team = models.Team(**team_data)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

# --- ENDPOINT BARU UNTUK UPDATE TIM ---
@app.put("/api/teams/{team_id}", response_model=schemas.Team, response_model_by_alias=True, dependencies=[Depends(security.require_role(["Superadmin"]))])
def update_team(team_id: int, team_update: schemas.TeamUpdate, db: Session = Depends(database.get_db)):
    """Memperbarui nama tim (hanya Superadmin)."""
    
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Tim tidak ditemukan")
    
    # Ambil data dari Pydantic dan perbarui model
    update_data = team_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_team, key, value)
        
    db.commit()
    db.refresh(db_team)
    return db_team

# --- ENDPOINT BARU UNTUK HAPUS TIM ---
@app.delete("/api/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security.require_role(["Superadmin"]))])
def delete_team(team_id: int, db: Session = Depends(database.get_db)):
    """Menghapus tim (hanya Superadmin)."""
    
    team_query = db.query(models.Team).filter(models.Team.id == team_id)
    db_team = team_query.first()

    if db_team is None:
        raise HTTPException(status_code=404, detail="Tim tidak ditemukan")
        
    team_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/api/sistem-roles", response_model=List[schemas.SistemRole])
def get_all_sistem_roles(db: Session = Depends(database.get_db)):
    """Mengembalikan semua peran sistem yang tersedia."""
    roles_db = db.query(models.SistemRole).all()
    # Konversi manual
    return [schemas.SistemRole.from_orm(role) for role in roles_db]

@app.get("/api/jabatan", response_model=List[schemas.Jabatan])
def get_all_jabatan(db: Session = Depends(database.get_db)):
    """Mengembalikan semua jabatan yang tersedia."""
    jabatan_db = db.query(models.Jabatan).all()
    # Konversi manual
    return [schemas.Jabatan.from_orm(j) for j in jabatan_db]

# Hapus response_model_by_alias karena kita sudah menangani alias di skema
@app.get("/api/aktivitas", response_model=List[schemas.Aktivitas])
def get_semua_aktivitas(db: Session = Depends(database.get_db), q: Optional[str] = None):
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
def create_aktivitas(aktivitas: schemas.AktivitasCreate, db: Session = Depends(database.get_db)):   
    db_aktivitas = models.Aktivitas(
        nama_aktivitas=aktivitas.nama_aktivitas,
        deskripsi=aktivitas.deskripsi,
        tim_penyelenggara=aktivitas.tim_penyelenggara,
        jam_mulai=aktivitas.jam_mulai,
        jam_selesai=aktivitas.jam_selesai
    )

    if aktivitas.use_date_range:
        db_aktivitas.tanggal_mulai = aktivitas.tanggal_mulai
        db_aktivitas.tanggal_selesai = aktivitas.tanggal_selesai
    else:
        db_aktivitas.tanggal_mulai = aktivitas.tanggal_mulai
    
    for nama_dok in aktivitas.daftar_dokumen_wajib:
        if nama_dok:
            db_daftar_dokumen = models.DaftarDokumen(nama_dokumen=nama_dok)
            db_aktivitas.daftar_dokumen_wajib.append(db_daftar_dokumen)

    db.add(db_aktivitas)
    db.commit()
    db.refresh(db_aktivitas)
    
    return db_aktivitas

# --- ENDPOINT MENGAMBIL DETAIL AKTIVITAS ---
@app.get("/api/aktivitas/{aktivitas_id}", response_model=schemas.Aktivitas)
def get_aktivitas_by_id(aktivitas_id: int, db: Session = Depends(database.get_db)):
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
def update_aktivitas(
    aktivitas_id: int, 
    aktivitas: schemas.AktivitasCreate, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(security.get_current_user)
):
    """Memperbarui aktivitas yang ada beserta checklist-nya."""
    db_aktivitas = db.query(models.Aktivitas).options(
        joinedload(models.Aktivitas.daftar_dokumen_wajib)
    ).filter(models.Aktivitas.id == aktivitas_id).first()
    if db_aktivitas is None:
        raise HTTPException(status_code=404, detail="Aktivitas tidak ditemukan")

    # Ambil semua data dari Pydantic model sebagai dictionary snake_case
    update_data = aktivitas.dict(exclude_unset=True)
    
    # Hapus field yang tidak ada di model Aktivitas
    update_data.pop('daftar_dokumen_wajib', None)
    update_data.pop('use_date_range', None)
    update_data.pop('use_time', None)
    
    # Update field-field utama
    for key, value in update_data.items():
        setattr(db_aktivitas, key, value)

    # Logika khusus untuk tanggal selesai jika tidak menggunakan rentang
    if not aktivitas.use_date_range:
        db_aktivitas.tanggal_selesai = None

    # Logika khusus untuk jam jika tidak digunakan
    if not aktivitas.use_time:
        db_aktivitas.jam_mulai = None
        db_aktivitas.jam_selesai = None

    # Logika untuk update checklist (sudah benar)
    existing_doc_names = {doc.nama_dokumen for doc in db_aktivitas.daftar_dokumen_wajib}
    incoming_doc_names = set(aktivitas.daftar_dokumen_wajib)
    
    docs_to_delete = [doc for doc in db_aktivitas.daftar_dokumen_wajib if doc.nama_dokumen not in incoming_doc_names]
    for doc in docs_to_delete:
        db.delete(doc)

    docs_to_add = incoming_doc_names - existing_doc_names
    for doc_name in docs_to_add:
        new_doc = models.DaftarDokumen(nama_dokumen=doc_name, aktivitas_id=aktivitas_id)
        db.add(new_doc)
        
    db.commit()
    db.refresh(db_aktivitas)
    return db_aktivitas

# --- ENDPOINT MENGHAPUS AKTIVITAS ---
@app.delete("/api/aktivitas/{aktivitas_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aktivitas(aktivitas_id: int, db: Session = Depends(database.get_db)):
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
def create_dokumen_untuk_aktivitas(
    aktivitas_id: int,
    keterangan: str = Form(...),
    checklist_item_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
    ):
    # Cek aktivitas (tidak berubah)
    aktivitas = db.query(models.Aktivitas).filter(models.Aktivitas.id == aktivitas_id).first()
    if not aktivitas:
        raise HTTPException(status_code=404, detail="Aktivitas tidak ditemukan")

    # Simpan file fisik (tidak berubah)
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    finally:
        file.file.close()

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
    db.refresh(db_dokumen) # Refresh untuk memastikan db_dokumen.id sudah ada

    # 2. JIKA ada checklist_item_id, BARU perbarui item checklist
    if checklist_item_id:
        db_checklist_item = db.query(models.DaftarDokumen).filter(models.DaftarDokumen.id == checklist_item_id).first()
        if db_checklist_item:
            db_checklist_item.status = 'Selesai'
            # Sekarang kita bisa pastikan db_dokumen.id sudah memiliki nilai
            db_checklist_item.dokumen_id = db_dokumen.id
            db.commit() # Commit perubahan pada item checklist
    
    return db_dokumen

# --- ENDPOINT MENAMBAHKAN LINK ---
@app.post("/api/aktivitas/{aktivitas_id}/link", response_model=schemas.Dokumen)
def add_link_untuk_aktivitas(


    aktivitas_id: int,
    link_data: schemas.DokumenCreate, # Kita akan gunakan kembali skema ini
    db: Session = Depends(database.get_db)
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

# --- ENDPOINT BARU UNTUK MENGGANTI FILE DI CHECKLIST ---
@app.post("/api/checklist/{item_id}/replace", response_model=schemas.Dokumen)
def replace_checklist_dokumen(
    item_id: int,
    old_file_action: str = Form(...), # Menerima 'hapus' atau 'unlink'
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    # 1. Cari item checklist yang akan diupdate
    db_checklist_item = db.query(models.DaftarDokumen).filter(models.DaftarDokumen.id == item_id).first()
    if not db_checklist_item:
        raise HTTPException(status_code=404, detail="Item checklist tidak ditemukan")

    # Simpan ID dokumen lama sebelum diubah
    old_dokumen_id = db_checklist_item.dokumen_id

    # 2. Simpan file baru dan buat entri dokumen baru (logika sama seperti upload)
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_location = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    finally:
        file.file.close()
    
    new_db_dokumen = models.Dokumen(
        aktivitas_id=db_checklist_item.aktivitas_id,
        keterangan=db_checklist_item.nama_dokumen,
        tipe='FILE',
        path_atau_url=file_location,
        nama_file_asli=file.filename,
        tipe_file_mime=file.content_type
    )
    db.add(new_db_dokumen)
    db.flush() # Gunakan flush untuk mendapatkan ID dari dokumen baru

    # 3. Update item checklist untuk menunjuk ke dokumen baru
    db_checklist_item.dokumen_id = new_db_dokumen.id

    # 4. Proses dokumen lama berdasarkan aksi yang dipilih
    if old_dokumen_id and old_file_action == 'hapus':
        old_db_dokumen = db.query(models.Dokumen).filter(models.Dokumen.id == old_dokumen_id).first()
        if old_db_dokumen:
            # Hapus file fisik
            if os.path.exists(old_db_dokumen.path_atau_url):
                os.remove(old_db_dokumen.path_atau_url)
            # Hapus catatan dari database
            db.delete(old_db_dokumen)
    
    # 5. Commit semua perubahan
    db.commit()
    db.refresh(new_db_dokumen)
    
    return new_db_dokumen

# --- ENDPOIN MENGHAPUS DOKUMEN ---
@app.delete("/api/dokumen/{dokumen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dokumen(dokumen_id: int, db: Session = Depends(database.get_db)):
    db_dokumen = db.query(models.Dokumen).filter(models.Dokumen.id == dokumen_id).first()
    
    if db_dokumen is None:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan")

    # --- LOGIKA BARU: PERBARUI CHECKLIST ---
    db_checklist_item = db.query(models.DaftarDokumen).filter(models.DaftarDokumen.dokumen_id == dokumen_id).first()
    
    # 3. Jika ada, reset status dan tautannya
    if db_checklist_item:
        db_checklist_item.status = 'Wajib Diunggah'
        db_checklist_item.dokumen_id = None
        
    # 4. Hapus file fisik dari folder 'uploads' jika tipenya 'FILE'
    if db_dokumen.tipe == 'FILE':
        file_path = db_dokumen.path_atau_url
        if os.path.exists(file_path):
            os.remove(file_path)
            
    # 5. Hapus data dari tabel 'dokumen'
    db.delete(db_dokumen)
    
    # 6. Simpan semua perubahan (update checklist dan delete dokumen)
    db.commit()
    
    # 4. Kembalikan respons tanpa konten
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- ENDPOINT BARU UNTUK UNDUH/PREVIEW DOKUMEN ---
@app.get("/api/dokumen/{dokumen_id}/download")
def download_dokumen(
    dokumen_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Mengirim file ke pengguna dengan nama file aslinya dan menyarankan preview.
    """
    db_dokumen = db.query(models.Dokumen).filter(models.Dokumen.id == dokumen_id).first()

    if db_dokumen is None or db_dokumen.tipe != 'FILE' or not os.path.exists(db_dokumen.path_atau_url):
        raise HTTPException(status_code=404, detail="File tidak ditemukan")

    # --- PERBAIKAN DI SINI ---
    # Atur header Content-Disposition secara manual untuk 'inline'
    headers = {
        'Content-Disposition': f'inline; filename="{db_dokumen.nama_file_asli}"'
    }
    
    # Kirim file sebagai respons dengan header yang sudah diatur
    return FileResponse(
        path=db_dokumen.path_atau_url,
        media_type=db_dokumen.tipe_file_mime,
        headers=headers
    )

# --- ENDPOINTUNTUK UNDUH SEMUA DOKUMEN DALAM SATU AKTIVITAS ---
@app.get("/api/aktivitas/{aktivitas_id}/download-all")
def download_all_dokumen(
    aktivitas_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Mengunduh semua dokumen bertipe FILE dari sebuah aktivitas dalam bentuk .zip.
    """
    db_aktivitas = db.query(models.Aktivitas).options(
        joinedload(models.Aktivitas.dokumen)
    ).filter(models.Aktivitas.id == aktivitas_id).first()

    if not db_aktivitas:
        raise HTTPException(status_code=404, detail="Aktivitas tidak ditemukan")

    files_to_zip = [doc for doc in db_aktivitas.dokumen if doc.tipe == 'FILE' and os.path.exists(doc.path_atau_url)]

    # --- VALIDASI DOKUMEN KOSONG ---
    if not files_to_zip:
        raise HTTPException(status_code=404, detail="Tidak ada file yang bisa diunduh untuk aktivitas ini.")

    # --- PROSES ZIPPING YANG LEBIH EFISIEN ---
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for doc in files_to_zip:
            zip_file.write(doc.path_atau_url, doc.nama_file_asli)
    
    zip_buffer.seek(0)

    zip_filename = f"{db_aktivitas.nama_aktivitas.replace(' ', '_')}.zip"
    
    return StreamingResponse(
        iter([zip_buffer.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={'Content-Disposition': f'attachment; filename="{zip_filename}"'}
    )