from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError


def check_auth(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        return authorize
    except MissingTokenError:
        raise HTTPException(status_code=403, detail='Вы не авторизованы')
