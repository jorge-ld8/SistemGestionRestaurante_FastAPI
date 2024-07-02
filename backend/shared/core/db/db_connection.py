from database import engine
from database import Session, Base

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()