from marshmallow import Schema, fields


class OSConfigurationSchema(Schema):
    name = fields.Str()
    version = fields.Str()
