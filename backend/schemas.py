from pydantic import BaseModel, model_validator, Field, ConfigDict
from typing import Optional, Any
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
    # Hilangkan Optional untuk membuatnya wajib diisi
    namaAktivitas: str
    timPenyelenggara: str

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