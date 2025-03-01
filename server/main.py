from io import BytesIO
from fastapi import FastAPI, File, UploadFile, Form, Depends,Request
from loguru import logger
import os
import sys
import json
import time
import uvicorn
from logging.handlers import RotatingFileHandler
from typing import List, Dict
import pandas as pd
from sqlmodel import select
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from methods import *
from typing import Annotated
from db import engine, Session, Learner,UserInDB, get_db
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY","default-fallback-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30
valid_validate_codes={
    "abcde",
    "12345",
    "00001"
}
used_validate_codes=set()

origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 根据实际情况调整允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
    
class Restriction(BaseModel):
    criterion: str
    importance: int
    group_type: str


class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    username:str | None = None

class User_to_create(BaseModel):
    username:str
    password:str
    invitation_code:str
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def setup_async_logging():
    os.makedirs("logs",exist_ok=True)
    logger.remove()

    def json_formatter(record):
    # 确保时间字段存在并正确处理时区
        log_time = record["time"].replace(tzinfo=None)
        log_entry = {
            "time": log_time.isoformat(),

            "level": record["level"].name,
            "message": record["message"],
            "module": record["module"]
        }
        print("xxxxxxxxx")
        
        # 合并extra字段
        if record["extra"]:
            log_entry.update({k: v for k, v in record["extra"].items() if k != "log_type"})
        print(log_entry["time"])
        return json.dumps(log_entry) + "\n"
    
    
    logger.add(
        "logs/app.log",
        rotation="10MB",
        retention="7 days",
        compression="zip",
        enqueue=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan> - <level>{message}</level>",#json_formatter,
        filter=lambda record:"log_type" not in record["extra"],
        level = os.getenv("LOG_LEVEL","INFO")
    )
    logger.add(
        "logs/access.log",
        rotation="10MB",
        retention="7 days",
        compression="zip",
        enqueue=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan> - <level>{message}</level>",#json_formatter,
        filter=lambda record:record["extra"].get("log_type") == "access",
        level = os.getenv("LOG_LEVEL","INFO")
    )
    logger.add(
        sys.stdout, 
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan> - <level>{message}</level>",
        enqueue=True,
        level="DEBUG"
    )
@app.middleware("http")
async def log_requests(request:Request,call_next):
    start_time = time.time()
    logger.bind(
        path = request.url.path,
        method = request.method,
        client = request.client.host if request.client else None,
        log_type = "access",
    ).info("Request received")
    response = None
    try:
        response = await call_next(request)
    except Exception as e:
        logger.opt(exception=e).error(
            "Unhandled exception",
            error_type=type(e).__name__,
            path = request.url.path,
            method = request.method,
            client = request.client.host if request.client else None,
            log_type = "access",
        )
        raise
    finally:
        duration = time.time()-start_time
        status_code = getattr(response,"status_code",500)
        response_size = response.headers.get("content-length", 0) if response else 0
       
        logger.bind(
            log_type="access",
            status_code=status_code,
            response_size=response_size,
            duration=round(duration, 4), 
            path=request.url.path,
            method=request.method,
            client=request.client.host if request.client else None
        ).info("Request completed")
    return response
    
def validate_invitation_code(code:str):
    if code in valid_validate_codes and code not in used_validate_codes:
        
        used_validate_codes.add(code)
        return True
    else:
        raise HTTPException(status_code=400,detail="Invalid invitation code")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username:str,db:Session=Depends(get_db)):
    user_dict = db.query(UserInDB).filter(UserInDB.username == username).first()
    return user_dict


def authenticate_user(username:str,password:str,db:Session=Depends(get_db)):
    user = get_user(username,db)
    if not user:
        logger.bind(username=username).error("User not found")
        return False
    if not verify_password(password,user.hashed_password):
        logger.bind(username=username).error("Invalid password")
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.bind(token=token).error("Invalid token")
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username,db=db)
    if user is None:
        logger.bind(username=username).error("User not found")
        raise credentials_exception
    return user

async def get_current_active_user(current_user:Annotated[UserInDB,Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user
def create_user(user:User_to_create,db:Session=Depends(get_db)):
    if db.query(UserInDB).filter(UserInDB.username == user.username).first() is not None:
        raise HTTPException(status_code=400,detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = UserInDB(username=user.username,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
@app.post("/register")
async def register(user:User_to_create,db:Session=Depends(get_db)):
    
    validate_invitation_code(user.invitation_code)
    create_user(user,db)
    logger.bind(log_type="business").info("New Registration")
    
    return {"message":"User created successfully"}
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db))->Token:
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate":"Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
@app.get("/users/me/", response_model=UserInDB)
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_active_user)]):
    return current_user

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith('.xlsx'):
        logger.bind(filename=file.filename).error("Only .xlsx files are allowed")
        return {"error": "Only .xlsx files are allowed"}

    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents), engine='openpyxl')
        df.to_sql('learner', con=engine, index=False, if_exists='append', method='multi')
        logger.bind(filename=file.filename).info("File uploaded successfully")
        return {"message": "File uploaded successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/grouping/")
async def grouping(restrictions: List[Restriction], db: Session = Depends(get_db)):
    query = select(Learner)
    learners = db.execute(query).scalars().all()

    # Convert learners to a list of dictionaries for easier manipulation
    learners_data = [{key: getattr(learner, key) for key in ['id', 'name', 'capability', 'gender', 'style']} for learner in learners]

    learners_map = {}
    for learner in learners_data:
        learners_map[learner["id"]]=learner
    criterions = {}
    for restrict in restrictions:
        criterions[restrict.criterion] = {"importance": restrict.importance, "group_type": restrict.group_type}
    grouped_learners = grouping1(learners_map, criterions)
    logger.bind(log_type="business").info("Grouping completed")
    return {"groups":grouped_learners}
    #return {"groups": grouped_learners}


if __name__ == "__main__":
    setup_async_logging()
    uvicorn.run(app,
                host="127.0.0.1",
                port=8080,
                log_config=None,
                access_log=False
            )

    