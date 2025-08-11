import { defineStore } from 'pinia'

export const useApiKeyStore = defineStore('apiKeys', {
  state: () => ({
    gpt: '',
    claude: '',
    gemini: ''
  }),

  getters: {
    // 모든 API 키 반환
    getAllKeys: (state) => ({
      gpt: state.gpt,
      claude: state.claude,
      gemini: state.gemini
    }),

    // 특정 API 키 반환
    getKey: (state) => (provider) => state[provider] || '',

    // 설정된 API 키들만 반환
    getValidKeys: (state) => {
      const validKeys = {}
      Object.keys(state).forEach(key => {
        if (state[key] && state[key].trim() !== '') {
          validKeys[key] = state[key]
        }
      })
      return validKeys
    },

    // 설정된 API 키 개수
    getValidKeyCount: (state) => {
      return Object.values(state).filter(key => key && key.trim() !== '').length
    }
  },

  actions: {
    // API 키 설정
    setKey(provider, key) {
      if (this[provider] !== undefined) {
        this[provider] = key
      }
    },

    // 모든 API 키 설정
    setAllKeys(keys) {
      Object.keys(keys).forEach(provider => {
        if (this[provider] !== undefined) {
          this[provider] = keys[provider]
        }
      })
    },

    // 특정 API 키 삭제
    clearKey(provider) {
      if (this[provider] !== undefined) {
        this[provider] = ''
      }
    },

    // 모든 API 키 삭제
    clearAllKeys() {
      this.gpt = ''
      this.claude = ''
      this.gemini = ''
    },

    // API 키 유효성 검사 (백엔드와 동일한 기준)
    isValidKey(provider, key = null) {
      const keyToCheck = key || this[provider]
      if (!keyToCheck || keyToCheck.trim() === '') return false

      const trimmedKey = keyToCheck.trim()

      // 각 API별 기본 유효성 검사 (실제 형식에 맞춤)
      switch (provider) {
        case 'gpt':
          // OpenAI: sk- 시작, 최소 48자 (기본) 또는 sk-proj- 시작
          return (trimmedKey.startsWith('sk-') && trimmedKey.length >= 48) ||
                 (trimmedKey.startsWith('sk-proj-') && trimmedKey.length >= 56)
        case 'claude':
          // Anthropic: sk-ant- 시작, 최소 80자
          return trimmedKey.startsWith('sk-ant-') && trimmedKey.length >= 80
        case 'gemini':
          // Google: AIza 시작, 정확히 39자
          return trimmedKey.startsWith('AIza') && trimmedKey.length === 39
        default:
          return false
      }
    }
  }
})