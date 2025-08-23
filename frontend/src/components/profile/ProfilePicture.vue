<template>
  <div class="flex flex-col items-center gap-5">
    <!-- Foto Profil -->
    <div class="relative group">
      <img
        :src="previewUrl || getProfileUrl(authStore.user?.fotoProfilUrl) || '/profile-default.png'"
        alt="Foto Profil"
        class="w-32 h-32 md:w-40 md:h-40 rounded-full object-cover border-4 border-gray-200 dark:border-gray-700 shadow-lg transition duration-300 group-hover:scale-105"
      />
      <!-- Overlay saat hover -->
      <div
        class="absolute inset-0 flex items-center justify-center gap-4 bg-black/50 opacity-0 group-hover:opacity-100 transition duration-300 rounded-full"
      >
        <!-- Ganti Foto -->
        <label
          for="file-upload"
          class="cursor-pointer p-2 rounded-full bg-blue-600 hover:bg-blue-700 text-white shadow-md transition"
        >
          ✏️
        </label>

        <!-- Hapus Foto -->
        <button
          v-if="authStore.user?.fotoProfilUrl"
          @click="deletePhoto"
          class="p-2 rounded-full bg-red-500 hover:bg-red-600 text-white shadow-md transition"
        >
          🗑️
        </button>
      </div>
    </div>

    <!-- Input File -->
    <input
      id="file-upload"
      type="file"
      class="hidden"
      accept="image/png, image/jpeg"
      @change="handleFileChange"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";
import { useToast } from "vue-toastification";

const authStore = useAuthStore();
const toast = useToast();

const previewUrl = ref(null);

// 🔗 Helper: normalisasi URL foto profil
const getProfileUrl = (path) => {
  if (!path) return null;
  if (path.startsWith("./")) {
    return `http://127.0.0.1:8000/${path.replace("./", "")}`;
  }
  return path;
};

const handleFileChange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  previewUrl.value = URL.createObjectURL(file);
  try {
    const formData = new FormData();
    formData.append("file", file);

    await axios.post(
      `http://127.0.0.1:8000/api/${authStore.user.id}/upload-photo`,
      formData,
      { headers: { "Content-Type": "multipart/form-data" } }
    );

    toast.success("Foto profil berhasil diperbarui");
    await authStore.fetchUser();
    previewUrl.value = null;
  } catch (err) {
    toast.error("Gagal mengunggah foto profil");
    console.error(err);
  }
};

// ❌ Hapus Foto
const deletePhoto = async () => {
  try {
    await axios.delete(
      `http://127.0.0.1:8000/api/${authStore.user.id}/delete-photo`
    );
    toast.success("Foto profil berhasil dihapus");
    previewUrl.value = null;
    await authStore.fetchUser();
  } catch (err) {
    toast.error("Gagal menghapus foto profil");
    console.error(err);
  }
};
</script>
