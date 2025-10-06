import uvicorn
from fastapi import FastAPI, status

VERSION = 1.0
app = FastAPI(version=VERSION)


@app.get("/")
def return_model_version():
    """Simple route returning the model version

    Returns:
        JSON reponse:
            {
            'healtcheck': 'Everything OK!'
            }
    """
    return {"Model version": VERSION}


@app.get("/healthcheck", status_code=status.HTTP_200_OK)
def healthcheck():
    """Simple route for healthcheck

    Returns:
        JSON reponse:
            {
            'healtcheck': 'Everything OK!'
            }
    """
    return {"healthcheck": "Everything OK!"}


if __name__ == "__main__":
    # Start the sever, set reload=True for testing
    uvicorn.run("main:app", host="0.0.0.0", port=8002, log_level="info", reload=True)
