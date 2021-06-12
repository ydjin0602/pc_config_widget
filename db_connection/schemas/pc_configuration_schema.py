from marshmallow import Schema, fields

from db_connection.schemas.disk_configuration_shema import DiskConfigurationSchema
from db_connection.schemas.gpu_configuration_schema import GPUConfigurationSchema
from db_connection.schemas.os_configuration_schema import OSConfigurationSchema
from db_connection.schemas.processor_configuration_schema import ProcessorConfigurationSchema
from db_connection.schemas.ram_configuration_schema import RAMConfigurationSchema
from db_connection.schemas.socket_configuration_schema import SocketConfigurationSchema


class PCConfigurationSchema(Schema):

    token = fields.Str()
    os = fields.Nested(OSConfigurationSchema)
    processor = fields.Nested(ProcessorConfigurationSchema)
    socket_info = fields.Nested(SocketConfigurationSchema)
    disk = fields.Nested(DiskConfigurationSchema)
    ram = fields.Nested(RAMConfigurationSchema)
    gpu = fields.Nested(GPUConfigurationSchema)
