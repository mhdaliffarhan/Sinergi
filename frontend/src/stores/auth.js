import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router';

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'));
  const user = ref(null);

  const isAuthenticated = computed(() => !!token.value);
  const userRole = computed(() => user.value?.sistemRole?.namaRole);

  function setToken(newToken) {
    localStorage.setItem('token', newToken);
    token.value = newToken;
    // SECARA OTOMATIS TAMBAHKAN TOKEN KE SEMUA REQUEST AXIOS
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
  }

  function removeToken() {
    localStorage.removeItem('token');
    token.value = null;
    user.value = null;
    // HAPUS TOKEN DARI SEMUA REQUEST AXIOS
    delete axios.defaults.headers.common['Authorization'];
  }

  // Jika token sudah ada saat halaman di-refresh, langsung atur header-nya
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`;
  }

  async function login(username, password) {
    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);
      const response = await axios.post('http://127.0.0.1:8000/token', params);

      setToken(response.data.accessToken);

      await fetchUser();
      await router.push('/dashboard');
      return true;
    } catch (error) {
      removeToken();
      return false;
    }
  }

  async function fetchUser() {
    if (!token.value) return;
    try {
      // Tidak perlu lagi menambahkan header secara manual di sini
      const response = await axios.get('http://127.0.0.1:8000/users/me');
      user.value = response.data;
    } catch (error) {
      if (error.response?.status === 401) {
        logout();
      }
    }
  }

  function logout() {
    removeToken();
    router.push('/login');
  }

  return { token, user, isAuthenticated, userRole, login, fetchUser, logout };
});