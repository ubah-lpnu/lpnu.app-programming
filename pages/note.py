from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from model_objects import Session, Notes, TagNote, Tags, Users, Editors
from validation_schemas import NoteCreate, NoteUpdate, AllowNote, NoteInfo
from sqlalchemy.exc import NoResultFound
from datetime import datetime
import json
import pprint

note = Blueprint('note', __name__, url_prefix='/note')
session = Session()

@note.route('/', methods=['POST'])
def create_note():
    try:
        note = NoteCreate().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    try:
        userCreate = session.query(Users).filter_by(id=note['owner_id']).one()
    except NoResultFound:
         return {"message": "Owner could not be found."}, 400
        
    exist_title = session.query(Notes).filter_by(title=note['title']).first()
    if exist_title:
        return Response(status=404, response='This title has already exist.')    

    tagInTable = []
    for item in note['tags']:
        try:
             session.query(Tags.id).filter(item['name'] == Tags.name).one()
        except NoResultFound:
            return {"message": "Tag could not be found."}, 400
        tagInTable.append(session.query(Tags.id).filter(item['name'] == Tags.name).scalar())
    

    if len(tagInTable) > len(set(tagInTable)):
        return jsonify({"message": "Can't use the same tag again"}), 400

    
    newNote = Notes(owner_id=note['owner_id'], title=note['title'], isPublic=note['isPublic'], text=note['text'])
   
    session.add(newNote)
    session.commit()
    userCreate.numOfNotes +=1
    idd = newNote.id
    
    for i in range(len(tagInTable)):
        newConnection = TagNote(note_id=idd, tag_id = tagInTable[i])
        session.add(newConnection)

    session.commit()
    
    return Response(response="Note was added successfully")


@note.route('/<int:note_update_id>', methods=['PUT'])
def update_note(note_update_id):
    try:
        note_update = NoteUpdate().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    db_note = session.query(Notes).filter_by(id=note_update_id).first()
    if not db_note:
        return Response(status=404, response='An Note with provided ID was not found.')

    if 'title' in note_update.keys():
        existsTitle = session.query(Notes).filter_by(title=note_update['title']).first()
        if existsTitle:
            return Response(status=400, response='Note with such title already exists.')
        db_note.title = note_update['title']
    if 'isPublic' in note_update.keys():
        db_note.last_name = note_update['isPublic']
    if 'text' in note_update.keys():
        db_note.text = note_update['text']
    if 'tags' in note_update.keys():
        tagInTable = []
        for item in note_update['tags']:
            try:
                session.query(Tags.id).filter(item['name'] == Tags.name).one()
            except NoResultFound:
                return {"message": "Tag could not be found."}, 400
            tagInTable.append(session.query(Tags.id).filter(item['name'] == Tags.name).scalar())
       
        if len(tagInTable) > len(set(tagInTable)):
            return jsonify({"message": "The tag is already used"}), 400

        try:
            for i in range(len(tagInTable)):
                newConnection = TagNote(note_id=note_update_id, tag_id = tagInTable[i])
                session.add(newConnection)
        except:
            session.rollback()
            return jsonify({"Touble"}),500
    userUpdate = session.query(Users).filter_by(id=4).one()
    userUpdate.numOfEditingNotes +=1
    current_dateTime = datetime.now()
    db_note.dateOfEditing = current_dateTime
    session.commit()
    
    return Response(response="Note was updated successfully")


@note.route('/allowed', methods=['POST'])
def give_rights():
    try:
        edit = AllowNote().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    db_note = session.query(Notes).filter_by(id=edit['note_id']).first()
    if not db_note:
        return Response(status=404, response='An Note with provided ID was not found.')

    db_user = session.query(Users).filter_by(id=edit['user_id']).first()
    if not db_user:
        return Response(status=404, response='An User with provided ID was not found.')

    selfRight = session.query(Notes).filter_by(owner_id=edit['user_id']).first()
    if selfRight:
        return Response(status=405, response='Owner cannot be editor')

    exists = session.query(
        session.query(Editors).filter_by(note_id=edit['note_id']).filter_by(user_id=edit['user_id']).exists()
        ).scalar()
    if exists:
        return Response(status=500, response='Already exist')

    giveEdit = Editors(user_id=edit['user_id'], note_id=edit['note_id'])
    session.add(giveEdit)
    session.commit()

    return Response(response="New editor was added.")

@note.route('/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    
    db_note = session.query(Notes).filter_by(id=note_id).first()
    if not db_note:
        return Response(status=404, response='An user with provided ID was not found.')

    session.delete(db_note)
    session.commit()
    return Response(response='Note was deleted.')



@note.route('/<int:note_get_id>', methods=['GET'])
def get_note(note_get_id):
    note_get = session.query(Notes).filter_by(id=note_get_id).first()
    if not note_get:
        return Response(status=404, response='An Note with provided ID was not found.')
    editors_note = []
    for editors in session.query(Editors).filter(Editors.note_id == note_get_id):
        user = session.query(Users).filter_by(id=editors.user_id).first()
        editors_note.append({"username":user.username, 'email':user.email})
    tag_note = []
    for tags in session.query(TagNote).filter(TagNote.note_id == note_get_id):
        tag = session.query(Tags).filter_by(id=tags.tag_id).first()
        tag_note.append({'name':tag.name})
    note_data = {
        'owner_id': note_get.owner_id,
        'title': note_get.title,
        'isPublic': note_get.isPublic,
        'text': note_get.text,
        'dateOfEditing':note_get.dateOfEditing,
        'editors':editors_note,
        'tags':tag_note
    }
    return jsonify({"note":note_data})