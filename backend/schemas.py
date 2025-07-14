from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, time, datetime

# Model dasar untuk semua skema kita
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
    pass

# Skema untuk MEMBACA/MENGIRIM data (mengirim data ke Vue)
class Aktivitas(BaseModel):
    # Field di sini juga camelCase, tapi menggunakan alias
    # untuk memetakan dari snake_case di database
    id: int
    namaAktivitas: str = Field(alias='nama_aktivitas')
    deskripsi: Optional[str] = None
    timPenyelenggara: Optional[str] = Field(None, alias='tim_penyelenggara')
    tanggalMulai: Optional[date] = Field(None, alias='tanggal_mulai')
    tanggalSelesai: Optional[date] = Field(None, alias='tanggal_selesai')
    jamMulai: Optional[time] = Field(None, alias='jam_mulai')
    jamSelesai: Optional[time] = Field(None, alias='jam_selesai')
    dibuatPada: datetime = Field(alias='dibuat_pada')

    # Ini adalah sintaks Pydantic V2 yang benar
    model_config = ConfigDict(
        from_attributes=True,  # Menggantikan orm_mode = True
        populate_by_name=True, # Menggantikan allow_population_by_field_name
    )