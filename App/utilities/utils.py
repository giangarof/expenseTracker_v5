from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from App.exports import SECRET_KEY, algorithm, oauth2_bearer

from App.schema.User import bcrypt_context
from jose import JWTError, jwt


# Description: Generate a new ID
# Explanation: Get the last row id to calculate the new id: (Last row id + 1)
async def incrementId(model, db):
    data = db.query(model).all()

    if len(data) == 0:
        return 1
    return data[-1].id + 1


# Description: Check for existense in the database
# Explanation: Gets the model and check if something exist in the database
def checkIfExist(data):
    pass


# Description: Hash password
# Explanation: Takes the plain password text as parameter and return the password hashed
async def hashPassword(data):
    return bcrypt_context.hash(data)


# Description: Verify stored password
# Explanation: verify the hashed password with the password form submission
def verify_password(password, hash_password):
    verify = bcrypt_context.verify(password, hash_password)

    if verify is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return verify


# Description: Check user role
# Explanation: Check if user has admin role
def ifAdmin(user):
    if user is None or user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="401 error"
        )
