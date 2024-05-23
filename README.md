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
pip3 install -r requirements.txt
```

## Run the application
```bash
uvicorn main:app --reload
# alternatively use the following command if the uvicorn is not in you path
python3 -m uvicorn main:app --reload
```

## Test the hash algorithms
There are several unit tests for each hash algorithm, to run them use the following command:
```bash
python3 static/unittests.py
```

## Running app in Docker
In the project root run the following command to build the docker image and then run the container with the application
```bash
docker build -t hash-app .
docker run -d -p 8000:8000 hash-app
```

## Documentation of the API
To see and try the API see the documentation on the application url + `/docs`
If you ran the application locally, then it is `http://127.0.0.1:8000/docs`
This documentation cosists of the individual endpoints which are available for try. Also, there is a list of schemas available which represent the data structures used by the application.

## User documentation
For extensive user documentation see the document `User_doc.pdf`.
