import os
import sys
sys.path.append(os.pardir)
from fastapi import FastAPI

from routers import admin


app = FastAPI()

app.include_router(admin.router)
