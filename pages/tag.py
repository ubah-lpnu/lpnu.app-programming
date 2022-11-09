from flask import Blueprint, Response, request, jsonify
from marshmallow import ValidationError
from flask_bcrypt import Bcrypt
from model_objects import Session, Tags
from validation_schemas import TagInfo

tag = Blueprint('tag', __name__, url_prefix="/tag")
bcrypt = Bcrypt()
session = Session()


@tag.route('/', methods=['POST'])
def add_tag():
    try:
        tag = TagInfo().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    exists = session.query(Tags.id).filter_by(name=tag['name']).first()
    if exists:
        return Response(status=400, response='Tag with such name already exists.')
    new_tag = Tags(name=tag['name'])
    session.add(new_tag)
    session.commit()

    return Response(response='New tag was successfully created!')


@tag.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tagGet = session.query(Tags).filter_by(id=tag_id).first()
    if not tagGet:
        return Response(status=404, response='An tag with provided ID was not found.')
    return TagInfo().dump(tagGet), 200
    
@tag.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    try:
        data = TagInfo().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    db_tag = session.query(Tags).filter_by(id=tag_id).first()
    if not db_tag:
        return Response(status=404, response='An tag with provided ID was not found.')

    exists = session.query(Tags.id).filter_by(name=data['name']).first()
    if exists:
        return Response(status=400, response='Tag with such number already exists.')
    db_tag.name = data['name']
    session.commit()

    return Response(response="The tag was successfully updated")

    
@tag.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    db_tag = session.query(Tags).filter_by(id=tag_id).first()
    if not db_tag:
        return Response(status=404, response='An tag with provided ID was not found.')

    session.delete(db_tag)
    session.commit()
    return Response(response='Tag was deleted.')





