from fastapi import FastAPI
import account_controller

app = FastAPI()
app.include_router(account_controller.controller.router, prefix='/api/Account')
