<template>
  <div class="min-h-screen py-10 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto space-y-8">
      <!-- Header -->
      <div class="flex flex-col items-center space-y-4">
        <ProfilePicture
          :user="authStore"
        />
        <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-gray-100">
          Profil Saya
        </h1>
        <p class="text-gray-500 dark:text-gray-400 text-center text-sm sm:text-base">
          Kelola informasi akun dan keamanan Anda
        </p>
      </div>

      <!-- Card 1: Informasi Akun -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-2xl p-6 transition hover:shadow-lg">
        <h2 class="text-lg sm:text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
          Informasi Akun
        </h2>
        <div class="space-y-3">
          <div class="flex justify-between text-sm sm:text-base">
            <span class="text-gray-600 dark:text-gray-400">Username</span>
            <span class="font-medium text-gray-900 dark:text-gray-100">{{ authStore.user?.username }}</span>
          </div>
          <div class="flex justify-between text-sm sm:text-base">
            <span class="text-gray-600 dark:text-gray-400">Nama Lengkap</span>
            <span class="font-medium text-gray-900 dark:text-gray-100">{{ authStore.user?.namaLengkap  }}</span>
          </div>
          <div v-if="user.role_sistem === 'admin' || user.role_sistem === 'superadmin'" 
               class="flex justify-between text-sm sm:text-base">
            <span class="text-gray-600 dark:text-gray-400">Role Sistem</span>
            <span class="font-medium text-gray-900 dark:text-gray-100">{{ user.role_sistem }}</span>
          </div>
          <div v-for="(tim, index) in user.tim_aktif" :key="index" 
               class="flex justify-between text-sm sm:text-base">
            <span class="text-gray-600 dark:text-gray-400">Tim {{ index + 1 }}</span>
            <span class="font-medium text-gray-900 dark:text-gray-100">
              {{ tim.nama }} ({{ tim.jabatan }})
            </span>
          </div>
        </div>
      </div>
      
      <!-- Card 2: Ganti Password -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-2xl p-6 transition hover:shadow-lg">
        <h2 class="text-lg sm:text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">
          Ganti Password
        </h2>
        <form @submit.prevent="updatePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Password Lama</label>
            <input 
              v-model="form.oldPassword" 
              type="password"
              required
              class="mt-1 block w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 focus:ring-blue-500 focus:border-blue-500 sm:text-sm p-2"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Password Baru</label>
            <input 
              v-model="form.newPassword" 
              type="password"
              required
              class="mt-1 block w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 focus:ring-blue-500 focus:border-blue-500 sm:text-sm p-2"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Konfirmasi Password Baru</label>
            <input 
              v-model="form.confirmPassword" 
              type="password"
              required
              class="mt-1 block w-full rounded-xl border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100 focus:ring-blue-500 focus:border-blue-500 sm:text-sm p-2"
            />
          </div>
          <button 
            type="submit" 
            class="w-full inline-flex justify-center py-2 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none transition duration-200">
            Simpan Password
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import ProfilePicture from "@/components/profile/ProfilePicture.vue";
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const user = ref({
  id: null,
  username: "",
  namaLengkap: "",
  roleSistem: "",
  foto_profil_url: "",
  tim_aktif: []
});

const form = ref({
  oldPassword: "",
  newPassword: "",
  confirmPassword: ""
});

const updatePassword = async () => {
  if (form.value.newPassword !== form.value.confirmPassword) {
    alert("Password baru dan konfirmasi tidak cocok");
    return;
  }
  try {
    await axios.put(`http://127.0.0.1:8000/api/users/${user.value.id}/password`, {
      oldPassword: form.value.oldPassword,
      newPassword: form.value.newPassword
    });
    alert("Password berhasil diperbarui");
    form.value = { oldPassword: "", newPassword: "", confirmPassword: "" };
  } catch (err) {
    alert("Gagal memperbarui password");
    console.error(err);
  }
};

</script>
