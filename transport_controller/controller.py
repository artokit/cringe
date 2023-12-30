from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from transport_controller.schemas import Transport, AddNewTransport, StatusOperationCar, UpdateTransportBody
from transport_controller import models
from users_auth.utils import check_auth

router = APIRouter()


@router.get('/{id}', response_model=Transport)
def get_transport(id: int):
    return models.get_car(id)


@router.post('/', response_model=StatusOperationCar)
def add_new_transport(transport: AddNewTransport, authorize: check_auth = Depends()):
    authorize: AuthJWT
    user_id = authorize.get_jwt_subject()
    return models.add_car(transport, user_id)


@router.put('/{id}', response_model=StatusOperationCar)
def update_transport(id: int, transport: UpdateTransportBody, authorize: check_auth = Depends()):
    authorize: AuthJWT
    user_id = authorize.get_jwt_subject()
    car = models.get_car(id)

    if car.owner_id != int(user_id):
        raise HTTPException(status_code=403, detail='Это не ваша машина :(')

    models.update_car(id, transport)

    return StatusOperationCar(status="success", id=id)


@router.delete('/{id}', response_model=StatusOperationCar)
def delete_transport(id: int, authorize: check_auth = Depends()):
    authorize: AuthJWT
    user_id = authorize.get_jwt_subject()
    car = models.get_car(id)

    if car.owner_id != int(user_id):
        raise HTTPException(status_code=403, detail='Это не ваша машина :(')

    models.delete_car(id)

    return StatusOperationCar(status='success', id=id)
