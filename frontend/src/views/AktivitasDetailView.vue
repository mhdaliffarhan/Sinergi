<template>
  <div>
    <Breadcrumbs :items="breadcrumbItems" />
    <div class="bg-white dark:bg-gray-800 p-4 sm:p-6 rounded-lg shadow-md">
      <div v-if="isLoading">
        <p class="text-center text-gray-500 dark:text-gray-400">Memuat data aktivitas...</p>
      </div>
      <div v-else-if="aktivitas">
        
        <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
          <div class="md:mb-0">
            <h1 class="text-2xl sm:text-3xl font-bold text-orange-600 dark:text-orange-500 mt-1">{{ aktivitas.namaAktivitas }}</h1>
            <p class="mt-2 text-base text-gray-500 dark:text-gray-400 max-w-3xl">{{ aktivitas.deskripsi }}</p>
          </div>
          
          <div class="flex-shrink-0 w-full md:w-auto">
            <Menu as="div" class="relative inline-block text-left w-full md:w-auto">
              <div>
                <MenuButton class="inline-flex w-full justify-center gap-x-1.5 rounded-md bg-white dark:bg-gray-700 px-4 py-2 text-sm font-semibold text-gray-900 dark:text-gray-200 shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600">
                  Tindakan
                  <svg class="-mr-1 h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                    <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
                  </svg>
                </MenuButton>
              </div>

              <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                <MenuItems class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white dark:bg-gray-800 shadow-lg ring-1 ring-inset ring-gray-300 dark:ring-gray-600 focus:outline-none">
                  <div class="py-1"> 
                    <!-- COOMING SOON -->
                    <!-- <MenuItem v-slot="{ active }">
                      <button @click="handleDownloadAll" :class="[active ? 'bg-green-100 dark:bg-green-700' : '', 'text-green-700 dark:text-green-200 block w-full text-left px-4 py-2 text-sm']">
                        Unduh Semua File     
                      </button>
                    </MenuItem> -->
                    <MenuItem v-slot="{ active }" v-if="isAnggotaTim">
                      <button @click="openEditModal" :class="[active ? 'bg-blue-100 dark:bg-blue-700' : '', 'text-blue-700 dark:text-blue-200 block w-full text-left px-4 py-2 text-sm']">
                        Edit Aktivitas
                      </button>
                    </MenuItem>
                    <MenuItem v-slot="{ active }" v-if="isAnggotaTim">
                      <button @click="confirmDeleteActivity" :class="[active ? 'bg-red-100 dark:bg-red-800' : '', 'text-red-700 dark:text-red-300 block w-full text-left px-4 py-2 text-sm']">
                        Hapus Aktivitas
                      </button>
                    </MenuItem>
                  </div>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex items-center gap-4 transition-transform hover:scale-105 duration-300">
            <span class="text-3xl">🗓️</span>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Pelaksanaan</p>
              <span class="text-base font-bold text-gray-900 dark:text-white">{{ formattedWaktuPelaksanaan.tanggal }}</span>
              <p v-if="formattedWaktuPelaksanaan.waktu" class="text-sm text-gray-600 dark:text-gray-300 mt-1">
                {{ formattedWaktuPelaksanaan.waktu }}
              </p>
            </div>
          </div>
          
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex items-center gap-4 transition-transform hover:scale-105 duration-300">
            <span class="text-3xl">👥</span>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Tim Penyelenggara</p>
              <router-link :to="{ name: 'team-detail', params: { id: aktivitas.team?.id } }" class="text-base font-bold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                {{ aktivitas.team?.namaTim || 'Tidak ada tim' }}
              </router-link>
              <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Ketua: {{ aktivitas.team?.ketuaTim?.namaLengkap || '-' }}
              </p>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex items-center gap-4 transition-transform hover:scale-105 duration-300">
            <span class="text-3xl">💼</span>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Project Terkait</p>
              <router-link :to="{ name: 'project-detail', params: { id: aktivitas.project?.id } }" class="text-base font-bold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                {{ aktivitas.project?.namaProject || 'Tidak ada proyek' }}
              </router-link>
              <p class="text-sm text-gray-600 dark:text-gray-300 mt-1">
                Leader: {{ aktivitas.project?.projectLeader?.namaLengkap || '-' }}
              </p>
            </div>
          </div>
        </div>

        <div class="mt-4 border-t border-gray-200 dark:border-gray-700 pt-4">
          <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">Anggota Aktivitas</h2>
          <div v-if="aktivitas.users && aktivitas.users.length > 0" class="flex flex-wrap -space-x-2">
            <div 
              v-for="user in aktivitas.users" 
              :key="user.id" 
              class="relative h-10 w-10 rounded-full flex items-center justify-center text-xs font-semibold text-gray-600 dark:text-gray-300 ring-2 ring-white dark:ring-gray-800 transition duration-150 transform hover:scale-110 hover:z-10"
              :title="user.namaLengkap"
            >
              <img v-if="user.fotoProfilUrl"
                :src="getProfileUrl(user.fotoProfilUrl)"
                alt="Profil"
                class="h-full w-full rounded-full object-cover"
              />
              <div v-else
                class="h-full w-full rounded-full flex items-center justify-center text-white"
                :style="{ backgroundColor: getSoftRandomColor(user.id) }"
              >
                {{ getInitials(user.namaLengkap) }}
              </div>
            </div>
          </div>
          <p v-else class="text-sm text-gray-500 dark:text-gray-400">Tidak ada anggota tim yang terlibat.</p>
        </div>
        
        <hr class="my-6 border-gray-200 dark:border-gray-700">

        <div class="mb-6">
          <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">Checklist Kelengkapan Dokumen</h2>
          <input type="file" ref="fileInputForChecklist" @change="handleFileSelectedForChecklist" class="hidden">
          <input type="file" ref="replaceFileInput" @change="handleReplaceFileSelected" class="hidden">
          <div v-if="aktivitas.daftarDokumenWajib && aktivitas.daftarDokumenWajib.length > 0" class="border border-gray-200 dark:border-gray-700 rounded-lg divide-y divide-gray-200 dark:divide-gray-700">
            <ChecklistItem
              v-for="doc in aktivitas.daftarDokumenWajib"
              :key="doc.id"
              :item="doc"
              :isKetuaTim="isKetuaTim"
              :isAnggotaTim="isAnggotaTim"
              :isProjectLeader="isProjectLeader"
              @unggah="handleUploadRequest"
              @hapus="confirmDeleteDokumen"
              @preview="handlePreviewRequest"
              @cek="handleCheckDoc"
            />
          </div>
          <div v-else>
            <p class="text-sm text-center text-gray-500 dark:text-gray-400 py-4">Tidak ada daftar dokumen wajib untuk aktivitas ini.</p>
          </div>
        </div>

        <div>
          <div class="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between mb-4">
            <h2 class="text-lg font-semibold text-gray-800 dark:text-white">Link & Dokumen Lainnya</h2>
            <button v-if="isAnggotaTim" @click="openLinkModal" class="px-3 py-1.5 text-sm font-medium text-white dark:text-gray-200 bg-blue-600 dark:bg-blue-700 rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 w-full sm:w-auto">+ Tambah Link</button>
          </div>
          <div v-if="otherDocuments.length > 0" class="border border-gray-200 dark:border-gray-700 rounded-lg divide-y divide-gray-200 dark:divide-gray-700">
            <DokumenItem 
              v-for="doc in otherDocuments" 
              :key="doc.id" 
              :dokumen="doc" 
              :isAnggotaTim="isAnggotaTim"
              @hapus="confirmDeleteDokumen"
              @preview="handlePreviewRequest" 
              class="p-3" />
          </div>
          <div v-else>
            <p class="text-sm text-center text-gray-500 dark:text-gray-400 py-4">Tidak ada Link & Dokumen Lainnya untuk aktivitas ini.</p>
          </div>
          <DropzoneUploader v-if="isAnggotaTim" @file-selected="handleFileReadyForUpload" class="mt-4" />
        </div>
      </div>
      <div v-else>
        <p class="text-center text-red-500">Gagal memuat data.</p>
      </div>
    </div>
    
    <FilePreviewModal :show="isPreviewModalOpen" :file-url="fileToPreview.url" :file-name="fileToPreview.name" :file-type="fileToPreview.type" @close="closePreviewModal" />
    <ModalWrapper :show="isEditModalOpen" @close="closeEditModal" title="Edit Aktivitas">
      <FormAktivitas tipe="Simpan" :initial-data="aktivitas" @close="closeEditModal" @submit="handleUpdateActivity" :team-list="teamList" :project-list="projectList" :team-members="teamMembers"/>
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
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import Breadcrumbs from '@/components/Breadcrumbs.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormAktivitas from '@/components/aktivitas/FormAktivitas.vue';
import DokumenItem from '@/components/aktivitas/DokumenItem.vue';
import FormTambahLink from '@/components/aktivitas/FormTambahLink.vue';
import ChecklistItem from '@/components/aktivitas/ChecklistItem.vue';
import DropzoneUploader from '@/components/aktivitas/DropzoneUploader.vue';
import FormKonfirmasiDokumen from '@/components/aktivitas/FormKonfirmasiDokumen.vue';
import ModalKonfirmasiGantiFile from '@/components/aktivitas/ModalKonfirmasiGantiFile.vue';
import FilePreviewModal from '@/components/FilePreviewModal.vue';

// --- DEKLARASI STATE & INISIALISASI ---
const baseURL = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();
const toast = useToast();
const aktivitasId = route.params.id;
const authStore = useAuthStore();
const user = authStore.user;

const aktivitas = ref(null);
const isLoading = ref(true);
const breadcrumbItems = ref([
  { text: 'Dashboard', to: '/dashboard' },
  { text: 'Daftar Aktivitas', to: '/aktivitas/daftar' },
  { text: 'Project', to: ''},
  { text: 'Detail Aktivitas' }
]);

const isEditModalOpen = ref(false);
const isLinkModalOpen = ref(false);
const isFileModalOpen = ref(false);
const isReplaceModalOpen = ref(false);
const isPreviewModalOpen = ref(false);
const fileToPreview = ref({ url: '', name: '', type: '' });

const fileToUpload = ref(null);
const fileInputForChecklist = ref(null);
const replaceFileInput = ref(null);
const checklistItemIdToUpload = ref(null);
const itemToReplace = ref(null);
const teamList = ref([]);
const teamMembers = ref([]);
const projectList = ref([]);

const isProjectLeader = computed (() => {
  const projectLeaderId = aktivitas.value?.project?.projectLeaderId;
  console.log("Project Leader ID : ", projectLeaderId);
  if (projectLeaderId && projectLeaderId === user?.id) {
    return true;
  }
  return false;
});

const isKetuaTim = computed(() => {
  const team = aktivitas.value?.team;
  if (!team) return false
  return team.ketuaTimId === user?.id
});

const isAnggotaTim = computed(() => {
  const aktivitasTeamId = aktivitas.value?.team?.id;
  if (!aktivitasTeamId) {
    return false;
  }
  if (!user || !user.teams || user.teams.length === 0) {
    return false;
  }
  return user.teams.some(team => team.id === aktivitasTeamId);
});

// --- COMPUTED PROPERTIES ---
const unfulfilledChecklistItems = computed(() =>
  aktivitas.value?.daftarDokumenWajib?.filter(item => item.dokumenId == null) || []
);


// --- FUNGSI HELPER ---
// Fungsi untuk mendapatkan inisial dari nama lengkap
const getInitials = (namaLengkap) => {
  if (!namaLengkap) return '';
  const parts = namaLengkap.split(' ').filter(p => p.length > 0);
  if (parts.length === 1) {
    return parts[0].charAt(0).toUpperCase();
  }
  return (parts[0].charAt(0) + parts[1].charAt(0)).toUpperCase();
};

// Fungsi untuk mendapatkan warna latar belakang acak yang lembut
const getSoftRandomColor = (userId) => {
  const colors = [
    '#E57373', '#F06292', '#BA68C8', '#9575CD', '#7986CB', '#64B5F6',
    '#4FC3F7', '#4DD0E1', '#4DB6AC', '#81C784', '#AED581', '#FF8A65',
    '#FFB74D', '#FFD54F', '#FFF176', '#FFEB3B', '#DCE775', '#A2D729',
    '#4FC3F7', '#64B5F6'
  ];
  const index = userId % colors.length;
  return colors[index];
};

// Helper untuk normalisasi URL foto profil
const getProfileUrl = (path) => {
  if (!path) return null;
  // Jika path dimulai dengan './', tambahkan base URL.
  // Ini penting agar gambar bisa diakses dari backend.
  if (path.startsWith('./')) {
    return `${baseURL}/${path.replace('./', '')}`;
  }
  return path;
};

const otherDocuments = computed(() => {
  if (!aktivitas.value?.dokumen) return [];
  const checklistDocIds = new Set(aktivitas.value.daftarDokumenWajib.map(item => item.dokumenId).filter(id => id != null));
  return aktivitas.value.dokumen.filter(doc => !checklistDocIds.has(doc.id));
});
const links = computed(() => otherDocuments.value.filter(d => d.tipe === 'LINK'));
const files = computed(() => otherDocuments.value.filter(d => d.tipe === 'FILE'));
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

const fetchDetailAktivitas = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${baseURL}/api/aktivitas/${aktivitasId}`);
    aktivitas.value = response.data;
    console.log("Aktivitas : ", aktivitas.value);
    breadcrumbItems.value[2] = {
        text: aktivitas.value.project.namaProject,
        to: `/project/detail/${aktivitas.value.project.id}`
      };
    breadcrumbItems.value[3].text = aktivitas.value?.namaAktivitas ?? 'Detail Aktivitas';
  } catch (error) {
    const message = error.response?.data?.message || "Gagal memuat detail aktivitas.";
    toast.error(message);
    console.error("Fetch detail aktivitas error:", error);
  } finally {
    isLoading.value = false;
  }
};

const fetchTeams = async () => {
  try {
    const response = await axios.get(`${baseURL}/api/teams/active`);
    teamList.value = response.data.map(team => ({
      id: team.id,
      namaTim: team.namaTim 
    }));
    for (const team of response.data) {
      if (team.users && team.users.length > 0) {
        teamMembers.value[team.id] = team.users.map(user => ({
          id: user.id,
          namaLengkap: user.namaLengkap,
          username: user.username
        }));
      }
    }
    console.log("Team members : ", teamMembers.value);
  } catch (error) {
    toast.error("Gagal memuat daftar tim.");
    console.error("Gagal mengambil data tim:", error);
  }
};

const fetchProjects = async () => {
  try {
    const response = await axios.get(`${baseURL}/api/projects`);
    projectList.value = response.data.items.map(project => ({
      id: project.id,
      namaProject: project.namaProject,
      teamId: project.teamId,
      projectLeaderId: project.projectLeaderId
    }));
    console.log(projectList.value);
  } catch (error) {
    toast.error("Gagal memuat data project");
    console.error("Gagal memuat data project: ", error);
  }
}

onMounted(() => { 
  fetchDetailAktivitas(); 
  fetchTeams();
  fetchProjects();
});

// --- Logika untuk Aktivitas (Edit/Hapus) ---
const openEditModal = () => { isEditModalOpen.value = true; };
const closeEditModal = () => { isEditModalOpen.value = false; };
const handleUpdateActivity = async (formData) => {
  const payload = { ...formData };
  const nullableFields = ['tanggalMulai', 'tanggalSelesai', 'jamMulai', 'jamSelesai'];
  nullableFields.forEach(field => { if (payload[field] === '') payload[field] = null; });
  try {
    await axios.put(`${baseURL}/api/aktivitas/${aktivitasId}`, payload);
    toast.success("Aktivitas berhasil diperbarui!");
    closeEditModal();
    await fetchDetailAktivitas();
  } catch (error) {
    const errorMsg = error.response?.data?.detail?.[0]?.msg || "Gagal memperbarui aktivitas.";
    toast.error(errorMsg);
  }
};

const confirmDeleteActivity = () => { if (window.confirm("Yakin ingin hapus aktivitas ini?")) deleteActivity(); };
const deleteActivity = async () => {
  try {
    await axios.delete(`${baseURL}/api/aktivitas/${aktivitasId}`);
    toast.success("Aktivitas berhasil dihapus.");
    router.push('/aktivitas/daftar');
  } catch (error) { 
    if (error.response && error.response.status === 409) {

        toast.error(error.response.data.detail);
    } else {
        // Tampilkan pesan error umum
        toast.error("Gagal menghapus aktivitas. Silakan coba lagi.");
    }
   }
};

// --- Logika untuk Dokumen (Umum) ---
const confirmDeleteDokumen = (dokumenId) => { if (window.confirm("Yakin ingin hapus dokumen ini?")) deleteDokumen(dokumenId); };
const deleteDokumen = async (dokumenId) => {
  try {
    await axios.delete(`${baseURL}/api/dokumen/${dokumenId}`);
    toast.success("Dokumen berhasil dihapus.");
    await fetchDetailAktivitas();
  } catch (error) {
    toast.error("Gagal menghapus dokumen.");
  }
};

// --- Logika untuk Tambah Link ---
const openLinkModal = () => { isLinkModalOpen.value = true; };
const closeLinkModal = () => { isLinkModalOpen.value = false; };
const handleLinkSubmit = async (formData) => {
  try {
    await axios.post(`${baseURL}/api/aktivitas/${aktivitasId}/link`, formData);
    toast.success("Link berhasil ditambahkan.");
    closeLinkModal();
    await fetchDetailAktivitas();
  } catch (error) { toast.error("Gagal menambahkan link."); }
};

// --- Logika untuk Unggah File (via Dropzone) ---
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
  }
  try {
    await axios.post(`${baseURL}/api/aktivitas/${aktivitasId}/dokumen`, data);
    toast.success("File berhasil diunggah.");
    closeFileModal();
    await fetchDetailAktivitas();
  } catch (error) { toast.error("Gagal mengunggah file"); }
};

// --- Logika untuk Unggah File (via Checklist) ---
const handleUploadRequest = (itemId) => {
  checklistItemIdToUpload.value = itemId;
  fileInputForChecklist.value.click();
};

const handleFileSelectedForChecklist = async (event) => {
  const file = event.target.files[0];
  if (!file || !checklistItemIdToUpload.value) return;

  // Temukan nama item checklist untuk dijadikan keterangan default
  const checklistItem = aktivitas.value.daftarDokumenWajib.find(
    item => item.id === checklistItemIdToUpload.value
  );
  const keterangan = checklistItem ? checklistItem.namaDokumen : 'Dokumen Checklist';

  // Siapkan data untuk dikirim
  const data = new FormData();
  data.append('file', file);
  data.append('keterangan', keterangan);
  data.append('checklist_item_id', checklistItemIdToUpload.value);
  console.log('data : ',data);
  try {
    await axios.post(`${baseURL}/api/aktivitas/${aktivitasId}/dokumen`, data);
      
    toast.success("Dokumen berhasil diunggah & checklist diperbarui!");
    await fetchDetailAktivitas();
  } catch (error) {
    toast.error("Gagal mengunggah file.");
    console.error(error);
  } finally {
    checklistItemIdToUpload.value = null;
    event.target.value = '';
  }
};

// --- Logika untuk Ganti File (via Checklist) ---
const openReplaceModal = () => { isReplaceModalOpen.value = true; };
const closeReplaceModal = () => { isReplaceModalOpen.value = false; itemToReplace.value = null; };
const handleGantiRequest = (item) => {
  itemToReplace.value = item;
  openReplaceModal();
};
const handleReplaceActionChosen = (action) => {
  if (!itemToReplace.value) return;
  itemToReplace.value.old_file_action = action;
  closeReplaceModal();
  replaceFileInput.value.click();
};
const handleReplaceFileSelected = async (event) => {
  const newFile = event.target.files[0];
  if (!newFile || !itemToReplace.value) return;
  const data = new FormData(); 
  data.append('file', newFile);
  data.append('old_file_action', itemToReplace.value.old_file_action);
  try {
    await axios.post(`${baseURL}/api/checklist/${itemToReplace.value.id}/replace`, data);
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

const openPreviewModal = () => { isPreviewModalOpen.value = true; };
const closePreviewModal = () => {
  // Hapus URL sementara untuk membersihkan memori
  if (fileToPreview.value.url) {
    window.URL.revokeObjectURL(fileToPreview.value.url);
  }
  isPreviewModalOpen.value = false;
  fileToPreview.value = { url: '', name: '', type: '' };
};

// Fungsi ini dipanggil saat event @preview dari DokumenItem diterima
const handlePreviewRequest = async (dokumen) => {
  try {
    const response = await axios.get(`${baseURL}/api/dokumen/${dokumen.id}/download`, {
      responseType: 'blob',
    });

    const blob = new Blob([response.data], { type: response.headers['content-type'] });
    const url = window.URL.createObjectURL(blob);
    
    fileToPreview.value = {
      url: url,
      name: dokumen.namaFileAsli,
      type: response.headers['content-type']
    };
    
    // Buka modal
    openPreviewModal();

  } catch (error) {
    toast.error("Gagal membuka file untuk preview.");
    console.error(error);
  }
};

const handleDownloadAll = async () => {
  // --- VALIDASI DI FRONTEND ---
  const filesToDownload = files.value;

  if (filesToDownload.length === 0) {
    toast.warning("Tidak ada file yang bisa diunduh untuk aktivitas ini.");
    return; 
  }

  if (window.confirm(`Apakah Anda yakin ingin mengunduh semua file untuk aktivitas ini?`)) {
    const toastId = toast.info("Sedang mempersiapkan file ZIP, mohon tunggu...", { timeout: false });
    
    try {
      const response = await axios.get(`${baseURL}/api/aktivitas/${aktivitasId}/download-all`, {
        responseType: 'blob',
        timeout: 60000,
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      let fileName = `${aktivitas.value.namaAktivitas || 'dokumen'}.zip`;
      const contentDisposition = response.headers['content-disposition'];
      if (contentDisposition) {
        const fileNameMatch = contentDisposition.match(/filename="(.+)"/);
        if (fileNameMatch && fileNameMatch.length === 2) {
          fileName = fileNameMatch[1];
        }
      }

      link.setAttribute('download', fileName);
      document.body.appendChild(link);
      link.click();

      link.remove();
      window.URL.revokeObjectURL(url);
      toast.dismiss(toastId);
      toast.success("File ZIP berhasil diunduh!");

    } catch (error) {
      toast.dismiss(toastId);
      console.error("Gagal mengunduh semua file:", error);
      toast.error(error.response?.data?.detail || "Gagal mengunduh file ZIP.");
    }
  }
};

const handleCheckDoc = async ({ id, value }) => {
  try {
    const { data } = await axios.patch(`${baseURL}/api/daftar_dokumen/${id}/cek`, {
      statusPengecekan: value
    })

    // update lokal state biar realtime
    const target = aktivitas.value.daftarDokumenWajib.find(d => d.id === id)
    if (target) target.statusPengecekan = data.statusPengecekan

    toast.success(value ? 'Ditandai sudah dicek' : 'Tanda cek dibatalkan')
  } catch (err) {
    console.error(err)
    toast.error(err?.response?.data?.detail || 'Gagal memperbarui status pengecekan')
  }
};
</script>