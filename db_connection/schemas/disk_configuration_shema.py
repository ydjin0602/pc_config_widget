from marshmallow import Schema, fields


class DiskConfigurationSchema(Schema):
    file_system_type = fields.Str()
    total_memory = fields.Str()
    available = fields.Str()
    used = fields.Str()
    used_in_percents = fields.Str()
