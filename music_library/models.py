from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __str__(self):
        return self.name