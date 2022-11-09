from pprint import pprint
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range, ValidationError

class TagInfo(Schema):
    name = fields.String(required=True)


class UserCreate(Schema):
    first_name = fields.String(required=True, error_messages={"required": "first_name is required."})
    last_name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=6))

class UserUpdate(Schema):
    first_name = fields.String(error_messages={"required": "first_name is required."})
    last_name = fields.String()
    username = fields.String()
    email = fields.Email()
    password = fields.String(validate=Length(min=6))
   
class UserInfo(Schema):
    first_name = fields.String(error_messages={"required": "first_name is required."})
    last_name = fields.String()
    username = fields.String()
    email = fields.Email()
    password = fields.String(validate=Length(min=6), load_only=True)
    numOfNotes = fields.Integer()
    numOfEditingNotes = fields.Integer()
    dateOfCreating = fields.DateTime(dump_only=True)


class NoteCreate(Schema):
    owner_id = fields.Integer(required=True)
    title = fields.String(required=True)
    isPublic = fields.Boolean(default=False)
    text = fields.String(required=True, validate=Length(max=404))
    tags = fields.List(fields.Nested(TagInfo))


class NoteUpdate(Schema):
    title = fields.String()
    isPublic = fields.Boolean(default=False)
    text = fields.String(validate=Length(max=404))
    tags = fields.List(fields.Nested(TagInfo))
    dateOfEditting = fields.DateTime(dump_only=True)

class AllowNote(Schema):
    note_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)

class NoteInfo(Schema):
    owner_id = fields.Integer(required=True)
    title = fields.String(required=True)
    isPublic = fields.Boolean(default=False)
    text = fields.String(required=True, validate=Length(max=404))
    tags = fields.List(fields.Nested(TagInfo))
    editors = fields.List(fields.Nested(AllowNote))
    dateOfEditting = fields.DateTime()







# tag_note = [{"name": "Dasha"},{"name": "Lizo"}]
# Note = {"owner_id": 1, "title":"s", "isPublic":True, "text":"dd", "tags": tag_note}

# result = NoteCreate().load(Note)
# pprint(result)