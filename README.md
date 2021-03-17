# ACME Workflow - Playvox

Framework: **FastApi** 

## How to run
1. Install the libraries using the command:
   
        pip install -Ur requirements.txt

2. Copy the default environment in the patch **local_env** to **.env**:
   
        cp /path_to_proyect/local_env.env /path_to_project.env

3. Start the server using the command:

        uvicorn main:app --reload

4. The server will start to listen in:

        http://localhost:8000/

## API Docs

1. Once the server is running, the complete docs in:

        http://localhost:8000/docs#/


## Unit Tests
1 To execute the tests:

        python -m unittest discover -s .

