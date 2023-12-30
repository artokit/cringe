import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from starlette.responses import Response
from users_auth.oauth import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN
from account_controller.schemas import LoginSuccessSchema
from account_controller import password
from account_controller import schemas, models
from users_auth.utils import check_auth

router = APIRouter()


@router.post('/SignUp', status_code=201, response_model=schemas.UserRegisterResponseSuccess)
async def create_user(payload: schemas.UserRegisterSchema):
    payload.password = password.get_password_hash(payload.password)
    r = models.add_user(payload.username, payload.password)
    if r:
        return schemas.UserRegisterResponseSuccess(time_register_user=datetime.datetime.now())
    raise HTTPException(status_code=401, detail='Данный логин уже занят')


@router.post('/SignIn')
def login(payload: schemas.LoginUserSchema, response: Response, Authorize: AuthJWT = Depends()):
    user = models.get_user_by_username(payload.username)
    if not user:
        raise HTTPException(status_code=400,
                            detail='Неверный логин или пароль')

    if not password.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400,
                            detail='Неверный логин или пароль')

    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    models.update_tokens(payload.username, access_token, refresh_token)

    return LoginSuccessSchema(status=200, access_token=access_token)


@router.post('/SignOut', status_code=200)
def logout(response: Response, authorize: check_auth = Depends()):
    authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)

    return {'status': 'success'}


@router.get('/Me', response_model=schemas.UserMeInfo)
def get_me(authorize: check_auth = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user = models.get_user_info(user_id)
    return user
