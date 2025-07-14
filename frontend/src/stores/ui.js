import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', () => {
  // 'state' untuk melacak status sidebar
  const isSidebarOpen = ref(true)

  // 'action' untuk mengubah state
  function toggleSidebar() {
    isSidebarOpen.value = !isSidebarOpen.value
  }

  function closeSidebar() {
    // Hanya tutup jika di layar mobile
    if (window.innerWidth < 768) {
      isSidebarOpen.value = false
    }
  }

  return { isSidebarOpen, toggleSidebar, closeSidebar }
})