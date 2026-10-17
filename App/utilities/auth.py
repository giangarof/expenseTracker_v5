from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from App.exports import SECRET_KEY, algorithm, oauth2_bearer

from jose import JWTError, jwt

from App.utilities.utils import verify_password


# Description: Authenticate user
# Explanation: Used to login the user
def authenticate_user(username: str, password: str, db, model):
    user = db.query(model).filter(model.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    verify_password(password, user.password)

    return user


# Description: Create token when login
# Explanation: Create a token for jwt with expiration
def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "role": role, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=algorithm)


# Description: Get the current user that is log in
# Explanation: get the current user by decoding the jwt
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        return {"username": username, "id": user_id, "role": role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
