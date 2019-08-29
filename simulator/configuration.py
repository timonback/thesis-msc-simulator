import typing
from decimal import *

getcontext().prec = 10


class Configuration:
    def __init__(self):
        # Timing limits of the simulation
        self.simulation_start = 0  # in seconds
        self.simulation_end = 3600  # in seconds

        # VM configuration
        """Amount of parallel request. Related to cores per VM"""
        self.vm_parallel = 60
        self.vm_scaling_degradation = 0.00  # 5 percent degradation -> 0.05
        self.vm_min_instances = 0
        self.vm_auto_scaling = True

        # FaaS
        """Performance factor y = a + m * log(<memory in MB>)"""
        self.faas_performance_a = 2.2157
        self.faas_performance_m = -0.3002

        # Request configuration
        self.request_duration = 21.41247  # in seconds
        self.request_memory = 229  # in MB

        # random request generator
        self.request_generator_seed = 10  # seed for the random request generator
        self.request_variation = 0.0  # Percentage variation

        # load generator
        self.load_generator_seed = 10
        self.load_generator_variation = 1
        self.load_generator_non_zeros = True

        # load
        self.load_name = None
        self.load_altitude = 1
        self.load_spacing = 3600
        self.load_num_requests = 10286
        self.load_num_spikes = 1

        # persist
        self.archive_folder = 'archive/'
        self.plotting_folder = 'images/'
        self.plotting = True

    def get_ident(self) -> typing.Dict[str, str]:
        diff_r = str(self.faas_performance_a) + '-' + str(self.faas_performance_m)
        duration = round(self.request_duration, 5)
        return {
            'load': str(self.load_name),
            'altitude': str(self.load_altitude),
            'spacing': str(self.load_spacing),
            'spikes': str(self.load_num_spikes),
            'num_requests': str(self.load_num_requests),
            'simulation_end': str(self.simulation_end),
            'request_memory': str(self.request_memory),
            'request_duration': str(duration),
            'performance_degradation': str(diff_r),
        }

    def get_ident_keys(self) -> typing.List[str]:
        return list(self.get_ident().keys())

    def get_ident_values(self) -> typing.List[str]:
        return list(self.get_ident().values())

    def __eq__(self, o: object):
        if not isinstance(o, Configuration):
            return False
        return self.__dict__ == o.__dict__

    def __str__(self):
        return str(self.__dict__)
