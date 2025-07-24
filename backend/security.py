from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import models, schemas, database
# --- KONFIGURASI KEAMANAN ---
# Di aplikasi nyata, KUNCI RAHASIA ini HARUS diganti dan disimpan dengan aman
# Anda bisa generate kunci baru dengan perintah: openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Konteks untuk hashing password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Skema ini memberitahu FastAPI cara menemukan token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_user(db: Session, username: str):
    """Fungsi helper untuk mencari user di DB."""
    return db.query(models.User).filter(models.User.username == username).first()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Dependensi untuk mendapatkan user yang sedang login dari token.
    Ini akan menjadi "satpam" untuk endpoint terproteksi kita.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # Ambil data user dari database
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# --- FUNGSI-FUNGSI KEAMANAN ---

def verify_password(plain_password, hashed_password):
    """Memverifikasi password asli dengan hash di database."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Membuat hash dari password asli."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Membuat JSON Web Token (JWT)."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt