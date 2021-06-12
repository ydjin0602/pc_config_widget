import platform
import socket
import re
import uuid

import psutil
from GPUtil import GPUtil
from pyspectator.computer import Computer

from pc_configuration.os_enum import OSName


class PCConfiguration:
    def __init__(self, token: str):

        os_info = platform.uname()

        self.system_name = os_info.system

        ram_info = psutil.virtual_memory()
        disk_info = psutil.disk_partitions()
        disk_memory_info = psutil.disk_usage(disk_info[0].mountpoint)
        gpu_info = GPUtil.getGPUs()[0]

        self.config = {
            'token': token,
            'os': {
                'name': self.system_name,
                'version': os_info.version,
            },
            'processor': {
                'total_cores': psutil.cpu_count(logical=True),

                'max_frequency': f'{psutil.cpu_freq().max}Mhz',
                'current_frequency': f'{psutil.cpu_freq().current:.2f}Mhz',
                'loading': f'{psutil.cpu_percent()}%',
                'usage_per_core': self.get_cpu_per_core(),
            },
            'socket_info': {
                'host': socket.gethostname(),
                'ip_address': socket.gethostbyname(socket.gethostname()),
                'mac_address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            },
            'disk': {
                'file_system_type': disk_info[0].fstype,
                'total_memory': self.get_size(disk_memory_info.total),
                'available': self.get_size(disk_memory_info.free),
                'used': self.get_size(disk_memory_info.used),
                'used_in_percents': f'{disk_memory_info.percent}%',
            },
            'ram': {
                'total_memory': self.get_size(ram_info.total),
                'available': self.get_size(ram_info.available),
                'used': self.get_size(ram_info.used),
                'used_in_percents': f'{ram_info.percent}%',
            },
            'gpu': {
                'name': gpu_info.name,
                'temperature': f'{gpu_info.temperature}°C',
                'loading': f'{gpu_info.load}%',
                'total_memory': f'{gpu_info.memoryTotal}MB',
                'available': f'{gpu_info.memoryFree}MB',
                'used': f'{gpu_info.memoryUsed}MB',
                'used_in_percents': f'{gpu_info.memoryUsed / gpu_info.memoryTotal * 100:.2f}%'
            }
        }

        if self.system_name == OSName.LINUX.value:
            self.config['processor'].update(
                {
                    'name': Computer().processor.name,
                    'architecture': platform.processor(),
                    'temperature': f'{psutil.sensors_temperatures()["k10temp"][0].current}°C'
                }
            )

        if self.system_name == OSName.WINDOWS.value:
            self.config['processor'].update(
                {
                    'name': self.get_processor_name(),
                    'architecture': platform.architecture()[0],
                    'temperature': 'Unavailable for OS Windows'
                }
            )

    def update(self):
        ram_info = psutil.virtual_memory()
        disk_info = psutil.disk_partitions()
        disk_memory_info = psutil.disk_usage(disk_info[0].mountpoint)
        gpu_info = GPUtil.getGPUs()[0]
        self.config.update(
            {
                'processor': {
                    'architecture': platform.processor(),
                    'total_cores': psutil.cpu_count(logical=True),
                    'max_frequency': f'{psutil.cpu_freq().max}Mhz',
                    'current_frequency': f'{psutil.cpu_freq().current:.2f}Mhz',
                    'loading': f'{psutil.cpu_percent()}%',
                    'usage_per_core': self.get_cpu_per_core(),
                },
                'disk': {
                    'file_system_type': disk_info[0].fstype,
                    'total_memory': self.get_size(disk_memory_info.total),
                    'available': self.get_size(disk_memory_info.free),
                    'used': self.get_size(disk_memory_info.used),
                    'used_in_percents': f'{disk_memory_info.percent}%',
                },
                'ram': {
                    'total_memory': self.get_size(ram_info.total),
                    'available': self.get_size(ram_info.available),
                    'used': self.get_size(ram_info.used),
                    'used_in_percents': f'{ram_info.percent}%',
                },
                'gpu': {
                    'name': gpu_info.name,
                    'temperature': f'{gpu_info.temperature}°C',
                    'loading': f'{gpu_info.load}%',
                    'total_memory': f'{gpu_info.memoryTotal}MB',
                    'available': f'{gpu_info.memoryFree}MB',
                    'used': f'{gpu_info.memoryUsed}MB',
                    'used_in_percents': f'{gpu_info.memoryUsed / gpu_info.memoryTotal * 100:.2f}%'
                }
            }
        )

        if self.system_name == OSName.LINUX.value:
            self.config['processor'].update(
                {
                    'name': Computer().processor.name,
                    'architecture': platform.processor(),
                    'temperature': f'{psutil.sensors_temperatures()["k10temp"][0].current}°C'
                }
            )

        if self.system_name == OSName.WINDOWS.value:
            self.config['processor'].update(
                {
                    'name': self.get_processor_name(),
                    'architecture': str(platform.architecture()[0]),
                    'temperature': f'Unavailable for OS Windows'
                }
            )

    @staticmethod
    def get_cpu_per_core():
        cpu_usage_per_core = ''
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            cpu_usage_per_core += f"Core {i + 1}: {percentage}%\n"
        return cpu_usage_per_core

    @staticmethod
    def get_size(size_in_bytes):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if size_in_bytes < factor:
                return f"{size_in_bytes:.2f}{unit}B"
            size_in_bytes /= factor

    @staticmethod
    def get_processor_name():
        from winreg import ConnectRegistry, OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE

        registry_connection = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        registry_key = OpenKey(registry_connection, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        name = QueryValueEx(registry_key, 'ProcessorNameString')[0]
        return name
