import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';
import { useToast } from 'vue-toastification';

export const useAuthStore = defineStore('auth', () => {
  // === STATE ===
  // State reaktif untuk menyimpan token dan data pengguna.
  // Token diambil dari localStorage agar sesi tetap ada saat halaman di-refresh.
  const token = ref(localStorage.getItem('token'));
  const user = ref(null);
  const toast = useToast();

  // === GETTERS ===
  // Computed property untuk memeriksa status login dengan mudah di komponen lain.
  const isAuthenticated = computed(() => !!token.value);
  const userRole = computed(() => user.value?.sistemRole?.namaRole);

  // === ACTIONS ===

  // Fungsi internal untuk menyimpan token ke state dan localStorage.
  function setToken(newToken) {
    localStorage.setItem('token', newToken);
    token.value = newToken;
  }

  // Fungsi internal untuk menghapus token.
  function removeToken() {
    localStorage.removeItem('token');
    token.value = null;
    user.value = null;
  }

  /**
   * Mengirim kredensial ke backend untuk login.
   * @param {string} username - Username pengguna.
   * @param {string} password - Password pengguna.
   * @returns {boolean} - True jika login berhasil, false jika gagal.
   */
  async function login(username, password) {
    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      const response = await axios.post('http://127.0.0.1:8000/token', params);

      // Ambil token dari respons API.
      // Dibuat fleksibel untuk menangani camelCase atau snake_case.
      const accessToken = response.data.accessToken || response.data.access_token;
      if (!accessToken) {
        throw new Error("Token tidak ditemukan di respons API.");
      }

      setToken(accessToken);

      // Setelah dapat token, langsung ambil data pengguna.
      await fetchUser();

      toast.success(`Login berhasil! Selamat datang, ${user.value.namaLengkap}.`);

      // Arahkan ke dashboard jika berhasil.
      await router.push('/dashboard');
      return true;
    } catch (error) {
      console.error("Login gagal:", error);
      removeToken();
      return false;
    }
  }

  /**
   * Mengambil detail pengguna yang sedang login menggunakan token.
   */
  async function fetchUser() {
    if (!token.value) return;

    try {
      const response = await axios.get('http://127.0.0.1:8000/users/me', {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      });
      user.value = response.data;
    } catch (error) {
      console.error("Gagal mengambil data pengguna:", error);
      // Jika token tidak valid (misal: kadaluarsa), otomatis logout.
      if (error.response && error.response.status === 401) {
        logout();
      }
    }
  }

  /**
   * Menghapus sesi login pengguna.
   */
  function logout() {
    removeToken();
    toast.success("Anda telah berhasil logout.");
    router.push('/login');
  }

  return {
    // State
    token,
    user,
    // Getters
    isAuthenticated,
    userRole,
    // Actions
    login,
    fetchUser,
    logout
  };
});