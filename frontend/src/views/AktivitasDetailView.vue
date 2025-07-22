<template>
  <div>
    <Breadcrumbs :items="breadcrumbItems" />
    <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div v-if="isLoading">
        <p class="text-center text-gray-500 dark:text-gray-400">Memuat data aktivitas...</p>
      </div>
      <div v-else-if="aktivitas">
        <div class="flex items-start justify-between">
            <div>
              <p class="text-sm text-blue-500 font-semibold">{{ aktivitas.timPenyelenggara }}</p>
              <h1 class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ aktivitas.namaAktivitas }}</h1>
              <p class="mt-2 text-base text-gray-500 dark:text-gray-400 max-w-3xl">{{ aktivitas.deskripsi }}</p>
            </div>
            <div class="flex items-center gap-2 flex-shrink-0 ml-4">
              <button @click="openEditModal" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">Edit</button>
              <button @click="confirmDelete" class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700">Hapus</button>
            </div>
        </div>
        <div class="mt-4 flex flex-wrap items-center gap-3 border-t border-gray-200 dark:border-gray-700 pt-4">
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100 dark:bg-gray-700">
            <span class="text-lg">🗓️</span>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ formattedWaktuPelaksanaan.tanggal }}</span>
          </div>
          <div v-if="aktivitas.jamMulai" class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100 dark:bg-gray-700">
            <span class="text-lg">🕒</span>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ formattedWaktuPelaksanaan.waktu }}</span>
          </div>
        </div>

        <hr class="my-6 border-gray-200 dark:border-gray-700">

         <div class="mb-6">
          <div class="mb-6">
            <DropzoneUploader @file-selected="handleFileReadyForUpload" />
          </div>
          <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">Kelengkapan Dokumen</h2>

          <input type="file" ref="fileInputChecklist" @change="handleFileSelectedForChecklist" class="hidden">
          <input type="file" ref="replaceFileInput" @change="handleReplaceFileSelected" class="hidden">

          <div v-if="aktivitas.daftarDokumenWajib && aktivitas.daftarDokumenWajib.length > 0" class="border border-gray-200 dark:border-gray-700 rounded-lg divide-y divide-gray-200 dark:divide-gray-700">
            <ChecklistItem
              v-for="item in aktivitas.daftarDokumenWajib"
              :key="item.id"
              :item="item"
              @unggah="handleUploadRequest"
              @ganti="handleGantiRequest"
              @hapus="confirmDeleteDokumen"
            />
          </div>
          <div v-else>
            <p class="text-sm text-center text-gray-500 dark:text-gray-400">Tidak ada daftar dokumen wajib untuk aktivitas ini.</p>
          </div>
        </div>


        <div class="mb-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-gray-800 dark:text-white">Link & Dokumen Lainnya</h2>
            <button @click="openLinkModal" class="px-3 py-1.5 font-medium text-gray-700 dark:text-gray-200 bg-gray-200 dark:bg-gray-600 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500">+ Tambah Link</button>
          </div>
          <div v-if="otherDocuments.length > 0" class="border border-gray-200 dark:border-gray-700 rounded-lg divide-y divide-gray-200 dark:divide-gray-700">
            <DokumenItem v-for="doc in otherDocuments" :key="doc.id" :dokumen="doc" @hapus="confirmDeleteDokumen" />
          </div>
          
        </div>
      </div>
      <div v-else>
        <p class="text-center text-red-500">Gagal memuat data atau aktivitas tidak ditemukan.</p>
      </div>
    </div>

    <ModalWrapper :show="isEditModalOpen" @close="closeEditModal" title="Edit Aktivitas">
      <FormBuatAktivitas :initial-data="aktivitas" @close="closeEditModal" @submit="handleUpdateActivity" />
    </ModalWrapper>
    <ModalWrapper :show="isLinkModalOpen" @close="closeLinkModal" title="Tambah Link Baru">
      <FormTambahLink @close="closeLinkModal" @submit="handleLinkSubmit" />
    </ModalWrapper>
    <ModalWrapper :show="isFileModalOpen" @close="closeFileModal" title="Konfirmasi Unggah File">
      <FormKonfirmasiDokumen v-if="fileToUpload" :file="fileToUpload" :unfulfilled-items="unfulfilledChecklistItems" @close="closeFileModal" @submit="handleFileUploadSubmit" />
    </ModalWrapper>
    <ModalWrapper :show="isReplaceModalOpen" @close="closeReplaceModal" title="Ganti File Dokumen">
      <ModalKonfirmasiGantiFile @pilih="handleReplaceActionChosen" />
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import Breadcrumbs from '@/components/Breadcrumbs.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormBuatAktivitas from '@/components/FormBuatAktivitas.vue';
import DokumenItem from '@/components/DokumenItem.vue';
import FormTambahLink from '@/components/FormTambahLink.vue';
import DropzoneUploader from '@/components/DropzoneUploader.vue';
import FormKonfirmasiDokumen from '@/components/FormKonfirmasiDokumen.vue';
import ChecklistItem from '@/components/ChecklistItem.vue';
import ModalKonfirmasiGantiFile from '@/components/ModalKonfirmasiGantiFile.vue';

const route = useRoute();
const router = useRouter();
const toast = useToast();
const aktivitasId = route.params.id;

const aktivitas = ref(null);
const isLoading = ref(true);
const breadcrumbItems = ref([
  { text: 'Dashboard', to: '/dashboard' },
  { text: 'Detail Aktivitas' }
]);

const isEditModalOpen = ref(false);
const isLinkModalOpen = ref(false);
const isFileModalOpen = ref(false);
const fileToUpload = ref(null);

const fileInputChecklist = ref(null); 
const checklistItemIdToUpload = ref(null);

const isReplaceModalOpen = ref(false);
const itemToReplace = ref(null);
const replaceFileInput = ref(null);


const files = computed(() => aktivitas.value?.dokumen?.filter(d => d.tipe === 'FILE') || []);
const links = computed(() => aktivitas.value?.dokumen?.filter(d => d.tipe === 'LINK') || []);
const unfulfilledChecklistItems = computed(() => 
  aktivitas.value?.daftarDokumenWajib?.filter(item => item.status !== 'Selesai') || []
);
const otherDocuments = computed(() => {
  const checklistDocIds = new Set(aktivitas.value?.daftarDokumenWajib?.map(item => item.dokumenId).filter(id => id != null));
  return aktivitas.value?.dokumen?.filter(doc => !checklistDocIds.has(doc.id)) || [];
});
const formattedWaktuPelaksanaan = computed(() => {
  if (!aktivitas.value || !aktivitas.value.tanggalMulai) return { tanggal: 'Tanggal belum ditentukan', waktu: '' };
  const options = { day: 'numeric', month: 'long', year: 'numeric' };
  let tanggalTampil = '';
  let waktuTampil = '';
  const tglMulai = new Date(aktivitas.value.tanggalMulai);
  
  if (aktivitas.value.tanggalSelesai) {
    const tglSelesai = new Date(aktivitas.value.tanggalSelesai);
    const mulai = tglMulai.toLocaleDateString('id-ID', { day: 'numeric', month: 'long' });
    const selesai = tglSelesai.toLocaleDateString('id-ID', options);
    tanggalTampil = `${mulai} - ${selesai}`;
  } else {
    tanggalTampil = tglMulai.toLocaleDateString('id-ID', options);
  }

  if (aktivitas.value.jamMulai) {
    waktuTampil = `${aktivitas.value.jamMulai} - ${aktivitas.value.jamSelesai} WITA`;
  }
  return { tanggal: tanggalTampil, waktu: waktuTampil };
});
const snakeToCamel = (str) => str.replace(/([-_][a-z])/g, (group) => group.toUpperCase().replace('-', '').replace('_', ''));
const convertKeysToCamelCase = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(item => convertKeysToCamelCase(item));
  const newObj = {};
  for (let key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      newObj[snakeToCamel(key)] = convertKeysToCamelCase(obj[key]);
    }
  }
  return newObj;
};
const fetchDetailAktivitas = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}`);
    aktivitas.value = convertKeysToCamelCase(response.data);
    breadcrumbItems.value[1].text = aktivitas.value.namaAktivitas;
  } catch (error) {
    toast.error("Gagal memuat detail aktivitas.");
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};
const openEditModal = () => { isEditModalOpen.value = true; };
const closeEditModal = () => { isEditModalOpen.value = false; };
const handleUpdateActivity = async (formData) => {
  const payload = { ...formData };
  const nullableFields = ['tanggalMulai', 'tanggalSelesai', 'jamMulai', 'jamSelesai'];
  nullableFields.forEach(field => { if (payload[field] === '') payload[field] = null; });
  try {
    await axios.put(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}`, payload);
    toast.success("Aktivitas berhasil diperbarui!");
    closeEditModal();
    await fetchDetailAktivitas();
  } catch (error) {
    const errorMsg = error.response?.data?.detail?.[0]?.msg || "Gagal memperbarui aktivitas.";
    toast.error(errorMsg);
  }
};

const confirmDelete = () => { if (window.confirm("Yakin ingin hapus aktivitas ini?")) deleteActivity(); };
const deleteActivity = async () => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}`);
    toast.success("Aktivitas berhasil dihapus.");
    router.push('/dashboard');
  } catch (error) { toast.error("Gagal menghapus aktivitas."); }
};

const confirmDeleteDokumen = (dokumenId) => { if (window.confirm("Yakin ingin hapus dokumen ini?")) deleteDokumen(dokumenId); };
const deleteDokumen = async (dokumenId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/dokumen/${dokumenId}`);
    toast.success("Dokumen berhasil dihapus.");
    await fetchDetailAktivitas();
  } catch (error) { toast.error("Gagal menghapus dokumen."); }
};

const openLinkModal = () => { isLinkModalOpen.value = true; };
const closeLinkModal = () => { isLinkModalOpen.value = false; };
const handleLinkSubmit = async (formData) => {
  try {
    await axios.post(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}/link`, { ...formData, tipe: 'LINK' });
    toast.success("Link berhasil ditambahkan.");
    closeLinkModal();
    await fetchDetailAktivitas();
  } catch (error) { toast.error("Gagal menambahkan link."); }
};

const closeFileModal = () => { isFileModalOpen.value = false; fileToUpload.value = null; };
const handleFileReadyForUpload = (file) => {
  fileToUpload.value = file;
  isFileModalOpen.value = true;
};
const handleFileUploadSubmit = async (formData) => {
  const data = new FormData();
  data.append('file', formData.file);
  data.append('keterangan', formData.keterangan);
  if (formData.checklistItemId) {
    data.append('checklist_item_id', formData.checklistItemId);
    console.log('ada checklist item', formData.checklistItemId);
  }
  
  try {
    await axios.post(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}/dokumen`, data);
    toast.success("File berhasil diunggah.");
    closeFileModal();
    await fetchDetailAktivitas();
  } catch (error) { toast.error("Gagal mengunggah file"); }
};

// 1. Fungsi ini dipanggil saat tombol "Upload" di ChecklistItem diklik
const handleUploadRequest = (itemId) => {
  checklistItemIdToUpload.value = itemId; // Simpan ID itemnya
  fileInputChecklist.value.click(); // Buka dialog pilih file
};

const handleFileSelectedForChecklist = async (event) => {
  // 1. Ambil file yang dipilih dari input
  const file = event.target.files[0];

  // 2. Pastikan ada file yang dipilih & kita tahu untuk checklist item mana
  if (!file || !checklistItemIdToUpload.value) {
    event.target.value = ''; // Reset input jika dibatalkan
    return;
  }

  // 3. Temukan nama item checklist untuk dijadikan keterangan default
  const checklistItem = aktivitas.value.daftarDokumenWajib.find(
    item => item.id === checklistItemIdToUpload.value
  );
  const keterangan = checklistItem ? checklistItem.namaDokumen : 'Dokumen Checklist';

  // 4. Siapkan data untuk dikirim ke backend
  const data = new FormData();
  data.append('file', file);
  data.append('keterangan', keterangan);
  data.append('checklist_item_id', checklistItemIdToUpload.value);
  
  try {
    // 5. Panggil endpoint upload DOKUMEN yang cerdas
    await axios.post(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}/dokumen`, data);
    
    toast.success(`Dokumen "${keterangan}" berhasil diunggah!`);
    await fetchDetailAktivitas(); // Muat ulang data untuk melihat status baru
  } catch (error) {
    toast.error("Gagal mengunggah file.");
    console.error(error);
  } finally {
    // 6. Reset state setelah selesai
    checklistItemIdToUpload.value = null;
    event.target.value = ''; // Reset input file agar bisa memilih file yang sama lagi
  }
};

const openReplaceModal = () => { isReplaceModalOpen.value = true; };
const closeReplaceModal = () => { isReplaceModalOpen.value = false; };

// 1. Dipicu saat tombol 'Ganti File' di ChecklistItem diklik
const handleGantiRequest = (item) => {
  itemToReplace.value = item;
  openReplaceModal();
};

// 2. Dipicu saat pengguna memilih 'hapus' atau 'unlink' di modal konfirmasi
const handleReplaceActionChosen = (action) => {
  if (!itemToReplace.value) return;
  itemToReplace.value.old_file_action = action;
  closeReplaceModal();
  replaceFileInput.value.click(); // Memicu input file pengganti
};

// 3. Dipicu setelah pengguna memilih file baru
const handleReplaceFileSelected = async (event) => {
  const newFile = event.target.files[0];
  console.log('2. File yang baru dipilih:', newFile);
  console.log('3. Isi `itemToReplace`:', itemToReplace.value);

  if (!newFile || !itemToReplace.value) return;
  
  console.log('terpanggil');

  const data = new FormData(); 
  data.append('file', newFile);
  data.append('old_file_action', itemToReplace.value.old_file_action);

  try {
    await axios.post(`http://127.0.0.1:8000/api/checklist/${itemToReplace.value.id}/replace`, data);
    toast.success("File berhasil diganti!");
    await fetchDetailAktivitas();
  } catch (error) {
    toast.error("Gagal mengganti file.");
    console.error(error);
  } finally {
    itemToReplace.value = null;
    event.target.value = '';
  }
};



onMounted(() => {
  fetchDetailAktivitas();
});
</script>