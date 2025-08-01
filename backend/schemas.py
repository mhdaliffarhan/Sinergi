from pydantic import BaseModel, model_validator, Field, ConfigDict
from typing import Optional, Any, List
from datetime import date, time, datetime

def to_camel(snake_str: str) -> str:
    parts = snake_str.split('_')
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

# Model dasar yang akan melakukan konversi otomatis untuk SEMUA skema
class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, 
        populate_by_name=True, 
        from_attributes=True          
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

class Dokumen(CamelModel):
    id: int
    keterangan: str
    tipe: str
    path_atau_url: str
    nama_file_asli: Optional[str] = None
    diunggah_pada: datetime


class DaftarDokumen(CamelModel):
    id: int
    nama_dokumen: str
    status: str
    dokumen_id: Optional[int] = None
    dokumen_terkait: Optional[Dokumen] = None

class AktivitasBase(CamelModel):
    nama_aktivitas: str
    deskripsi: Optional[str] = None
    tim_penyelenggara: Optional[str] = None
    use_date_range: Optional[bool] = False
    use_time: Optional[bool] = False
    tanggal_mulai: Optional[date] = None
    tanggal_selesai: Optional[date] = None
    jam_mulai: Optional[time] = None
    jam_selesai: Optional[time] = None

# Skema untuk MEMBUAT aktivitas (menerima data dari Vue)
class AktivitasCreate(AktivitasBase):
    daftar_dokumen_wajib: List[str] = []

    @model_validator(mode='before')
    @classmethod
    def check_required_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            use_date_range = data.get('useDateRange') # Di sini tetap pakai camelCase karena data datang dari JSON
            if not use_date_range:
                if not data.get('tanggalMulai'):
                    raise ValueError('Tanggal Pelaksanaan wajib diisi.')
            elif use_date_range:
                if not data.get('tanggalMulai') or not data.get('tanggalSelesai'):
                    raise ValueError('Tanggal Mulai dan Tanggal Selesai wajib diisi.')
        return data

class Aktivitas(AktivitasBase):
    id: int
    dibuat_pada: datetime
    dokumen: List[Dokumen] = []
    daftar_dokumen_wajib: List[DaftarDokumen] = []


# Skema untuk Token JWT
class Token(CamelModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class DokumenCreate(BaseModel): # Tidak perlu konversi
    keterangan: str
    pathAtauUrl: str