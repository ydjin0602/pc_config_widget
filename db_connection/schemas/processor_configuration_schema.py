from marshmallow import Schema, fields


class ProcessorConfigurationSchema(Schema):
    name = fields.Str()
    architecture = fields.Str()
    total_cores = fields.Int()
    max_frequency = fields.Str()
    current_frequency = fields.Str()
    temperature = fields.Str()
    loading = fields.Str()
    usage_per_core = fields.Str()
