// src/data/dummyActivities.js
export const dummyActivities = [
  {
    id: 1,
    namaAktivitas: "Rapat Pleno Sensus Ekonomi",
    timPenyelenggara: "Tim Sensus Ekonomi",
    dibuatPada: "2025-07-01",
    daftarDokumenWajib: [
      { id: 101, namaDokumen: "Memo Undangan", status: "Selesai", diunggahPada: "2025-07-02" },
      { id: 102, namaDokumen: "Daftar Hadir", status: "Selesai", diunggahPada: "2025-07-05" },
      { id: 103, namaDokumen: "Notulensi Rapat", status: "Wajib Diunggah" },
      { id: 104, namaDokumen: "Foto Kegiatan", status: "Wajib Diunggah" },
    ],
  },
  {
    id: 2,
    namaAktivitas: "Perjalanan Dinas ke Lombok Timur",
    timPenyelenggara: "Tim Survei Lapangan",
    dibuatPada: "2025-07-03",
    daftarDokumenWajib: [
      { id: 201, namaDokumen: "SPPD", status: "Selesai", diunggahPada: "2025-07-04" },
      { id: 202, namaDokumen: "Laporan Hasil", status: "Selesai", diunggahPada: "2025-07-08" },
      { id: 203, namaDokumen: "Dokumentasi Biaya", status: "Selesai", diunggahPada: "2025-07-08" },
    ],
  },
  {
    id: 3,
    namaAktivitas: "Pelatihan Aplikasi SINERGI",
    timPenyelenggara: "Divisi IT",
    dibuatPada: "2025-07-05",
    daftarDokumenWajib: [
      { id: 301, namaDokumen: "Materi Pelatihan", status: "Selesai", diunggahPada: "2025-07-06" },
      { id: 302, namaDokumen: "Absensi Peserta", status: "Wajib Diunggah" },
    ],
  },
  {
    id: 4,
    namaAktivitas: "Rapat Bulanan Tim Neraca",
    timPenyelenggara: "Tim Neraca",
    dibuatPada: "2025-07-08",
    daftarDokumenWajib: [
      { id: 401, namaDokumen: "Notulensi", status: "Wajib Diunggah" },
    ],
  },
];