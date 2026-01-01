from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import SQLModel, Session, select, create_engine, Field
from sqlalchemy.exc import IntegrityError
import logging
import time

logger = logging.getLogger("MyAPI")
logger.setLevel(logging.INFO)

# Handler 1: Menulis ke File
file_handler = logging.FileHandler("system_monitor.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Handler 2: Menulis ke Terminal (Console)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Gabungkan keduanya
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class Data(SQLModel, table=True):
    __table__name = "data"

    id_data: str = Field(primary_key=True)
    service_name: str
    cpu_usage: float
    memory_usage: float
    latency: int
    error_count: int

class SendData(SQLModel):
    id_data: str
    service_name: str
    cpu_usage: float
    memory_usage: float
    latency: int
    error_count: int

sqlite_file_name = "./data_monitor.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    connect_args= {
        "check_same_thread": False
    }
)

def get_session():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(
    title="Monitoring Data API",
    description="API untuk memonitoring proses API Microservice"
)

@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        # Ganti logging.info jadi logger.info
        logger.info(f"REQUEST: {request.method} {request.url.path} - STATUS: {response.status_code} - DURATION: {process_time:.2f}ms")
        return response
    except Exception as e:
        # Ganti logging.error jadi logger.error
        logger.error(f"ERROR SYSTEM: {request.method} {request.url.path} - PESAN: {str(e)}")
        raise e

@app.get("/", include_in_schema=False)
async def root(): 
    return RedirectResponse(url="/docs")

@app.get("/health")
async def CekHidup():
    return {"message": "Sistem HIDUP ONLINE!"}

@app.get("/metrics/", response_model=list[Data], status_code=200)
def getAllData(session:sessionDep):
    statement = select(Data)
    results = session.exec(statement).all()
    return results

@app.post("/metrics/", response_model=Data, status_code=201)
def addNewData(
    data: SendData,
    session: sessionDep
):
    data_db = Data.model_validate(data)

    try:
        session.add(data_db)
        session.commit()
        session.refresh(data_db)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code = 409,
            detail="ID Error sudah ada"
        )
    return data_db




