#####
# Collect routes and run the FastAPI server
#####

from fastapi import FastAPI
from routers import classify, search

app = FastAPI()

app.include_router(search.router)
