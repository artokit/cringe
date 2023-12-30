from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TransportType(Enum):
    CAR = 'Car'
    BIKE = 'Bike'
    SCOOTER = 'Scooter'


@dataclass
class Transport:
    id: Optional[int]
    canBeRented: bool
    transportType: TransportType
    model: str
    color: str
    identifier: str
    description: Optional[str]
    latitude: float
    longitude: float
    minutePrice: Optional[float]
    dayPrice: Optional[float]
    owner_id: int


@dataclass
class AddNewTransport:
    canBeRented: bool
    transportType: TransportType
    model: str
    color: str
    identifier: str
    description: Optional[str]
    latitude: float
    longitude: float
    minutePrice: Optional[float]
    dayPrice: Optional[float]


@dataclass
class UpdateTransportBody:
    canBeRented: bool
    transportType: TransportType
    model: str
    color: str
    identifier: str
    description: Optional[str]
    latitude: float
    longitude: float
    minutePrice: Optional[float]
    dayPrice: Optional[float]


@dataclass
class StatusOperationCar:
    status: str
    id: Optional[int] = None
