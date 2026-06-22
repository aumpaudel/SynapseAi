from sqlalchemy import Column, String, Integer
from database import Base

class User(Base):
    __tablename__ = 'users'

    sno = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"      