import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from static.algorithms import Algorithm

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/hash')
async def calculate_hash(data: dict):
    algorithm = data.get('algorithm')
    message = data.get('message')

    logger = logging.getLogger(__name__)
    logger.debug(f'Calculating hash({algorithm}) from "{message}"')

    algorithm = Algorithm(message, algorithm)

    # Return the hash result as a JSON response
    return {'algorithm': algorithm.type, 'message': message, 'hash': algorithm.hash()}
