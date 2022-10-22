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
    userstatus = Column(BOOLEAN, nullable=False)


class Notes(BaseModel):
    __tablename__ = "notes"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    ispublic = Column(BOOLEAN, nullable=False)
    text = Column(String, nullable=False)
    dateofediting = Column(DATE, nullable=False)

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


class Stats(BaseModel):
    __tablename__ = "stats"

    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    numofnotes = Column(Integer, nullable=False)
    numofeditingnotes = Column(Integer, nullable=False)
    dateofcreating = Column(DATE, nullable=False)

    user = relationship(Users, foreign_keys=[user_id], backref="stats", lazy="joined")


class AllowedNotes(BaseModel):
    __tablename__ = "allowed_notes"

    note_id = Column(Integer, ForeignKey('notes.id'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)

    user = relationship(Users, foreign_keys=[user_id], backref="allowedNotes", lazy="joined")
    note = relationship(Notes, foreign_keys=[note_id], backref="allowedNotes", lazy="joined")
