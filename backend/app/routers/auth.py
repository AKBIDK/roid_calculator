from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.security import create_access_token, verify_password, hash_password

router = APIRouter(prefix="/api/auth", tags=["Autenticação & RBAC"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

# Usuários padrão do sistema para inicialização rápida
DEMO_USERS = {
    "admin": {"password_hash": hash_password("admin123"), "role": "ADMIN"},
    "editor": {"password_hash": hash_password("editor123"), "role": "EDITOR"},
    "viewer": {"password_hash": hash_password("viewer123"), "role": "VIEWER"}
}

@router.post("/login", response_model=TokenResponse)
def login(creds: LoginRequest):
    user = DEMO_USERS.get(creds.username)
    if not user or not verify_password(creds.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos"
        )
    token = create_access_token(data={"sub": creds.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}
