import requests
from marshmallow import ValidationError
from json import JSONDecodeError

from config import CONFIGURATION
from db_connection.schemas.pc_configuration_schema import PCConfigurationSchema


class DBConnectionManager:

    __RECORD_SCHEMA = PCConfigurationSchema()

    def create(self, data):
        try:
            request_body = self.__RECORD_SCHEMA.load(data)
        except ValidationError as exception:
            raise exception

        response = requests.post(
            url=CONFIGURATION.db_manager_url,
            json=request_body,
            headers={
                'Content-type': 'application/json'
            }
        )

        try:
            response_body = response.json()
            self.__RECORD_SCHEMA.load(response_body)
        except (ValidationError, JSONDecodeError) as exception:
            raise exception

    def update(self, data):
        try:
            request_body = self.__RECORD_SCHEMA.load(data)
        except ValidationError as exception:
            raise exception
        response = requests.put(
            url=CONFIGURATION.db_manager_url,
            json=request_body,
            headers={
                'Content-type': 'application/json'
            }
        )

        try:
            response_body = response.json()
            self.__RECORD_SCHEMA.load(response_body)
        except (ValidationError, JSONDecodeError) as exception:
            raise exception
