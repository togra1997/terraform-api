import logging
import os
import sys

import dotenv
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from src.api.endpoint.endpoint import router

dotenv.load_dotenv()
allow_origins = os.getenv("ALLOW_ORIGINS")

logger.remove()  # デフォルトハンドラを削除
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)
logger.add(
    "logs/uvicorn_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # 毎日ローテーション
    retention="30 days",  # 30日間保持
    compression="zip",  # 古いログを圧縮
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # loguruのloggerに標準のloggingレコードを渡す
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

app = FastAPI()
app.include_router(router)
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
    # logsディレクトリを作成
    os.makedirs("logs", exist_ok=True)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,  # loguruで一元管理
        log_level="info",
    )


if __name__ == "__main__":
    main()
