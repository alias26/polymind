# Node.js 18 기반 이미지 사용 (빌드 단계)
FROM node:18-alpine as build-stage

# 작업 디렉터리 설정
WORKDIR /app

# 패키지 파일들 복사
COPY package*.json ./

# 의존성 설치
RUN npm ci --only=production

# 소스 코드 복사
COPY . .

# 프로덕션 빌드
RUN npm run build

# Nginx 기반 이미지 사용 (서빙 단계)
FROM nginx:alpine as production-stage

# 빌드된 파일을 Nginx로 복사
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Nginx 설정 파일 복사 (SPA 라우팅 지원)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 포트 노출
EXPOSE 80

# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]