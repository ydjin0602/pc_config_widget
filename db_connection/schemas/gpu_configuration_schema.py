from marshmallow import Schema, fields


class GPUConfigurationSchema(Schema):
    name = fields.Str()
    temperature = fields.Str()
    loading = fields.Str()
    total_memory = fields.Str()
    available = fields.Str()
    used = fields.Str()
    used_in_percents = fields.Str()
