from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import models so alembic can see them.  Doing this after the Base class to avoid a circular import error.
# from app.models.service import Service