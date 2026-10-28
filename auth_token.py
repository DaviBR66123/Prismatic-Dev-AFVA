
import os
import datetime
import jwt

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "troque-esta-chave-no-env")

ALGORITHM = "HS256"

security = HTTPBearer()

def criar_token(usuario_id: int, nome: str, papel: str) -> str:
    payload = {
        "sub": str(usuario_id),
        "nome": nome,
        "papel": papel,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            credenciais.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado."
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido."
        )
