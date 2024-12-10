from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your MySQL connection details
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/blog_crud"

# Create the engine
engine = create_engine(DATABASE_URL)

# Create a session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()    

