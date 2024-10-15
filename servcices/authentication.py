from fastapi import Depends, HTTPException
from models import User

def get_current_user(token: str) -> User:
    if token == "valid_token":
        return User(username="test_user", token=token)
    else:
        raise HTTPException(status_code=401, detail="Token inválido")
