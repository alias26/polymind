<template>
  <div class="simple-markdown" v-html="renderedContent"></div>
</template>

<script setup>
import { computed, ref } from 'vue'
import MarkdownIt from 'markdown-it'
import DOMPurify from 'dompurify'

const props = defineProps({
  content: {
    type: String,
    required: true
  }
})

// 🚀 성능 최적화: 싱글톤 MarkdownIt 인스턴스
let mdInstance = null
function getMarkdownInstance() {
  if (!mdInstance) {
    mdInstance = new MarkdownIt({
      html: true, // HTML 태그 허용
      breaks: true, // 줄바꿈을 <br>로 변환
      linkify: true, // URL을 자동으로 링크로 변환
    })
  }
  return mdInstance
}

// 🚀 성능 최적화: 렌더링 결과 캐싱
const renderCache = new Map()
const MAX_CACHE_SIZE = 100 // 최대 100개 메시지 캐시

const renderedContent = computed(() => {
  if (!props.content || typeof props.content !== 'string') {
    return ''
  }

  // 🚀 캐시 확인 (해시키 생성)
  const contentHash = hashString(props.content)
  if (renderCache.has(contentHash)) {
    return renderCache.get(contentHash)
  }

  try {
    let content = props.content
    
    // 코드 블록이 아닌 경우에만 HTML 이스케이프 해제
    if (!content.includes('```') && (content.includes('&lt;table') || content.includes('&lt;/table&gt;'))) {
      content = content
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&amp;/g, '&')
    }
    
    // markdown-it으로 렌더링
    const md = getMarkdownInstance()
    const html = md.render(content)

    // HTML 새니타이징 (설정 재사용)
    const sanitized = DOMPurify.sanitize(html, getSanitizeConfig())
    
    // 🚀 캐시에 저장 (LRU 방식)
    if (renderCache.size >= MAX_CACHE_SIZE) {
      const firstKey = renderCache.keys().next().value
      renderCache.delete(firstKey)
    }
    renderCache.set(contentHash, sanitized)
    
    return sanitized
  } catch (error) {
    console.error('MarkdownRenderer error:', error)
    // 오류 시 원본 텍스트 반환 (HTML 이스케이프)
    return props.content.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>')
  }
})

// 🚀 성능 최적화: DOMPurify 설정 재사용
let sanitizeConfig = null
function getSanitizeConfig() {
  if (!sanitizeConfig) {
    sanitizeConfig = {
      ALLOWED_TAGS: [
        'strong', 'em', 'code', 'pre', 'br', 'p',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'blockquote', 'a'
      ],
      ALLOWED_ATTR: ['href', 'class', 'style'],
      KEEP_CONTENT: true
    }
  }
  return sanitizeConfig
}

// 🚀 간단한 해시 함수 (문자열 → 숫자)
function hashString(str) {
  let hash = 0
  if (str.length === 0) return hash
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // 32bit 정수 변환
  }
  return hash
}
</script>

<style scoped>
.simple-markdown {
  line-height: 1.6;
  font-family: inherit;
}

/* 헤딩 */
.simple-markdown :deep(h1) {
  font-size: 1.5em;
  font-weight: bold;
  margin: 0.5em 0 0.3em 0;
  color: #1f2937;
}

.simple-markdown :deep(h2) {
  font-size: 1.3em;
  font-weight: bold;
  margin: 0.4em 0 0.25em 0;
  color: #374151;
}

.simple-markdown :deep(h3) {
  font-size: 1.2em;
  font-weight: bold;
  margin: 0.35em 0 0.2em 0;
  color: #374151;
}

.simple-markdown :deep(h4) {
  font-size: 1.1em;
  font-weight: bold;
  margin: 0.3em 0 0.15em 0;
  color: #4b5563;
}

.simple-markdown :deep(h5) {
  font-size: 1.05em;
  font-weight: bold;
  margin: 0.25em 0 0.1em 0;
  color: #4b5563;
}

.simple-markdown :deep(h6) {
  font-size: 1em;
  font-weight: bold;
  margin: 0.2em 0 0.1em 0;
  color: #6b7280;
}

/* 문단 */
.simple-markdown :deep(p) {
  margin: 0.5em 0;
}

/* 코드 */
.simple-markdown :deep(pre) {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  margin: 0.5rem 0;
}

.simple-markdown :deep(code) {
  background: #f5f5f5;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.simple-markdown :deep(pre code) {
  background: none;
  padding: 0;
}

/* 텍스트 강조 */
.simple-markdown :deep(strong) {
  font-weight: bold;
}

.simple-markdown :deep(em) {
  font-style: italic;
}

/* 리스트 */
.simple-markdown :deep(ul), 
.simple-markdown :deep(ol) {
  margin: 0.5em 0;
  padding-left: 1.5em;
}

.simple-markdown :deep(li) {
  margin: 0.2em 0;
}

/* 테이블 */
.simple-markdown :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 0.8rem 0;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.simple-markdown :deep(th) {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
}

.simple-markdown :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  color: #6b7280;
}

.simple-markdown :deep(tbody tr:nth-child(even)) {
  background: #f9fafb;
}

/* 인용문 */
.simple-markdown :deep(blockquote) {
  border-left: 4px solid #e5e7eb;
  padding-left: 1rem;
  margin: 0.5rem 0;
  color: #6b7280;
  font-style: italic;
}

/* 링크 */
.simple-markdown :deep(a) {
  color: #3b82f6;
  text-decoration: underline;
}
</style>