import platform
import socket
import re
import uuid

import psutil
from pyspectator.computer import Computer


class PCConfiguration:
    def __init__(self, token: str):
        os_info = platform.uname()
        ram_info = psutil.virtual_memory()
        disk_info = psutil.disk_partitions()
        disk_memory_info = psutil.disk_usage(disk_info[0].mountpoint)

        self.config = {
            'token': token,
            'os': {
                'name': os_info.system,
                'version': os_info.version,
            },
            'processor': {
                'name': Computer().processor.name,
                'architecture': platform.processor(),
                'total_cores': psutil.cpu_count(logical=True),
                'max_frequency': f'{psutil.cpu_freq().max:.2f}Mhz',
                'current_frequency': f'{psutil.cpu_freq().current:.2f}Mhz',
                'temperature': f'{psutil.sensors_temperatures()["k10temp"][0].current}°C',
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
        }

    def update(self):
        ram_info = psutil.virtual_memory()
        disk_info = psutil.disk_partitions()
        disk_memory_info = psutil.disk_usage(disk_info[0].mountpoint)
        self.config.update(
            {
                'processor': {
                    'name': Computer().processor.name,
                    'architecture': platform.processor(),
                    'total_cores': psutil.cpu_count(logical=True),
                    'max_frequency': f'{psutil.cpu_freq().max:.2f}Mhz',
                    'current_frequency': f'{psutil.cpu_freq().current:.2f}Mhz',
                    'temperature': f'{psutil.sensors_temperatures()["k10temp"][0].current}°C',
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
            }
        )

    @staticmethod
    def get_cpu_per_core():
        cpu_usage_per_core = ''
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            cpu_usage_per_core += f"Core {i}: {percentage}%\n"
        return cpu_usage_per_core

    @staticmethod
    def get_size(size_in_bytes):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if size_in_bytes < factor:
                return f"{size_in_bytes:.2f}{unit}B"
            size_in_bytes /= factor
