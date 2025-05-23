import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.db.session import engine
from app.db.base_class import Base
from app.models import User, Student, Job

def create_tables():
    print("Using database URL:", engine.url)
    Base.metadata.drop_all(bind=engine)
    print("Tables to create:", list(Base.metadata.tables.keys()))
    Base.metadata.create_all(bind=engine)
    print("Tables created!")

if __name__ == "__main__":
    create_tables()
