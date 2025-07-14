from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time, datetime

# Skema untuk MEMBUAT aktivitas (menerima data dari Vue)
# Tidak ada perubahan di sini
class AktivitasCreate(BaseModel):
    nama_aktivitas: str
    deskripsi: Optional[str] = None
    tim: Optional[str] = None
    tanggal: Optional[date] = None
    useDateRange: Optional[bool] = False
    useTime: Optional[bool] = False
    tanggalMulai: Optional[date] = None
    tanggalSelesai: Optional[date] = None
    jamMulai: Optional[time] = None
    jamSelesai: Optional[time] = None

# Skema untuk MEMBACA/MENGIRIM data (mengirim data ke Vue)
class Aktivitas(BaseModel):
    id: int
    nama_aktivitas: str
    deskripsi: Optional[str] = None
    
    # Pydantic akan mengisi field 'tim' dari atribut 'tim_penyelenggara' di database
    tim: Optional[str] = Field(None, alias='tim_penyelenggara')
    
    # Pydantic akan mengisi field 'tanggalMulai' dari atribut 'tanggal_mulai' di database
    tanggalMulai: Optional[date] = Field(None, alias='tanggal_mulai')
    tanggalSelesai: Optional[date] = Field(None, alias='tanggal_selesai')
    jamMulai: Optional[time] = Field(None, alias='jam_mulai')
    jamSelesai: Optional[time] = Field(None, alias='jam_selesai')
    
    dibuat_pada: datetime

    class Config:
        orm_mode = True
        # Izinkan Pydantic untuk mempopulasikan field berdasarkan alias
        allow_population_by_field_name = True