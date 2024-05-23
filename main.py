import logging
from fastapi import FastAPI, Request, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from static.algorithms import Algorithm
from static.models import HashRequest, HashResponse, post_hash_openapi, hash_request_openapi

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/hash', response_model=HashResponse, response_model_exclude_none=True, **post_hash_openapi)
async def calculate_hash(data: HashRequest = Body(..., **hash_request_openapi)):
    """Endpoint which takes the data and calculates the hash of the given message within the data."""

    logger = logging.getLogger(__name__)
    logger.debug(f'Calculating hash({data.algorithm}) from "{data.message}"')

    algorithm = Algorithm(data.message, data.algorithm)

    # Return the hash result as a JSON response
    return HashResponse(
        algorithm=algorithm.type,
        message=data.message,
        hash=algorithm.hash()
    )