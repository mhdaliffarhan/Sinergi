<template>
  <div>
    <Breadcrumbs :items="breadcrumbItems" />
    <div class="bg-white dark:bg-gray-800 p-4 sm:p-6 rounded-lg shadow-md">
      <div v-if="isLoading">
        <p class="text-center text-gray-500 dark:text-gray-400">Memuat data Project...</p>
      </div>
      <div v-else-if="project">
        
        <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
          <div class="md:mb-0">
            <p class="text-sm text-blue-500 font-semibold">{{ project.team.namaTim }}</p>
            <h1 class="text-2xl sm:text-3xl font-bold text-orange-600 dark:text-orange-500 mt-1">{{ project.namaProject }}</h1>
            <p class="mt-2 text-base text-gray-500 dark:text-gray-400 max-w-3xl">{{ project.deskripsi }}</p>
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
                    <MenuItem v-slot="{ active }">
                      <button @click="handleDownloadAll" :class="[active ? 'bg-green-100 dark:bg-green-700' : '', 'text-green-700 dark:text-green-200 block w-full text-left px-4 py-2 text-sm']">
                        Unduh Semua File    
                      </button>
                    </MenuItem>
                    <MenuItem v-slot="{ active }" v-if="isKetuaTim || isProjectLeader">
                      <button @click="openEditModal" :class="[active ? 'bg-blue-100 dark:bg-blue-700' : '', 'text-blue-700 dark:text-blue-200 block w-full text-left px-4 py-2 text-sm']">
                        Edit Project
                      </button>
                    </MenuItem>
                    <MenuItem v-slot="{ active }" v-if="isKetuaTim">
                      <button @click="confirmDeleteProject" :class="[active ? 'bg-red-100 dark:bg-red-800' : '', 'text-red-700 dark:text-red-300 block w-full text-left px-4 py-2 text-sm']">
                        Hapus Project
                      </button>
                    </MenuItem>
                  </div>
                </MenuItems>
              </transition>
            </Menu>
          </div>
        </div>

        <div class="mt-4 border-t border-gray-200 dark:border-gray-700 pt-4">
          <div v-if="project.aktivitas && project.aktivitas.length > 0" class="relative">
            <swiper
              :slides-per-view="1"
              :space-between="16"
              :pagination="{ clickable: true }"
              :navigation="true"
              :breakpoints="{
                640: { // Ukuran layar sm: dan di atas
                  slidesPerView: 2,
                  spaceBetween: 20,
                },
                768: { // Ukuran layar md: dan di atas
                  slidesPerView: 3,
                  spaceBetween: 30,
                },
                1024: { // Ukuran layar lg: dan di atas
                  slidesPerView: 4,
                  spaceBetween: 40,
                },
              }"
              class="my-swiper"
            >
              <swiper-slide v-for="aktivitas in project.aktivitas" :key="aktivitas.id">
                <AktivitasCard :aktivitas="aktivitas" />
              </swiper-slide>
            </swiper>
          </div>
          <div v-else class="text-center p-4">
            <p class="text-sm font-medium text-gray-500 dark:text-gray-400">
              Tidak ada aktivitas yang sedang berlangsung untuk Project ini.
            </p>
          </div>
        </div>

        <hr class="my-6 border-gray-200 dark:border-gray-700">
        
        <div>
           <div class="flex flex-col items-start gap-3 sm:flex-row sm:items-center sm:justify-between mb-4">
            <h2 class="text-lg font-semibold text-gray-800 dark:text-white">Dokumen & Link</h2>
            <button @click="openLinkModal" class="px-3 py-1.5 text-sm font-medium text-white dark:text-gray-200 bg-blue-600 dark:bg-blue-700 rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 w-full sm:w-auto">+ Tambah Link</button>
          </div>
          <div v-if="project.dokumen && project.dokumen.length > 0" class="border border-gray-200 dark:border-gray-700 rounded-lg divide-y divide-gray-200 dark:divide-gray-700">
            <DokumenItem 
              v-for="doc in project.dokumen" 
              :key="doc.id" 
              :dokumen="doc" 
              @hapus="confirmDeleteDokumen"
              @preview="handlePreviewRequest" 
              class="p-3" />
          </div>
          <div v-else>
            <p class="text-sm text-center text-gray-500 dark:text-gray-400 py-4">Belum ada dokumen yang diunggah untuk Project ini.</p>
          </div>
          <DropzoneUploader @file-selected="handleFileReadyForUpload" class="mt-4" />
        </div>
      </div>
      <div v-else>
        <p class="text-center text-red-500">Gagal memuat data.</p>
      </div>
    </div>
    
    <FilePreviewModal :show="isPreviewModalOpen" :file-url="fileToPreview.url" :file-name="fileToPreview.name" :file-type="fileToPreview.type" @close="closePreviewModal" />
    <ModalWrapper :show="isEditModalOpen" @close="closeEditModal" title="Edit Project">
      <FormProject tipe="Simpan" :initial-data="project" @close="closeEditModal" @submit="handleUpdateProject" :team-list="teamList"/>
    </ModalWrapper>
    <ModalWrapper :show="isLinkModalOpen" @close="closeLinkModal" title="Tambah Link Baru">
      <FormTambahLink @close="closeLinkModal" @submit="handleLinkSubmit" />
    </ModalWrapper>
    <ModalWrapper :show="isFileModalOpen" @close="closeFileModal" title="Konfirmasi Unggah File">
      <FormKonfirmasiDokumen v-if="fileToUpload" :file="fileToUpload" :unfulfilled-items="[]" @close="closeFileModal" @submit="handleFileUploadSubmit" />
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
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';

import Breadcrumbs from '@/components/Breadcrumbs.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import DokumenItem from '@/components/aktivitas/DokumenItem.vue';
import DropzoneUploader from '@/components/aktivitas/DropzoneUploader.vue';
import FormTambahLink from '@/components/aktivitas/FormTambahLink.vue';
import FormKonfirmasiDokumen from '@/components/aktivitas/FormKonfirmasiDokumen.vue';
import FilePreviewModal from '@/components/FilePreviewModal.vue';

// Pastikan komponen ini sudah Anda buat
import FormProject from '@/components/project/FormProject.vue'; 
import AktivitasCard from '@/components/aktivitas/AktivitasCard.vue';
import { id } from 'date-fns/locale';

// --- DEKLARASI STATE & INISIALISASI ---
const baseURL = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();
const toast = useToast();
const projectId = route.params.id;
const authStore = useAuthStore();
const user = authStore.user;

const project = ref(null);
const isLoading = ref(true);
const breadcrumbItems = ref([
  { text: 'Dashboard', to: '/dashboard' },
  { text: 'Daftar Project', to: '/project' },
  { text: 'Detail Project' }
]);

const isEditModalOpen = ref(false);
const isLinkModalOpen = ref(false);
const isFileModalOpen = ref(false);
const isPreviewModalOpen = ref(false);
const fileToPreview = ref({ url: '', name: '', type: '' });
const fileToUpload = ref(null);
const teamList = ref([]);

const isProjectLeader = (() => {
  const ProjectLeader_id = project.value?.ProjectLeader_id;
  if (!ProjectLeader_id) return false;
  return ProjectLeader_id === user?.id;
});

// --- COMPUTED PROPERTIES ---
const isKetuaTim = computed(() => {
  const team = project.value?.team;
  if (!team) return false;
  return team.ketuaTimId === user?.id;
});


// --- FUNGSI UTAMA ---
const fetchDetailProject = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${baseURL}/api/projects/${projectId}`);
    project.value = response.data;
    breadcrumbItems.value[2].text = project.value?.namaProject ?? 'Detail Project';
    console.log("Detail Project : ", response.data);
  } catch (error) {
    const message = error.response?.data?.message || "Gagal memuat detail Project.";
    toast.error(message);
    console.error("Fetch detail Project error:", error);
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
  } catch (error) {
    toast.error("Gagal memuat daftar tim.");
    console.error("Gagal mengambil data tim:", error);
  }
};

onMounted(() => { 
  fetchDetailProject(); 
  fetchTeams();
});

// --- Logika untuk Project (Edit/Hapus) ---
const openEditModal = () => { isEditModalOpen.value = true; };
const closeEditModal = () => { isEditModalOpen.value = false; };
const handleUpdateProject = async (formData) => {
  try {
    await axios.put(`${baseURL}/api/projects/${projectId}`, formData);
    toast.success("Project berhasil diperbarui!");
    closeEditModal();
    await fetchDetailProject();
  } catch (error) {
    const errorMsg = error.response?.data?.detail?.[0]?.msg || "Gagal memperbarui Project.";
    toast.error(errorMsg);
  }
};

const confirmDeleteProject = () => { 
  if (window.confirm("Yakin ingin hapus Project ini? Semua data terkait akan ikut terhapus.")) deleteProject(); 
};

const deleteProject = async () => {
  try {
    await axios.delete(`${baseURL}/api/projects/${projectId}`);
    toast.success("Project berhasil dihapus.");
    router.push('/project');
  } catch (error) { 
    toast.error("Gagal menghapus Project."); 
  }
};

// --- Logika untuk Dokumen (Umum) ---
const confirmDeleteDokumen = (dokumenId) => { 
  if (window.confirm("Yakin ingin hapus dokumen ini?")) deleteDokumen(dokumenId); 
};
const deleteDokumen = async (dokumenId) => {
  try {
    await axios.delete(`${baseURL}/api/dokumen/${dokumenId}`);
    toast.success("Dokumen berhasil dihapus.");
    await fetchDetailProject();
  } catch (error) {
    toast.error("Gagal menghapus dokumen.");
  }
};

// --- Logika untuk Tambah Link ---
const openLinkModal = () => { isLinkModalOpen.value = true; };
const closeLinkModal = () => { isLinkModalOpen.value = false; };
const handleLinkSubmit = async (formData) => {
  try {
    await axios.post(`${baseURL}/api/projects/${projectId}/links`, formData);
    toast.success("Link berhasil ditambahkan.");
    closeLinkModal();
    await fetchDetailProject();
  } catch (error) { toast.error("Gagal menambahkan link."); }
};

// --- Logika untuk Unggah File (via Dropzone) ---
const closeFileModal = () => { 
  isFileModalOpen.value = false; 
  fileToUpload.value = null; 
};

const handleFileReadyForUpload = (file) => {
  fileToUpload.value = file;
  isFileModalOpen.value = true;
};

const handleFileUploadSubmit = async (formData) => {
  const data = new FormData();
  data.append('file', formData.file);
  data.append('keterangan', formData.keterangan);
  try {
    console.log("Data : ", data);
    await axios.post(`${baseURL}/api/projects/${projectId}/dokumen`, data);
    toast.success("File berhasil diunggah.");
    closeFileModal();
    await fetchDetailProject();
  } catch (error) { 
    toast.error("Gagal mengunggah file"); 
  }
};

// --- Logika untuk Preview/Unduh Dokumen ---
const openPreviewModal = () => { isPreviewModalOpen.value = true; };
const closePreviewModal = () => {
  if (fileToPreview.value.url) {
    window.URL.revokeObjectURL(fileToPreview.value.url);
  }
  isPreviewModalOpen.value = false;
  fileToPreview.value = { url: '', name: '', type: '' };
};

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
    
    openPreviewModal();
  } catch (error) {
    toast.error("Gagal membuka file untuk preview.");
    console.error(error);
  }
};

const handleDownloadAll = async () => {
  // Pengecekan keamanan tambahan
  if (!project.value || !project.value.dokumen) {
    toast.warning("Data Project tidak ditemukan.");
    return;
  }
  
  const filesToDownload = project.value.dokumen.filter(d => d.tipe === 'FILE');

  if (filesToDownload.length === 0) {
    toast.warning("Tidak ada file yang bisa diunduh untuk Project ini.");
    return; 
  }

  if (window.confirm(`Apakah Anda yakin ingin mengunduh semua file untuk Project ini?`)) {
    const toastId = toast.info("Sedang mempersiapkan file ZIP, mohon tunggu...", { timeout: false });
    
    try {
      const response = await axios.get(`${baseURL}/api/projects/${projectId}/download-all`, {
        responseType: 'blob',
        timeout: 60000,
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      let fileName = `${project.value.namaProject || 'dokumen'}.zip`;
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
</script>