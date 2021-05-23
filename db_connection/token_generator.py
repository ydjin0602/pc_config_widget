import requests
from marshmallow import ValidationError
from json import JSONDecodeError

from config import CONFIGURATION
from db_connection.schemas.token_generator_shcema import TokenGeneratorSchema


def get_token():
    response_schema = TokenGeneratorSchema()

    try:
        generator_response = requests.get(CONFIGURATION.token_generator_url)
    except requests.exceptions.RequestException as exception:
        raise exception

    try:
        response_body = generator_response.json()
        response_data = response_schema.load(response_body)
    except (ValidationError, JSONDecodeError) as exception:
        raise exception

    return response_data['token']
