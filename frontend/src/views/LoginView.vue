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

        <div>
          <input 
            type="email" 
            placeholder="Alamat Email" 
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-700 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <input 
            type="password" 
            placeholder="Password" 
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-700 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <button class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-700 hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
          Masuk
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
// Logika untuk login (termasuk SSO) akan ditambahkan di sini
</script>