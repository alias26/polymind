# PostgreSQL 수동 설정 가이드

PostgreSQL 인증 문제로 인해 수동 설정이 필요합니다.

## 1단계: PostgreSQL 접속 (관리자 권한 필요)

터미널에서 다음 명령어를 실행하세요:

```bash
# 방법 1: postgres 사용자로 직접 접속
sudo -u postgres psql

# 방법 2: 설정 파일 사용
sudo -u postgres psql -f setup_postgresql.sql
```

## 2단계: 수동으로 SQL 실행

psql에 접속되면 다음 SQL을 실행하세요:

```sql
-- 사용자 생성
CREATE USER polyai_user WITH PASSWORD 'polyai_password';

-- 데이터베이스 생성
CREATE DATABASE polyai_db OWNER polyai_user;

-- 권한 부여
GRANT ALL PRIVILEGES ON DATABASE polyai_db TO polyai_user;

-- 데이터베이스 연결 후 스키마 권한 부여
\c polyai_db
GRANT ALL ON SCHEMA public TO polyai_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO polyai_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO polyai_user;

-- 기본 권한 설정
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO polyai_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO polyai_user;

-- 종료
\q
```

## 3단계: 연결 테스트

설정 완료 후 다음 명령어로 테스트:

```bash
source venv/bin/activate
python migrate_to_postgresql.py
```

## 대안: 임시로 SQLite 계속 사용

PostgreSQL 설정이 어려운 경우, 일단 SQLite를 계속 사용하고 나중에 마이그레이션할 수 있습니다:

```bash
# .env 파일을 다시 SQLite로 변경
echo "DATABASE_URL=sqlite:///./polyai.db" > .env.temp
echo "DEBUG=True" >> .env.temp
echo "" >> .env.temp
echo "# Encryption Key for API keys (base64 encoded Fernet key)" >> .env.temp
echo "ENCRYPTION_KEY=ykXpWM640qSkoKGgGu7aVhoR0EyHyN8jKxyL4kSs1ss=" >> .env.temp
mv .env.temp .env
```