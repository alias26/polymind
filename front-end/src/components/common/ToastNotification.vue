<template>
  <Transition name="toast" appear>
    <div 
      v-if="visible" 
      :class="[
        'toast-notification',
        `toast-${type}`,
        { 'toast-dismissible': dismissible }
      ]"
      @click="dismissible && close()"
    >
      <div class="toast-icon">
        <i :class="iconClass"></i>
      </div>
      <div class="toast-content">
        <div v-if="title" class="toast-title">{{ title }}</div>
        <div class="toast-message">{{ message }}</div>
      </div>
      <button 
        v-if="dismissible" 
        class="toast-close" 
        @click.stop="close()"
        aria-label="닫기"
      >
        <i class="fas fa-times"></i>
      </button>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'ToastNotification',
  props: {
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    title: {
      type: String,
      default: ''
    },
    message: {
      type: String,
      required: true
    },
    duration: {
      type: Number,
      default: 4000
    },
    dismissible: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      visible: true,
      timer: null
    }
  },
  computed: {
    iconClass() {
      const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
      }
      return icons[this.type] || icons.info
    }
  },
  mounted() {
    if (this.duration > 0) {
      this.timer = setTimeout(() => {
        this.close()
      }, this.duration)
    }
  },
  beforeUnmount() {
    if (this.timer) {
      clearTimeout(this.timer)
    }
  },
  methods: {
    close() {
      this.visible = false
      setTimeout(() => {
        this.$emit('close')
      }, 300)
    }
  }
}
</script>

<style scoped>
.toast-notification {
  display: flex;
  align-items: center;
  min-width: 320px;
  max-width: 500px;
  padding: 12px 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.toast-notification::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 4px;
  height: 100%;
}

.toast-success {
  background: rgba(16, 185, 129, 0.9);
  color: white;
}

.toast-success::before {
  background: #10b981;
}

.toast-error {
  background: rgba(239, 68, 68, 0.9);
  color: white;
}

.toast-error::before {
  background: #ef4444;
}

.toast-warning {
  background: rgba(245, 158, 11, 0.9);
  color: white;
}

.toast-warning::before {
  background: #f59e0b;
}

.toast-info {
  background: rgba(59, 130, 246, 0.9);
  color: white;
}

.toast-info::before {
  background: #3b82f6;
}

.toast-icon {
  margin-right: 12px;
  font-size: 20px;
  flex-shrink: 0;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}

.toast-message {
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
}

.toast-close {
  background: none;
  border: none;
  color: inherit;
  padding: 4px;
  margin-left: 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  flex-shrink: 0;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.2);
}

.toast-dismissible:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

/* 트랜지션 애니메이션 */
.toast-enter-active {
  transition: all 0.3s ease-out;
}

.toast-leave-active {
  transition: all 0.3s ease-in;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.9);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.9);
}
</style>