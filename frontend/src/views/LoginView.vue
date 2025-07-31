<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
    <div class="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg">

      <div>
        <img class="mx-auto h-20 w-auto" src="/logo.png" alt="SINERGI BPS NTB Logo" />
        <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
          Selamat Datang di SINERGI
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Silakan masuk untuk melanjutkan
        </p>
      </div>

      <div class="space-y-6">
        <button class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-orange-400 hover:bg-orange-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Masuk dengan Akun Pegawai (SSO)
        </button>

        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">atau</span>
          </div>
        </div>

        <form class="space-y-6" @submit.prevent="handleSubmit">
        <div v-if="errorMessage" class="p-3 bg-red-100 dark:bg-red-900/50 border border-red-300 dark:border-red-700 rounded-md">
          <p class="text-sm text-red-700 dark:text-red-300">{{ errorMessage }}</p>
        </div>

        <div>
          <label for="username" class="sr-only">Username</label>
          <input 
            id="username"
            type="text" 
            v-model="username"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-700 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Username"
          />
        </div>
        <div>
          <label for="password" class="sr-only">Password</label>
          <input 
            id="password"
            type="password" 
            v-model="password"
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-700 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Password"
          />
        </div>
        
        <button 
          type="submit"
          :disabled="isLoading"
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-400 disabled:cursor-not-allowed"
        >
          {{ isLoading ? 'Memproses...' : 'Masuk' }}
        </button>
      </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

// State untuk menampung input dari form
const username = ref('');
const password = ref('');

// State untuk menampilkan pesan error dan status loading
const errorMessage = ref(null);
const isLoading = ref(false);

const handleSubmit = async () => {
  isLoading.value = true;
  errorMessage.value = null;

  const success = await authStore.login(username.value, password.value);

  if (!success) {
    errorMessage.value = 'Username atau password salah.';
  }
  
  isLoading.value = false;
};
</script>