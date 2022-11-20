from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy.orm import backref
import datetime

#engine = create_engine("postgresql://postgres:30062003@localhost:5432/SysNotes")
engine = create_engine("postgresql://postgres:24062004@localhost:5432/notes")

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

BaseModel = declarative_base()


# tag_note = Table(
#     "tag_note",
#     BaseModel.metadata,
#     Column("note_id", Integer, ForeignKey("left_table.id")),
#     Column("tag_id", ForeignKey("right_table.id")),
# )


class Users(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    numOfNotes = Column(Integer, default=0)
    numOfEditingNotes = Column(Integer, default=0)
    dateOfCreating = Column(DateTime, default=func.now())


class Notes(BaseModel):
    __tablename__ = "notes"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    isPublic = Column(BOOLEAN, nullable=False)
    text = Column(String(404), nullable=False)
    dateOfEditing = Column(DateTime)

    # userKey = relationship(Users, foreign_keys=[owner_id], backref="notes", lazy="joined")
    # userKey = relationship(Users, backref=backref('owner', cascade='all,delete'))
    userKey = relationship(Users, backref=backref('owner', cascade='all,delete'))


class Tags(BaseModel):
    __tablename__ = "tags"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    name = Column(String, nullable=False)


class TagNote(BaseModel):
    __tablename__ = "tag_note"

    note_id = Column(Integer, ForeignKey('notes.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    tagKey = relationship(Tags, backref=backref('tags', cascade='all,delete'))
    NoteKey = relationship(Notes, backref=backref('notes', cascade='all,delete'))

    # tagKey = relationship(Tags, foreign_keys=[tag_id], backref="TagNote", lazy="joined")
    # NoteKey = relationship(Notes, foreign_keys=[note_id], backref="TagNote", lazy="joined")


class Editors(BaseModel):
    __tablename__ = "editors"

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    note_id = Column(Integer, ForeignKey('notes.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    userEdKey = relationship(Users, backref=backref('users_ed', cascade='all,delete'))
    noteEdKey = relationship(Notes, backref=backref('note_ed', cascade='all,delete'))

    # userEdKey = relationship(Users, foreign_keys=[user_id], backref="allowedNotes", lazy="joined")
    # noteEdKey = relationship(Notes, foreign_keys=[note_id], backref="allowedNotes", lazy="joined")
