#####
# Collect routes and run the FastAPI server
#####

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from routers import classify, search

app = FastAPI()

# CORS middleware to allow local traffic
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# middleware to log requests with latency
# (would be put with other metrics code if there was any)
LATENT_REQUEST_THRESHOLD_SECONDS = 0.1
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


@app.middleware("http")
async def log_slow_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    if process_time > LATENT_REQUEST_THRESHOLD_SECONDS:
        logging.warning(f"Slow request '{request.url.path}' took {process_time:.2f}s")
    else:
        logging.debug(f"Request '{request.url.path}' took {process_time:.2f}s")
    return response


app.include_router(search.router)
app.include_router(classify.router)
