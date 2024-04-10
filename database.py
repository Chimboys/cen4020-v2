from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
SQLALCHEMY_DATABASE_URL = 'postgresql://test:admin@localhost:5432/test5'
Base = declarative_base()  # Define Base before using it

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


Base = declarative_base()
Base.metadata.create_all(engine)  # Now you can use Base
