class ToastService {
  constructor() {
    this.addToastFunction = null
    this.toastIdCounter = 0
  }

  setAddToastFunction(fn) {
    this.addToastFunction = fn
  }

  show(options) {
    if (!this.addToastFunction) {
      console.error('ToastService: addToastFunction not set')
      return
    }

    const toast = {
      id: ++this.toastIdCounter,
      type: options.type || 'info',
      title: options.title || '',
      message: options.message || '',
      duration: options.duration !== undefined ? options.duration : 4000,
      dismissible: options.dismissible !== undefined ? options.dismissible : true
    }

    this.addToastFunction(toast)
    return toast.id
  }

  success(message, options = {}) {
    return this.show({
      type: 'success',
      message,
      ...options
    })
  }

  error(message, options = {}) {
    return this.show({
      type: 'error',
      message,
      duration: 6000, // 에러는 더 오래 보여줌
      ...options
    })
  }

  warning(message, options = {}) {
    return this.show({
      type: 'warning',
      message,
      ...options
    })
  }

  info(message, options = {}) {
    return this.show({
      type: 'info',
      message,
      ...options
    })
  }

  // API 키 관련 메시지들을 위한 편의 메서드들
  apiKeySaved(provider) {
    return this.success(`${provider.toUpperCase()} API 키가 저장되었습니다.`, {
      title: '저장 완료'
    })
  }

  apiKeyDeleted(provider) {
    return this.success(`${provider.toUpperCase()} API 키가 삭제되었습니다.`, {
      title: '삭제 완료'
    })
  }

  apiKeyError(message) {
    return this.error(message, {
      title: 'API 키 오류'
    })
  }

  promptSaved() {
    return this.success('프롬프트가 저장되었습니다.', {
      title: '저장 완료'
    })
  }

  promptError() {
    return this.error('프롬프트 저장 중 오류가 발생했습니다.', {
      title: '저장 실패'
    })
  }

  promptRestored() {
    return this.success('프롬프트가 초기값으로 복원되었습니다.', {
      title: '복원 완료'
    })
  }

  presetSaved() {
    return this.success('프리셋이 저장되었습니다.', {
      title: '저장 완료'
    })
  }

  presetError() {
    return this.error('프리셋 저장 중 오류가 발생했습니다.', {
      title: '저장 실패'
    })
  }

  presetRestored() {
    return this.success('프리셋이 초기값으로 복원되었습니다.', {
      title: '복원 완료'
    })
  }

  signUpSuccess() {
    return this.success('회원가입이 완료되었습니다!', {
      title: '회원가입 완료'
    })
  }

  emailVerificationSent() {
    return this.info('인증 코드가 이메일로 전송되었습니다.', {
      title: '인증 코드 전송'
    })
  }

  emailVerificationComplete() {
    return this.success('이메일 인증이 완료되었습니다.', {
      title: '인증 완료'
    })
  }

  invalidApiKey() {
    return this.error('유효하지 않은 API 키입니다.', {
      title: '유효성 검사 실패'
    })
  }
}

export const toastService = new ToastService()
export default toastService