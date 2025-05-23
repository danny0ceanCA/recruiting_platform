from app.db.session import engine
from app.db.session import Base
from app.models.student import Student
from app.models.user import User
from app.models.job import Job  #  register the Job model

def create_tables():
    Base.metadata.drop_all(bind=engine)  # dev only: clears existing tables
    Base.metadata.create_all(bind=engine)  # recreate all tables

if __name__ == "__main__":
    create_tables()
    print("Tables created!")
