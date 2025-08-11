// API 및 모델별 설정 범위 정의
export const MODEL_SETTINGS = {
  // OpenAI GPT
  openai: {
    name: 'OpenAI',
    models: {
      // GPT-5 시리즈 (Limited Access) - temperature 고정(1)
      'gpt-5': {
        name: 'GPT-5',
        temperature: { min: 1, max: 1, step: 0.1, default: 1.0, fixed: true },
        maxTokens: { min: 1, max: 128000, default: 4096 },
        description: 'OpenAI 최신 모델 (제한적 액세스)',
      },
      'gpt-5-mini': {
        name: 'GPT-5 Mini',
        temperature: { min: 1, max: 1, step: 0.1, default: 1.0, fixed: true },
        maxTokens: { min: 1, max: 128000, default: 4096 },
        description: 'OpenAI 최신 모델 mini (제한적 액세스)',
      },
      'gpt-5-nano': {
        name: 'GPT-5 Nano',
        temperature: { min: 1, max: 1, step: 0.1, default: 1.0, fixed: true },
        maxTokens: { min: 1, max: 128000, default: 4096 },
        description: 'OpenAI 최신 모델 nano (제한적 액세스)',
      },
      'gpt-5-chat': {
        name: 'GPT-5 Chat',
        temperature: { min: 1, max: 1, step: 0.1, default: 1.0, fixed: true },
        maxTokens: { min: 1, max: 128000, default: 4096 },
        description: 'OpenAI 최신 모델 chat (제한적 액세스)',
      },
      // GPT-4.1 시리즈 (특정 버전)
      'gpt-4.1': {
        name: 'GPT-4.1',
        temperature: { min: 0, max: 2, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 32768, default: 4096 },
        description: 'OpenAI 최신 코딩 특화 모델',
      },
      'gpt-4.1-mini': {
        name: 'GPT-4.1 Mini',
        temperature: { min: 0, max: 2, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 32768, default: 4096 },
        description: '빠르고 효율적인 GPT-4.1',
      },
      'gpt-4.1-nano': {
        name: 'GPT-4.1 Nano',
        temperature: { min: 0, max: 2, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 32768, default: 2048 },
        description: '초소형 고효율 모델',
      },

      // o-시리즈 추론 모델
      o3: {
        name: 'o3',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.5 },
        maxTokens: { min: 1, max: 100000, default: 4096 },
        description: '강력한 추론 모델',
      },
      'o4-mini': {
        name: 'o4-mini',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.5 },
        maxTokens: { min: 1, max: 100000, default: 4096 },
        description: '빠른 추론 최적화 모델',
      },

      // GPT-4o 시리즈 (특정 버전)
      'gpt-4o': {
        name: 'GPT-4o',
        temperature: { min: 0, max: 2, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 16384, default: 4096 },
        description: '멀티모달 GPT-4',
      },
      'gpt-4o-mini': {
        name: 'GPT-4o Mini',
        temperature: { min: 0, max: 2, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 16384, default: 2048 },
        description: '효율적인 GPT-4o',
      },

      // GPT-3.5 시리즈
      'gpt-3.5-turbo': {
        name: 'GPT-3.5 Turbo',
        temperature: { min: 0, max: 2, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 4096, default: 2048 },
        description: '빠르고 비용 효율적인 모델',
      },
    },
  },

  // Anthropic Claude
  anthropic: {
    name: 'Claude',
    models: {
      // Claude 4 시리즈 (특정 버전)
      'claude-opus-4-1-20250805': {
        name: 'Claude Opus 4.1',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.3 },
        maxTokens: { min: 1, max: 32000, default: 4096 },
        description: '가장 강력하고 지능적인 Claude 모델',
      },
      'claude-opus-4-20250514': {
        name: 'Claude Opus 4',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.3 },
        maxTokens: { min: 1, max: 32000, default: 4096 },
        description: 'Claude 4세대 최고 성능 모델',
      },
      'claude-sonnet-4-20250514': {
        name: 'Claude Sonnet 4',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 64000, default: 8192 },
        description: 'Claude 4세대 균형잡힌 고성능 모델',
      },

      // Claude 3.7 시리즈 (특정 버전)
      'claude-3-7-sonnet-20250219': {
        name: 'Claude Sonnet 3.7',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 64000, default: 8192 },
        description: '하이브리드 AI 추론 모델',
      },

      // Claude 3.5 시리즈 (특정 버전)
      'claude-3-5-sonnet-20241022': {
        name: 'Claude Sonnet 3.5',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 8192, default: 8192 },
        description: '뛰어난 추론과 코딩 능력',
      },
      'claude-3-5-haiku-20241022': {
        name: 'Claude Haiku 3.5',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 8192, default: 4096 },
        description: '빠르고 효율적인 모델',
      },

      // Claude 3 시리즈 (특정 버전)
      'claude-3-haiku-20240307': {
        name: 'Claude Haiku 3',
        temperature: { min: 0, max: 1, step: 0.1, default: 0.7 },
        maxTokens: { min: 1, max: 4096, default: 4096 },
        description: '빠르고 가벼운 모델',
      },
    },
  },

  // Google Gemini
  google: {
    name: 'Gemini',
    models: {
      // Gemini 2.5 시리즈 (특정 버전)
      'gemini-2.5-pro': {
        name: 'Gemini 2.5 Pro',
        temperature: { min: 0, max: 2, step: 0.1, default: 1.0 },
        maxTokens: { min: 1, max: 65536, default: 8192 },
        description: '최강 성능의 Gemini 모델',
      },
      'gemini-2.5-flash': {
        name: 'Gemini 2.5 Flash',
        temperature: { min: 0, max: 2, step: 0.1, default: 1.0 },
        maxTokens: { min: 1, max: 65536, default: 8192 },
        description: '빠르고 효율적인 Gemini',
      },
    },
  },
}

// 기본 설정값
export const DEFAULT_SETTINGS = {
  temperature: 0.7,
  maxTokens: 2048,
  systemPrompt: '당신은 도움이 되는 AI 어시스턴트입니다.',
}

// API 목록 가져오기
export const getApiList = () => {
  return Object.keys(MODEL_SETTINGS).map((apiKey) => ({
    key: apiKey,
    name: MODEL_SETTINGS[apiKey].name,
  }))
}

// 특정 API의 모델 목록 가져오기
export const getModelList = (apiKey) => {
  if (!MODEL_SETTINGS[apiKey]) return []

  return Object.keys(MODEL_SETTINGS[apiKey].models).map((modelKey) => ({
    key: modelKey,
    name: MODEL_SETTINGS[apiKey].models[modelKey].name,
    description: MODEL_SETTINGS[apiKey].models[modelKey].description,
  }))
}

// 특정 모델의 설정 범위 가져오기
export const getModelSettings = (apiKey, modelKey) => {
  if (!MODEL_SETTINGS[apiKey] || !MODEL_SETTINGS[apiKey].models[modelKey]) {
    return DEFAULT_SETTINGS
  }

  return MODEL_SETTINGS[apiKey].models[modelKey]
}

// 현재 채팅의 API 감지 (임시 Anthropic으로 고정)
export const getCurrentApi = () => {
  return 'anthropic'
}

// 모델 키로 API 감지
export const getApiFromModel = (modelKey) => {
  for (const [apiKey, apiConfig] of Object.entries(MODEL_SETTINGS)) {
    if (apiConfig.models[modelKey]) {
      return apiKey
    }
  }
  return 'anthropic' // 기본값
}

// 설정값이 유효한지 검증
export const validateSettings = (apiKey, modelKey, settings) => {
  const modelSettings = getModelSettings(apiKey, modelKey)
  const errors = []

  // Temperature 검증
  if (
    settings.temperature < modelSettings.temperature.min ||
    settings.temperature > modelSettings.temperature.max
  ) {
    errors.push(
      `Temperature는 ${modelSettings.temperature.min}-${modelSettings.temperature.max} 범위여야 합니다.`
    )
  }

  // MaxTokens 검증
  if (
    settings.maxTokens < modelSettings.maxTokens.min ||
    settings.maxTokens > modelSettings.maxTokens.max
  ) {
    errors.push(
      `최대 토큰은 ${modelSettings.maxTokens.min}-${modelSettings.maxTokens.max} 범위여야 합니다.`
    )
  }

  return {
    isValid: errors.length === 0,
    errors,
  }
}
