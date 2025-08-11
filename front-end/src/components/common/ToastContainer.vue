<template>
  <Teleport to="body">
    <div class="toast-container">
      <ToastNotification
        v-for="toast in toasts"
        :key="toast.id"
        :type="toast.type"
        :title="toast.title"
        :message="toast.message"
        :duration="toast.duration"
        :dismissible="toast.dismissible"
        @close="removeToast(toast.id)"
      />
    </div>
  </Teleport>
</template>

<script>
import { ref, onMounted } from 'vue'
import ToastNotification from './ToastNotification.vue'
import { toastService } from '../../utils/toastService.js'

export default {
  name: 'ToastContainer',
  components: {
    ToastNotification
  },
  setup() {
    const toasts = ref([])

    const addToast = (toast) => {
      toasts.value.push(toast)
    }

    const removeToast = (id) => {
      const index = toasts.value.findIndex(t => t.id === id)
      if (index > -1) {
        toasts.value.splice(index, 1)
      }
    }

    onMounted(() => {
      toastService.setAddToastFunction(addToast)
    })

    return {
      toasts,
      removeToast
    }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: var(--z-toast);
  pointer-events: none;
}

.toast-container > * {
  pointer-events: auto;
}

@media (max-width: 640px) {
  .toast-container {
    top: 10px;
    right: 10px;
    left: 10px;
  }
  
  .toast-container :deep(.toast-notification) {
    min-width: auto;
    max-width: none;
  }
}
</style>