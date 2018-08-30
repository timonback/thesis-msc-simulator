from simulator.configuration import Configuration


class ConfigurationUtil:
    """
    Util to fix certain aspects of the configuration for testing
    """

    @staticmethod
    def create() -> Configuration:
        config = Configuration()
        config.simulation_start = 0
        config.simulation_end = 10

        config.request_duration = 2
        config.request_memory = 255
        config.request_variation = 0.0

        config.vm_parallel = 2
        config.vm_scaling_degradation = 0.00
        config.vm_min_instances = 0
        config.vm_auto_scaling = True
        config.faas_performance_m = 0
        config.faas_performance_a = 1

        config.load_name = "constant"
        config.load_altitude = 3
        config.load_spacing = 20

        config.plotting = False

        return config
