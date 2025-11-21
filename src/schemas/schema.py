from marshmallow import Schema, fields, validate
from marshmallow.fields import BytesField

class SchemaSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    date = fields.DateTime()
    active = fields.Bool()
    email = fields.Email(required=True)
