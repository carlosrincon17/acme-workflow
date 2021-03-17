import pathlib

import i18n
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_restful import Api

from resources.account import AccountApi
from resources.workflow import WorkFlowApi
from settings import APISettings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = pathlib.Path(__file__).parent
i18n.load_path.append("{}/translations/".format(current_dir))
i18n.set('locale', 'es')


@app.get("/")
async def root():
    return {"message": "Playvox workflow API v1.0"}

api = Api(app)
api.add_resource(AccountApi(), "/v1/account")
api.add_resource(WorkFlowApi(), "/v1/workflow")


if __name__ == "__main__":
    uvicorn.run(app, host=APISettings().host, port=APISettings().port)
