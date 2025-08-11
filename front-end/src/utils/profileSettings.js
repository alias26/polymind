import { DEFAULT_SETTINGS } from '@/config/modelSettings'
import { userPreferencesApi } from '@/apis/userPreferencesApi'

/**
 * 프로필에서 저장한 기본 프리셋을 가져옵니다 (동기 버전)
 * @returns {Object} 기본 프리셋 설정
 */
export const getDefaultPresetSettings = () => {
  try {
    const saved = localStorage.getItem('defaultPresetSettings')
    if (saved) {
      const parsed = JSON.parse(saved)
      return {
        temperature: parsed.temperature || DEFAULT_SETTINGS.temperature,
        maxTokens: parsed.maxTokens || DEFAULT_SETTINGS.maxTokens,
        selectedApi: parsed.selectedApi || 'anthropic',
        selectedModel: parsed.selectedModel || 'Sonnet4'
      }
    }
  } catch (error) {
    console.error('기본 프리셋 로드 오류:', error)
  }
  
  // 저장된 설정이 없거나 오류 발생시 기본값 반환
  return {
    temperature: DEFAULT_SETTINGS.temperature,
    maxTokens: DEFAULT_SETTINGS.maxTokens,
    selectedApi: 'anthropic',
    selectedModel: 'Sonnet4'
  }
}

/**
 * 프로필에서 저장한 기본 프리셋을 서버에서 가져옵니다 (비동기 버전)
 * @returns {Promise<Object>} 기본 프리셋 설정
 */
export const getDefaultPresetSettingsAsync = async () => {
  try {
    // 서버에서 프리셋 설정 로드 시도
    const serverPreferences = await userPreferencesApi.getUserPreferences()
    
    if (serverPreferences && (serverPreferences.default_api || serverPreferences.default_model)) {
      const serverSettings = {
        selectedApi: serverPreferences.default_api || 'anthropic',
        selectedModel: serverPreferences.default_model || 'Sonnet4',
        temperature: serverPreferences.default_temperature || DEFAULT_SETTINGS.temperature,
        maxTokens: serverPreferences.default_max_tokens || DEFAULT_SETTINGS.maxTokens
      }
      
      
      // 서버 설정을 로컬스토리지에도 동기화
      localStorage.setItem('defaultPresetSettings', JSON.stringify(serverSettings))
      return serverSettings
    } else {
    }
  } catch (error) {
    console.error('서버에서 기본 프리셋 로드 오류:', error)
  }
  
  // 서버 로드 실패 시 로컬스토리지에서 로드
  const localSettings = getDefaultPresetSettings()
  return localSettings
}

/**
 * 프로필에서 저장한 기본 프롬프트를 가져옵니다 (기본 프롬프트 탭에서)
 * @returns {string} 기본 시스템 프롬프트
 */
export const getDefaultSystemPrompt = () => {
  // 기본 프롬프트 탭에서 저장된 설정 확인
  try {
    const saved = localStorage.getItem('defaultPromptSettings')
    if (saved) {
      const parsed = JSON.parse(saved)
      return parsed.systemPrompt || DEFAULT_SETTINGS.systemPrompt
    }
  } catch (error) {
    console.error('기본 프롬프트 로드 오류:', error)
  }
  
  // 저장된 설정이 없거나 오류 발생시 기본값 반환
  return DEFAULT_SETTINGS.systemPrompt
}

/**
 * 모든 기본 설정을 통합해서 가져옵니다 (동기 버전)
 * @returns {Object} 통합된 기본 설정 (프리셋만)
 */
export const getAllDefaultSettings = () => {
  return getDefaultPresetSettings()
}

/**
 * 모든 기본 설정을 통합해서 가져옵니다 (비동기 버전)
 * @returns {Promise<Object>} 통합된 기본 설정 (프리셋만)
 */
export const getAllDefaultSettingsAsync = async () => {
  return await getDefaultPresetSettingsAsync()
}