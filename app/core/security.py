from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from app.models import User
from app.core import settings
from jose import jwt

class PasswordManager:
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.bcrypt_context.hash(password)
    @classmethod
    def verified_password(cls, password: str, hashedpassword: str) -> bool:
        return cls.bcrypt_context.verify(password, hashedpassword)

    @classmethod
    def authenticate_user(cls, email: str, password: str, db):
        user = db.query(User).filter(email == User.email).first()
        if not user:
            return None
        if not cls.verified_password(password, user.hashed_password):
            return None
        return user

class TokenManager:

    @staticmethod
    def create_access_token(username: str, user_id: str, expires_delta: timedelta) -> str:
        expire_time = datetime.now(timezone.utc) + expires_delta

        payload = {
            "sub": username,
            "id": user_id,  
            "exp": int(expire_time.timestamp())
        }

        try:
            # 3. Sign and return the token
            return jwt.encode(
                payload, 
                settings.SECRET_KEY, 
                algorithm=settings.ALGORITHM
            )
        except Exception as e:
            # Senior Tip: Log the exact error to your terminal for debugging
            print(f"CRITICAL: JWT Encoding failed: {e}")
            raise e
