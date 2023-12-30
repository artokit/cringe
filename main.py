from fastapi import FastAPI
from account_controller import controller as acc_controller
from transport_controller import controller as auto_controller
from rent_controller import controller as rent_controller
import logger

logger.load_config()

app = FastAPI()
app.include_router(acc_controller.router, prefix='/api/Account', tags=['Account Endpoints'])
app.include_router(auto_controller.router, prefix='/api/Transport', tags=['Transport Endpoints'])
app.include_router(rent_controller.router, prefix='/api/Rent', tags=['Transport Endpoints'])
