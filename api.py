import os

import dotenv
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.endpoint.proxmox import router as proxmox_router
from src.api.endpoint.terraform import router

dotenv.load_dotenv()
allow_origins = os.getenv("ALLOW_ORIGINS")


app = FastAPI()
app.include_router(router)
app.include_router(proxmox_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[allow_origins],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
