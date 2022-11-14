from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import orm

engine = create_engine("postgresql://postgres:30062003@localhost:5432/SysNotes")
Session = orm.scoped_session(orm.sessionmaker())
Session.configure(bind=engine)
