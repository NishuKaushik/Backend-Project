# Ensure the following modules are installed:
# pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
import os
import shutil
import mimetypes

# Database (in-memory simulation)
USERS_DB = {}
FILES_DB = {}
VERIFICATION_TOKENS = {}

# Settings
SECRET_KEY = "secret_key_example"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Temporary hardcoded Ops user (for testing purpose)
from collections import namedtuple
UserModel = namedtuple("UserModel", ["email", "name", "password", "role", "verified"])
USERS_DB["ops@example.com"] = UserModel(
    email="ops@example.com",
    name="Ops User",
    password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash("ops123"),
    role="ops",
    verified=True
)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth & Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Pydantic Models
class User(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str  # ops or client
    verified: bool = False

class FileMeta(BaseModel):
    id: str
    filename: str
    uploader: str
    timestamp: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class SignupRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

# Utility Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return USERS_DB[email]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# API Routes
@app.post("/sign-up")
def sign_up(user: SignupRequest):
    if user.email in USERS_DB:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(user.password)
    USERS_DB[user.email] = User(email=user.email, name=user.name, password=hashed, role="client")
    token = create_access_token({"sub": user.email, "role": "client"}, timedelta(hours=1))
    VERIFICATION_TOKENS[token] = user.email
    return {"encrypted-verification-url": f"/verify-email/{token}"}

@app.get("/verify-email/{token}")
def verify_email(token: str):
    email = VERIFICATION_TOKENS.get(token)
    if not email or email not in USERS_DB:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    USERS_DB[email].verified = True
    return {"message": "Email verified successfully"}

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload-file")
def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if current_user.role != "ops":
        raise HTTPException(status_code=403, detail="Not allowed")
    ext = os.path.splitext(file.filename)[1]
    if ext not in [".docx", ".pptx", ".xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    fid = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, fid + ext)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    FILES_DB[fid] = FileMeta(id=fid, filename=file.filename, uploader=current_user.email, timestamp=datetime.utcnow())
    return {"message": "File uploaded successfully", "file_id": fid}

@app.get("/files")
def list_files(current_user: User = Depends(get_current_user)):
    if current_user.role != "client" or not current_user.verified:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return [f.dict() for f in FILES_DB.values()]

@app.get("/download-file/{file_id}")
def generate_download_link(file_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != "client" or not current_user.verified:
        raise HTTPException(status_code=403, detail="Unauthorized")
    token = create_access_token({"sub": current_user.email, "file_id": file_id, "role": "client"}, timedelta(minutes=5))
    return {"download-link": f"/download-file-secure/{token}", "message": "success"}

@app.get("/download-file-secure/{token}")
def download_file_secure(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        file_id = payload.get("file_id")
        role = payload.get("role")
        if role != "client" or email not in USERS_DB:
            raise HTTPException(status_code=403, detail="Invalid access")
        meta = FILES_DB.get(file_id)
        if not meta:
            raise HTTPException(status_code=404, detail="File not found")
        ext = os.path.splitext(meta.filename)[1]
        path = os.path.join(UPLOAD_DIR, file_id + ext)
        return FileResponse(path, media_type=mimetypes.guess_type(meta.filename)[0], filename=meta.filename)
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

@app.get("/")
def root():
    return {"message": "✅ Secure File Sharing API is live!"}
