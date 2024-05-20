# APP : hash algorithm implementation

This is the demonstration web application for custom implementation of the hash algorithms.

## Setup Locally
In terminal initialize the virtual environment
```bash
# Create
python3 -m venv /venv
# Activate
source venv/bin/activate
```

Now install dependencies:
```bash
pip install -r requirements.txt
```

## Run the application
```bash
uvicorn main:app --reload
```

## Running app in Docker
In the project root run the following command to build the docker image and then run the container with the application
```bash
docker build -t hash-app .
docker run -d -p 8000:8000 hash-app
```
