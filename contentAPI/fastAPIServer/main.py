import os
import sys
sys.path.append(os.pardir)
from fastapi import FastAPI

from routers import admin


app_admin = FastAPI()

app_admin.include_router(admin.router)
