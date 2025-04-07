from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlite_file_name = "./database.db"


SQLALCHEMY_DATABASE_URL = f"sqlite:///{sqlite_file_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True,connect_args={"check_same_thread":False})


SessionLocal =  sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base  = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()