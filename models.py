from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"      