from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException
from .database import get_db
from sqlalchemy.orm import Session
from .models import APIKeyModel, VoltagesModel
from .dtos.voltages import VoltagesDTO, VoltagesCreateDTO
from .dtos.generic import SuccessResponse
from .pagination import Page, PageParams, paginate_sqlalchemy
from .config import settings
from .logging import load_config, server_access_middleware
from .exception_handlers import (
    handle_unhandled_exceptions,
    http_exception_handler,
    request_validation_exception_handler,
)

load_config(settings.logging_config)

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=server_access_middleware)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)
app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler,
)
app.add_exception_handler(
    Exception,
    handle_unhandled_exceptions,
)

def create_voltage(db: Session, voltage: VoltagesCreateDTO) -> VoltagesModel:
    db_voltages = VoltagesModel(**voltage.dict())
    db.add(db_voltages)
    db.commit()
    db.refresh(db_voltages)
    return db_voltages

def check_api_key(db, api_key):
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Please verify your API key is valid"
            ),
        )

    api_key_query = db.query(APIKeyModel).filter(APIKeyModel.api_key==api_key).filter(APIKeyModel.status==1).first()
    if not api_key_query:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Please verify your API key is valid"
            ),
        )
    return api_key_query

@app.get("/voltage")
async def get_voltage(request: Request, db: Session = Depends(get_db), page_params: PageParams = Depends()):
    api_key = request.headers.get('api-key')
    api_key_query = check_api_key(db, api_key)

    voltage_query = db.query(VoltagesModel).filter(VoltagesModel.api_key==api_key_query.id).order_by(VoltagesModel.id.desc())
    page = paginate_sqlalchemy(voltage_query, page_params)

    data = []
    for voltage in page.data:
        voltage = VoltagesDTO.from_orm(voltage)
        data.append(voltage)

    return Page[VoltagesDTO](meta=page.meta, data=data)

@app.post("/voltage")
async def post_voltage(request: Request, json: VoltagesCreateDTO, db: Session = Depends(get_db)):
    api_key = request.headers.get('api-key')
    api_key_query = check_api_key(db, api_key)

    voltage = create_voltage(db, VoltagesCreateDTO(
        voltage=json.voltage,
        api_key=api_key_query.id,
    ))

    return SuccessResponse(data=VoltagesDTO.from_orm(voltage))
