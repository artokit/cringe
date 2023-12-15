from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from starlette import status
from account_controller import models
from account_controller.models import SECRET_KEY, ALGORITHM

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/Account/SignIn")


def generate_access_token(username):
    access_token_expires = timedelta(minutes=models.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = models.create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return access_token


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = models.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = models.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return token_data


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    return current_user


@router.get("/Me", response_model=models.TokenData)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user


@router.post('/SignUp', response_model=models.Token)
async def sign_up(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    h = models.get_password_hash(form_data.password)

    res = models.add_user(form_data.username, h)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Данный логин уже занят",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = generate_access_token(form_data.username)
    models.update_access_token(form_data.username, token)

    return {"access_token": token, "token_type": "bearer"}


@router.post('/SignIn', response_model=models.Token)
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = models.get_user_by_username(form_data.username)

    if user:
        if models.verify_password(form_data.password, user.hashed_password):
            access_token = generate_access_token(form_data.username)
            models.update_access_token(form_data.username, access_token)
            return models.Token(access_token=access_token, token_type='bearer')

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный логин/пароль",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post('/Update')
async def update(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    models.update_user(current_user.username, form_data.username, form_data.password)
    access_token = generate_access_token(form_data.username)
    models.update_access_token(form_data.username, access_token)
    return {'access': True}
