from marshmallow import Schema, fields


class SocketConfigurationSchema(Schema):
    host = fields.Str()
    ip_address = fields.Str()
    mac_address = fields.Str()
