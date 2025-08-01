<template>
  <div class="relative h-screen w-screen overflow-hidden">
    <div 
      class="absolute inset-0 bg-cover bg-center z-0"
      style="background-image: url('/kantor-bg.jpg');"
    ></div>

    <div class="absolute inset-0 bg-white/20 dark:bg-black/80 z-10"></div>

    <div class="relative z-20 flex flex-col items-center justify-center h-full text-center text-white px-4">

      <img src="/logo.png" alt="Logo SINERGI" class="h-50 w-auto mb-4">

      <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight">
        Selamat Datang di <span class="text-blue-400">SI</span><span class="text-green-400">NER</span><span class="text-orange-400">GI</span>
      </h1>

      <p class="mt-4 max-w-2xl text-lg text-gray-200">
        Sebuah platform terintegrasi untuk meningkatkan produktivitas dan kolaborasi seluruh pegawai BPS Provinsi Nusa Tenggara Barat.
      </p>

      <router-link 
        to="/login" 
        class="mt-8 inline-block bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-lg shadow-lg transition-transform duration-200 hover:scale-105"
      >
        Masuk Aplikasi
      </router-link>
    </div>
  </div>
</template>

<script setup>
// Tidak perlu ada logika JavaScript untuk halaman statis ini
</script>