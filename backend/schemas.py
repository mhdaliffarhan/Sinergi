from pydantic import BaseModel, model_validator, Field, ConfigDict
from typing import Optional, Any, List
from datetime import date, time, datetime

def to_camel(snake_str: str) -> str:
    parts = snake_str.split('_')
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

# Model dasar yang akan melakukan konversi otomatis untuk SEMUA skema
class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,      # Otomatis buat alias camelCase
        populate_by_name=True, # Izinkan pengisian via snake_case atau camelCase
        from_attributes=True           # Izinkan membaca dari objek SQLAlchemy
    )

class Team(CamelModel):
    id: int
    nama_tim: str

class Jabatan(CamelModel):
    id: int
    nama_jabatan: str

class SistemRole(CamelModel):
    id: int
    nama_role: str

class UserBase(CamelModel):
    username: str
    nama_lengkap: Optional[str] = None

class UserCreate(UserBase):
    password: str
    sistem_role_id: int
    jabatan_id: int

class User(UserBase):
    id: int
    is_active: bool
    sistem_role: SistemRole
    jabatan: Optional[Jabatan] = None
    teams: List[Team] = []

# --- SKEMA DAFTAR DOKUMEN WAJIB ---
class DaftarDokumen(BaseModel):
    id: int
    namaDokumen: str = Field(alias='nama_dokumen')
    status: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

class AktivitasBase(BaseModel):
    # Field didefinisikan dengan camelCase agar sesuai dengan standar API/JSON
    namaAktivitas: str
    deskripsi: Optional[str] = None
    timPenyelenggara: Optional[str] = None
    tanggal: Optional[date] = None
    useDateRange: Optional[bool] = False
    useTime: Optional[bool] = False
    tanggalMulai: Optional[date] = None
    tanggalSelesai: Optional[date] = None
    jamMulai: Optional[time] = None
    jamSelesai: Optional[time] = None

# Skema untuk MEMBUAT aktivitas (menerima data dari Vue)
class AktivitasCreate(AktivitasBase):
    namaAktivitas: str
    timPenyelenggara: str
    daftarDokumenWajib: List[str] = []

    @model_validator(mode='before')
    @classmethod
    def check_required_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # Validasi Tanggal
            use_date_range = data.get('useDateRange')
            if use_date_range:
                if not data.get('tanggalMulai') or not data.get('tanggalSelesai'):
                    raise ValueError('Tanggal Mulai dan Tanggal Selesai wajib diisi jika menggunakan rentang tanggal.')
            else:
                if not data.get('tanggalMulai'):
                    raise ValueError('Tanggal Pelaksanaan wajib diisi.')
                
            
            # Validasi Jam
            use_time = data.get('useTime')
            if use_time:
                if not data.get('jamMulai') or not data.get('jamSelesai'):
                    raise ValueError('Jam Mulai dan Jam Selesai wajib diisi jika menggunakan jam.')
                if not use_date_range:
                    if data.get('jamMulai') >= data.get('jamSelesai'):
                        raise ValueError('Jam Mulai harus sebelum Jam Selesai!')
        return data
    
class DokumenBase(BaseModel):
    keterangan: str
    tipe: str # 'FILE' atau 'LINK'
    pathAtauUrl: str

class DokumenCreate(DokumenBase):
    pass

class Dokumen(BaseModel):
    id: int
    keterangan: str
    tipe: str
    pathAtauUrl: str = Field(alias='path_atau_url')
    namaFileAsli: Optional[str] = Field(None, alias='nama_file_asli')
    tipeFileMime: Optional[str] = Field(None, alias='tipe_file_mime')
    diunggahPada: datetime = Field(alias='diunggah_pada')

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


# Skema untuk MEMBACA/MENGIRIM data (mengirim data ke Vue)
class Aktivitas(BaseModel):
    id: int
    namaAktivitas: str = Field(alias='nama_aktivitas')
    deskripsi: Optional[str] = None
    timPenyelenggara: Optional[str] = Field(None, alias='tim_penyelenggara')
    tanggalMulai: Optional[date] = Field(None, alias='tanggal_mulai')
    tanggalSelesai: Optional[date] = Field(None, alias='tanggal_selesai')
    jamMulai: Optional[time] = Field(None, alias='jam_mulai')
    jamSelesai: Optional[time] = Field(None, alias='jam_selesai')
    dibuatPada: datetime = Field(alias='dibuat_pada')

    dokumenList: List[Dokumen] = Field(default=[], alias='dokumen')

    daftarDokumenWajib: List[DaftarDokumen] = Field(default=[], alias='daftar_dokumen_wajib')

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )

# Skema untuk Token JWT
class Token(BaseModel):
    accessToken: str = Field(alias='access_token')
    tokenType: str = Field(alias='token_type')

    # Tambahkan config ini agar alias bisa digunakan
    model_config = ConfigDict(
        populate_by_name=True,
    )

class TokenData(BaseModel):
    username: Optional[str] = None

