from fastapi import HTTPException
from database.db import cursor, connect
from transport_controller.schemas import Transport, AddNewTransport, StatusOperationCar, UpdateTransportBody
import logging


def get_car(id: int):
    try:
        cursor.execute('SELECT * FROM transports where id = %s', (id, ))
        res = cursor.fetchone()
        return Transport(**dict(zip(Transport.__match_args__, res)))
    except TypeError:
        raise HTTPException(status_code=404, detail='Машина не существует')


def add_car(transport: AddNewTransport, user_id: int) -> StatusOperationCar:
    try:
        cursor.execute(
            'INSERT INTO transports("canBeRented", "transportType", '
            'model, color, identifier, description, latitude, longitude, "minutePrice", "dayPrice", owner_id) '
            'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (transport.canBeRented, transport.transportType.value, transport.model, transport.color,
             transport.identifier, transport.description, transport.latitude, transport.longitude,
             transport.minutePrice, transport.dayPrice, user_id)
        )
        connect.commit()
        return StatusOperationCar(id=cursor.lastrowid, status='success')
    except Exception as e:
        logging.getLogger().exception(e)
        connect.rollback()
        return StatusOperationCar(status='error')


def delete_car(id: int):
    cursor.execute('DELETE FROM TRANSPORTS where id = %s', (id, ))
    connect.commit()


def update_car(id: int, transport: UpdateTransportBody):
    try:
        cursor.execute(
            'UPDATE TRANSPORTS SET "canBeRented" = %s, "transportType" = %s, model = %s, color = %s, '
            'identifier = %s, description = %s, latitude = %s, longitude = %s, "minutePrice" = %s, "dayPrice" = %s '
            'where id = %s',
            (transport.canBeRented, transport.transportType.value, transport.model, transport.color,
             transport.identifier, transport.description, transport.latitude, transport.longitude,
             transport.minutePrice, transport.dayPrice, id)
        )
        connect.commit()
    except Exception as e:
        logging.getLogger().exception(e)
        connect.rollback()
