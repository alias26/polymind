"""
이메일 서비스
개발 환경에서는 콘솔에 출력, 운영 환경에서는 실제 이메일 발송
"""
import os
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.models.email_verification import EmailVerification, PasswordResetToken
from app.models.user import User
import uuid

class EmailService:
    """이메일 관련 서비스"""
    
    def __init__(self):
        self.is_development = os.getenv("ENVIRONMENT", "development") == "development"
    
    def generate_verification_code(self) -> str:
        """6자리 인증 코드 생성"""
        return ''.join(random.choices(string.digits, k=6))
    
    def generate_reset_token(self) -> str:
        """비밀번호 재설정 토큰 생성"""
        return str(uuid.uuid4())
    
    def send_verification_email(self, db: Session, user: User, verification_type: str = "register") -> str:
        """이메일 인증 코드 발송"""
        # 기존 미사용 인증 코드 삭제
        db.query(EmailVerification).filter(
            EmailVerification.user_id == user.id,
            EmailVerification.verification_type == verification_type,
            EmailVerification.is_used == False
        ).delete()
        db.commit()
        
        # 새 인증 코드 생성
        verification_code = self.generate_verification_code()
        expires_at = datetime.utcnow() + timedelta(minutes=5)  # 5분 후 만료
        
        # DB에 저장
        verification = EmailVerification(
            id=str(uuid.uuid4()),
            user_id=user.id,
            email=user.email,
            verification_code=verification_code,
            verification_type=verification_type,
            expires_at=expires_at
        )
        db.add(verification)
        db.commit()
        
        # 이메일 발송 (개발 환경에서는 콘솔 출력)
        if self.is_development:
            self._print_verification_email(user.email, verification_code, verification_type)
        else:
            # TODO: 실제 이메일 발송 구현
            pass
        
        return verification_code
    
    def send_password_reset_email(self, db: Session, user: User) -> str:
        """비밀번호 재설정 이메일 발송"""
        # 기존 미사용 토큰 삭제
        db.query(PasswordResetToken).filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.is_used == False
        ).delete()
        db.commit()
        
        # 새 재설정 토큰 생성
        reset_token = self.generate_reset_token()
        expires_at = datetime.utcnow() + timedelta(minutes=30)  # 30분 후 만료
        
        # DB에 저장
        token_record = PasswordResetToken(
            id=str(uuid.uuid4()),
            user_id=user.id,
            token=reset_token,
            expires_at=expires_at
        )
        db.add(token_record)
        db.commit()
        
        # 이메일 발송 (개발 환경에서는 콘솔 출력)
        if self.is_development:
            self._print_password_reset_email(user.email, reset_token)
        else:
            # TODO: 실제 이메일 발송 구현
            pass
        
        return reset_token
    
    def verify_code(self, db: Session, email: str, code: str, verification_type: str = "register") -> Optional[User]:
        """인증 코드 검증"""
        verification = db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.verification_code == code,
            EmailVerification.verification_type == verification_type,
            EmailVerification.is_used == False,
            EmailVerification.expires_at > datetime.utcnow()
        ).first()
        
        if not verification:
            return None
        
        # 인증 코드 사용 처리
        verification.is_used = True
        
        # 사용자 이메일 인증 상태 업데이트 (회원가입 인증인 경우)
        if verification_type == "register":
            user = db.query(User).filter(User.id == verification.user_id).first()
            if user:
                user.is_email_verified = True
        
        db.commit()
        return db.query(User).filter(User.id == verification.user_id).first()
    
    def verify_reset_token(self, db: Session, token: str) -> Optional[User]:
        """비밀번호 재설정 토큰 검증"""
        token_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        ).first()
        
        if not token_record:
            return None
        
        return db.query(User).filter(User.id == token_record.user_id).first()
    
    def use_reset_token(self, db: Session, token: str) -> bool:
        """비밀번호 재설정 토큰 사용 처리"""
        token_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.utcnow()
        ).first()
        
        if not token_record:
            return False
        
        token_record.is_used = True
        db.commit()
        return True
    
    def _print_verification_email(self, email: str, code: str, verification_type: str):
        """콘솔에 인증 이메일 내용 출력"""
        print("\n" + "="*50)
        print("📧 EMAIL VERIFICATION (개발 환경)")
        print("="*50)
        print(f"받는 사람: {email}")
        
        if verification_type == "register":
            print("제목: [PolyMind] 회원가입 이메일 인증")
            print("\n안녕하세요! PolyMind에 가입해주셔서 감사합니다.")
            print("아래 인증 코드를 입력하여 이메일 인증을 완료해주세요.")
        elif verification_type == "password_reset":
            print("제목: [PolyMind] 비밀번호 재설정 인증")
            print("\n비밀번호 재설정을 위한 인증 코드입니다.")
            print("아래 인증 코드를 입력해주세요.")
        
        print(f"\n🔑 인증 코드: {code}")
        print("\n※ 이 코드는 5분 후에 만료됩니다.")
        print("※ 본인이 요청하지 않았다면 이 이메일을 무시하세요.")
        print("="*50 + "\n")
    
    def _print_password_reset_email(self, email: str, token: str):
        """콘솔에 비밀번호 재설정 이메일 내용 출력"""
        # 환경변수에서 프론트엔드 URL 가져오기 (Vue.js 개발서버 기본 포트: 8080)
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8080")
        reset_url = f"{frontend_url}/reset-password?token={token}"
        
        print("\n" + "="*50)
        print("📧 PASSWORD RESET EMAIL (개발 환경)")
        print("="*50)
        print(f"받는 사람: {email}")
        print("제목: [PolyMind] 비밀번호 재설정")
        print("\n비밀번호 재설정을 요청하셨습니다.")
        print("아래 링크를 클릭하여 새 비밀번호를 설정해주세요.")
        print(f"\n🔗 재설정 링크: {reset_url}")
        print(f"\n🔑 토큰: {token}")
        print("\n※ 이 링크는 30분 후에 만료됩니다.")
        print("※ 본인이 요청하지 않았다면 이 이메일을 무시하세요.")
        print("="*50 + "\n")

# 싱글톤 인스턴스
email_service = EmailService()