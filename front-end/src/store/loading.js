import { defineStore } from 'pinia'

/**
 * 전역 로딩 상태 관리 스토어
 * 여러 컴포넌트에서 일관된 로딩 UI를 제공하기 위한 중앙화된 스토어
 */
export const useLoadingStore = defineStore('loading', {
  state: () => ({
    // 전역 로딩 상태
    isGlobalLoading: false,
    globalLoadingMessage: '',
    
    // 개별 작업별 로딩 상태 (여러 작업 동시 처리 가능)
    operations: new Map(),
    
    // 로딩 UI 설정
    showSpinner: true,
    showOverlay: true
  }),

  getters: {
    // 현재 진행 중인 작업이 있는지 확인
    hasActiveOperations: (state) => state.operations.size > 0,
    
    // 전역 로딩 또는 개별 작업 로딩 중인지 확인
    isLoading: (state) => state.isGlobalLoading || state.operations.size > 0,
    
    // 현재 표시할 로딩 메시지
    currentMessage: (state) => {
      if (state.isGlobalLoading) {
        return state.globalLoadingMessage
      }
      
      // 가장 최근에 시작된 작업의 메시지 반환
      const operations = Array.from(state.operations.values())
      if (operations.length > 0) {
        return operations[operations.length - 1].message
      }
      
      return ''
    },
    
    // 특정 작업이 로딩 중인지 확인
    isOperationLoading: (state) => (operationKey) => {
      return state.operations.has(operationKey)
    },
    
    // 진행 중인 모든 작업 목록
    activeOperations: (state) => Array.from(state.operations.keys())
  },

  actions: {
    /**
     * 전역 로딩 시작
     * @param {string} message - 로딩 메시지
     */
    startGlobalLoading(message = '로딩 중...') {
      this.isGlobalLoading = true
      this.globalLoadingMessage = message
    },

    /**
     * 전역 로딩 종료
     */
    stopGlobalLoading() {
      this.isGlobalLoading = false
      this.globalLoadingMessage = ''
    },

    /**
     * 특정 작업의 로딩 시작
     * @param {string} operationKey - 작업 식별키 (예: 'login', 'api-save', 'chat-send')
     * @param {string} message - 로딩 메시지
     */
    startOperation(operationKey, message = '처리 중...') {
      this.operations.set(operationKey, {
        message,
        startTime: Date.now()
      })
    },

    /**
     * 특정 작업의 로딩 종료
     * @param {string} operationKey - 작업 식별키
     */
    stopOperation(operationKey) {
      this.operations.delete(operationKey)
    },

    /**
     * 모든 작업 로딩 종료
     */
    stopAllOperations() {
      this.operations.clear()
    },

    /**
     * 모든 로딩 상태 초기화
     */
    reset() {
      this.isGlobalLoading = false
      this.globalLoadingMessage = ''
      this.operations.clear()
    },

    /**
     * 로딩 UI 설정 변경
     * @param {Object} config - UI 설정 { showSpinner, showOverlay }
     */
    updateConfig(config) {
      if (config.showSpinner !== undefined) {
        this.showSpinner = config.showSpinner
      }
      if (config.showOverlay !== undefined) {
        this.showOverlay = config.showOverlay
      }
    }
  }
})