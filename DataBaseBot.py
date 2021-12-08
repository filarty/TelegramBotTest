from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from settings import DATABASE

engine = create_engine(DATABASE)
Base = declarative_base()
connection = engine.connect()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()