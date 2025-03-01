from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
class Learner(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    capability: int
    gender: int
    style: int


class UserInDB(SQLModel, table=True):
    username:str = Field(primary_key=True, default=None)
    hashed_password: str
    disabled:bool|None=None
    

DATABASE_URL = "mysql+pymysql://root:123456@localhost/mydatabase"
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SQLModel.metadata.create_all(engine)