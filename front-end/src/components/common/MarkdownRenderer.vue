<template>
  <div class="markdown-renderer" v-html="renderedContent"></div>
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps({
  content: {
    type: String,
    required: true
  }
})

// marked 옵션 설정
marked.setOptions({
  breaks: true, // 줄바꿈을 <br>로 변환
  gfm: true, // GitHub Flavored Markdown 지원
  tables: true, // 테이블 지원
  sanitize: false, // HTML 허용 (안전한 환경에서만)
  smartLists: true, // 스마트 리스트
  smartypants: true // 스마트 따옴표
})

// 커스텀 렌더러 설정
const renderer = new marked.Renderer()

// 코드 블록 커스터마이징
renderer.code = function(code, language) {
  const validLanguage = language && language.match(/^[a-zA-Z0-9-]+$/)
  const lang = validLanguage ? ` class="language-${language}"` : ''
  return `<pre><code${lang}>${escapeHtml(code)}</code></pre>`
}

// 인라인 코드 커스터마이징
renderer.codespan = function(code) {
  return `<code class="inline-code">${escapeHtml(code)}</code>`
}

// 링크 커스터마이징 (새 탭에서 열기)
renderer.link = function(href, title, text) {
  const titleAttr = title ? ` title="${title}"` : ''
  return `<a href="${href}"${titleAttr} target="_blank" rel="noopener noreferrer">${text}</a>`
}

// 테이블 커스터마이징
renderer.table = function(header, body) {
  return `<table class="markdown-table">
    <thead>${header}</thead>
    <tbody>${body}</tbody>
  </table>`
}

marked.setOptions({ renderer })

// HTML 이스케이프
const escapeHtml = (text) => {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

// ASCII 표를 마크다운 표로 변환하는 함수
const convertAsciiTableToMarkdown = (text) => {
  
  // 코드 블록 내의 ASCII 표를 처리하기 위해 코드 블록을 먼저 추출
  // 언어 지정자를 제외하고 코드 내용만 추출
  const codeBlockRegex = /```(?:\w+\s*)?([\s\S]*?)```/g
  const processedText = text.replace(codeBlockRegex, (match, codeContent) => {
    // 언어 지정자 제거 후 코드 내용만 처리
    const cleanContent = codeContent.trim()
    // 코드 블록 내의 ASCII 표 변환
    const convertedCodeContent = processAsciiTableInText(cleanContent)
    return convertedCodeContent // 코드 블록 마커 제거하고 변환된 내용만 반환
  })
  
  
  // 나머지 일반 텍스트에서도 ASCII 표 변환
  const finalResult = processAsciiTableInText(processedText)
  
  // 반드시 문자열 반환 보장
  if (typeof finalResult !== 'string') {
    console.warn('convertAsciiTableToMarkdown: 비문자열 결과, 원본 반환:', typeof finalResult, finalResult)
    return text
  }
  
  return finalResult
}

// 텍스트 내의 ASCII 표를 실제로 변환하는 함수 (안전장치 추가)
const processAsciiTableInText = (text) => {
  try {
    // 입력 값 검증
    if (typeof text !== 'string') {
      console.warn('processAsciiTableInText: 비문자열 입력:', typeof text, text)
      return String(text || '')
    }
    
    
    // 이미 HTML 테이블이 들어온 경우 그대로 반환 (마크다운에서 처리하도록)
    if (text.includes('<table>') || text.includes('<tr>') || text.includes('<th>') || text.includes('<td>')) {
      return text
    }
    
    const lines = text.split('\n')
    let inTable = false
    let tableLines = []
    let result = []
    
    for (let i = 0; i < lines.length; i++) {
    const line = lines[i]
    
    // ASCII 표 시작 감지 (+- 문자로 시작하는 라인)
    if (line.match(/^\+[-+]+\+$/)) {
      if (!inTable) {
        inTable = true
        tableLines = []
      }
      continue
    }
    
    // 표 내용 라인 (| 문자로 시작)
    if (inTable && line.match(/^\|.*\|$/)) {
      // | 문자로 분리하고 트림
      const cells = line.split('|').slice(1, -1).map(cell => cell.trim())
      tableLines.push(cells)
      continue
    }
    
    // 표 끝 감지
    if (inTable && !line.match(/^[+|]/)) {
      // ASCII 표를 마크다운 표로 변홨
      if (tableLines.length > 0) {
        // 헤더 추가
        result.push('| ' + tableLines[0].join(' | ') + ' |')
        // 구분자 추가
        result.push('|' + tableLines[0].map(() => ' --- ').join('|') + '|')
        // 데이터 로우 추가
        for (let j = 1; j < tableLines.length; j++) {
          result.push('| ' + tableLines[j].join(' | ') + ' |')
        }
        result.push('')
      }
      inTable = false
      tableLines = []
    }
    
    if (!inTable) {
      result.push(line)
    }
  }
  
  // 마지막에 표가 끝나지 않은 경우 처리
  if (inTable && tableLines.length > 0) {
    result.push('| ' + tableLines[0].join(' | ') + ' |')
    result.push('|' + tableLines[0].map(() => ' --- ').join('|') + '|')
    for (let j = 1; j < tableLines.length; j++) {
      result.push('| ' + tableLines[j].join(' | ') + ' |')
    }
  }
  
    const finalResult = result.join('\n')
    
    // 반드시 문자열 반환 보장
    if (typeof finalResult !== 'string') {
      console.warn('processAsciiTableInText: 비문자열 결과, 원본 반환:', typeof finalResult, finalResult)
      return text
    }
    
    return finalResult
  } catch (error) {
    console.error('processAsciiTableInText: 처리 오류:', error)
    return text // 오류 시 원본 텍스트 반환
  }
}

const renderedContent = computed(() => {
  if (!props.content) return ''
  
  // 디버깅: content 타입과 내용 확인
  
  // content가 객체인 경운 처리
  let contentToRender = props.content
  if (typeof props.content === 'object' && props.content !== null) {
    contentToRender = JSON.stringify(props.content, null, 2)
  } else if (typeof props.content !== 'string') {
    contentToRender = String(props.content)
  }
  
  // ASCII 표 변환 비활성화 - 원본 그대로 유지
  // contentToRender = convertAsciiTableToMarkdown(contentToRender)
  
  try {
    const rawHtml = marked(contentToRender)
    
    // DOMPurify로 HTML 새니타이징 - XSS 공격 방지
    const sanitized = DOMPurify.sanitize(rawHtml, {
      ALLOWED_TAGS: [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'br', 'strong', 'em', 'u', 'del',
        'ul', 'ol', 'li',
        'blockquote',
        'code', 'pre',
        'a',
        'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'hr'
      ],
      ALLOWED_ATTR: ['href', 'title', 'target', 'rel', 'class'],
      ALLOW_DATA_ATTR: false
    })
    
    
    return sanitized
  } catch (error) {
    console.error('Markdown parsing error:', error)
    // 파싱 오류 시 원본 텍스트 반환 (새니타이징 포함)
    return DOMPurify.sanitize(escapeHtml(contentToRender).replace(/\n/g, '<br>'))
  }
})
</script>

<style scoped>
.markdown-renderer {
  line-height: 1.6;
  color: inherit;
}

/* 헤더 스타일 */
.markdown-renderer :deep(h1) {
  font-size: 1.5em;
  font-weight: 600;
  margin: 1em 0 0.5em 0;
  color: #1f2937;
}

.markdown-renderer :deep(h2) {
  font-size: 1.3em;
  font-weight: 600;
  margin: 1em 0 0.5em 0;
  color: #374151;
}

.markdown-renderer :deep(h3) {
  font-size: 1.1em;
  font-weight: 600;
  margin: 1em 0 0.5em 0;
  color: #4b5563;
}

/* 코드 스타일 */
.markdown-renderer :deep(pre) {
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 0.875rem;
}

.markdown-renderer :deep(code) {
  font-family: 'Monaco', 'Courier New', monospace;
  font-size: 0.875rem;
}

.markdown-renderer :deep(.inline-code) {
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 3px;
  padding: 0.2em 0.4em;
  font-size: 0.85em;
}

/* 테이블 스타일 */
.markdown-renderer :deep(table),
.markdown-renderer :deep(.markdown-table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}

.markdown-renderer :deep(th) {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
}

.markdown-renderer :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.75rem;
  color: #6b7280;
}

.markdown-renderer :deep(tr:nth-child(even)) {
  background: #f9fafb;
}

/* 리스트 스타일 */
.markdown-renderer :deep(ul) {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.markdown-renderer :deep(ol) {
  margin: 1rem 0;
  padding-left: 1.5rem;
}

.markdown-renderer :deep(li) {
  margin: 0.25rem 0;
  line-height: 1.5;
}

/* 링크 스타일 */
.markdown-renderer :deep(a) {
  color: #3b82f6;
  text-decoration: none;
}

.markdown-renderer :deep(a:hover) {
  text-decoration: underline;
}

/* 텍스트 스타일 */
.markdown-renderer :deep(strong) {
  font-weight: 600;
  color: #1f2937;
}

.markdown-renderer :deep(em) {
  font-style: italic;
  color: #4b5563;
}

.markdown-renderer :deep(p) {
  margin: 0.5rem 0;
}

.markdown-renderer :deep(p:first-child) {
  margin-top: 0;
}

.markdown-renderer :deep(p:last-child) {
  margin-bottom: 0;
}
</style>