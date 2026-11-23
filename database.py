from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

Base = declarative_base()

url = "sqlite:///./student_portal.db"

engine = create_engine(
    url

)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
