from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("postgresql://postgres:24062004@localhost:5432/toksim4")
Session = sessionmaker(bind=engine)

BaseModel = declarative_base()


class Users(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    numOfNotes = Column(Integer, nullable=False)
    numOfEditingNotes = Column(Integer, nullable=False)
    dateOfCreating = Column(DATE, nullable=False)


class Notes(BaseModel):
    __tablename__ = "notes"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    isPublic = Column(BOOLEAN, nullable=False)
    text = Column(String, nullable=False)
    dateOfEditing = Column(DATE, nullable=False)

    user = relationship(Users, foreign_keys=[owner_id], backref="notes", lazy="joined")


class Tags(BaseModel):
    __tablename__ = "tags"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    text = Column(String, nullable=False)


class TagNote(BaseModel):
    __tablename__ = "tag_note"

    note_id = Column(Integer, ForeignKey('notes.id'), primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True, nullable=False)

    tag = relationship(Tags, foreign_keys=[tag_id], backref="TagNote", lazy="joined")
    note = relationship(Notes, foreign_keys=[note_id], backref="TagNote", lazy="joined")



class Editors(BaseModel):
    __tablename__ = "editors"

    note_id = Column(Integer, ForeignKey('notes.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)

    user = relationship(Users, foreign_keys=[user_id], backref="allowedNotes", lazy="joined")
    note = relationship(Notes, foreign_keys=[note_id], backref="allowedNotes", lazy="joined")
