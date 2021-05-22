from marshmallow import Schema, fields


class RAMConfigurationSchema(Schema):
    total_memory = fields.Str()
    available = fields.Str()
    used = fields.Str()
    used_in_percents = fields.Str()
