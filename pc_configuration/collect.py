import platform

import psutil


class PCConfiguration:
    def __init__(self, token: str):
        uname = platform.uname()
        self.config = {
            'token': token,
            'os': {
                'name': uname.system,
                'version': uname.version
            },
            'processor': {
                'name': uname.processor,
                'architecture': platform.processor(),
                'total_cores': psutil.cpu_count(logical=True),
                'max_frequency': f'{psutil.cpu_freq().max:.2f}Mhz',
                'current_frequency': f'{psutil.cpu_freq().current:.2f}Mhz',
                'temperature': psutil.sensors_temperatures()['k10temp'][0].current,
                'loading': f'{psutil.cpu_percent()}%'
            }
        }

    def update(self):
        pass
