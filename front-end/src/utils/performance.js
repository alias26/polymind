/**
 * 성능 최적화 유틸리티 함수들
 */

/**
 * Debounce 함수 - 연속된 호출을 지연시켜 성능 향상
 * @param {Function} func - 실행할 함수
 * @param {number} wait - 지연 시간 (ms)
 * @returns {Function} debounced 함수
 */
export function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * Throttle 함수 - 일정 시간 간격으로만 함수 실행
 * @param {Function} func - 실행할 함수
 * @param {number} limit - 제한 시간 (ms)
 * @returns {Function} throttled 함수
 */
export function throttle(func, limit) {
  let inThrottle
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

/**
 * 가상 스크롤링을 위한 가시 영역 아이템 계산
 * @param {Array} items - 전체 아이템 배열
 * @param {number} containerHeight - 컨테이너 높이
 * @param {number} itemHeight - 각 아이템 높이
 * @param {number} scrollTop - 현재 스크롤 위치
 * @param {number} buffer - 버퍼 아이템 수 (성능을 위한 여유분)
 * @returns {Object} 가시 영역 정보
 */
export function getVisibleRange(items, containerHeight, itemHeight, scrollTop, buffer = 5) {
  const totalItems = items.length
  const visibleCount = Math.ceil(containerHeight / itemHeight)
  
  const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - buffer)
  const endIndex = Math.min(totalItems - 1, startIndex + visibleCount + buffer * 2)
  
  return {
    startIndex,
    endIndex,
    visibleItems: items.slice(startIndex, endIndex + 1),
    offsetY: startIndex * itemHeight,
    totalHeight: totalItems * itemHeight
  }
}

/**
 * 이미지 지연 로딩을 위한 Intersection Observer
 */
export class LazyImageLoader {
  constructor(options = {}) {
    this.options = {
      root: null,
      rootMargin: '50px',
      threshold: 0.1,
      ...options
    }
    
    this.observer = new IntersectionObserver(this.handleIntersection.bind(this), this.options)
  }
  
  observe(element) {
    this.observer.observe(element)
  }
  
  unobserve(element) {
    this.observer.unobserve(element)
  }
  
  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target
        const src = img.dataset.src
        
        if (src) {
          img.src = src
          img.removeAttribute('data-src')
          this.observer.unobserve(img)
        }
      }
    })
  }
  
  disconnect() {
    this.observer.disconnect()
  }
}

/**
 * 메모리 사용량 모니터링 (개발용)
 */
export function logMemoryUsage() {
  // 개발환경에서만 메모리 사용량 로깅
  if (process.env.NODE_ENV === 'development' && performance.memory) {
    // 메모리 사용량 체크 (로그 제거됨)
  }
}

/**
 * 컴포넌트 렌더링 성능 측정
 */
export function measureRenderPerformance(name, fn) {
  const startTime = performance.now()
  const result = fn()
  const endTime = performance.now()
  
  // 개발환경에서만 렌더링 성능 로깅
  if (process.env.NODE_ENV === 'development') {
    // 렌더링 성능 체크 (로그 제거됨)
  }
  return result
}

/**
 * 큰 목록의 성능을 위한 청크 처리
 * @param {Array} array - 처리할 배열
 * @param {number} chunkSize - 청크 크기
 * @param {Function} processor - 각 청크를 처리할 함수
 * @param {number} delay - 청크 간 지연 시간 (ms)
 */
export async function processInChunks(array, chunkSize, processor, delay = 0) {
  for (let i = 0; i < array.length; i += chunkSize) {
    const chunk = array.slice(i, i + chunkSize)
    await processor(chunk, i)
    
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
}

/**
 * 스크롤 성능 최적화를 위한 패시브 이벤트 리스너 체크
 */
export function supportsPassiveEvents() {
  let supportsPassive = false
  try {
    const opts = Object.defineProperty({}, 'passive', {
      get: function() {
        supportsPassive = true
        return true
      }
    })
    window.addEventListener('testPassive', null, opts)
    window.removeEventListener('testPassive', null, opts)
  } catch (e) {
    // 패시브 이벤트 지원 체크 중 에러 무시
  }
  
  return supportsPassive
}

/**
 * 리액티브 시스템 성능을 위한 얕은 비교
 * @param {Object} obj1 
 * @param {Object} obj2 
 * @returns {boolean}
 */
export function shallowEqual(obj1, obj2) {
  const keys1 = Object.keys(obj1)
  const keys2 = Object.keys(obj2)
  
  if (keys1.length !== keys2.length) {
    return false
  }
  
  for (let key of keys1) {
    if (obj1[key] !== obj2[key]) {
      return false
    }
  }
  
  return true
}