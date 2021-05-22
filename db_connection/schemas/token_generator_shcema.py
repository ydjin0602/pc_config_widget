from marshmallow import Schema
from marshmallow.fields import String


class TokenGeneratorSchema(Schema):
    token = String()
