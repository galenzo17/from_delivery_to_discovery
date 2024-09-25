from fastapi import Depends, HTTPException
from models import User

def get_current_user(token: str = "dummy_token") -> User:
    # Aquí implementarías la lógica real de autenticación
    if token == "dummy_token":
        return User(username="test_user", token=token)
    else:
        raise HTTPException(status_code=401, detail="Token inválido")
