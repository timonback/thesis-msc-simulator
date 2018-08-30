from simulator.configuration import Configuration
from simulator.simulator_result import SimulatorResult


class SimulationResult:
    """
    The complete result of a simulation (including VM to FaaS patching)
    """

    def __init__(self, config: Configuration, requests: list):
        """Config under which the simulation was run"""
        self.config = config
        """New requests per simulation step"""
        self.requests = requests
        """Mapping of the amouont of VMs to SimulatorResult"""
        self.simulations = dict()

    def add_simulator_result(self, amount_vms: int, result: SimulatorResult):
        if len(self.simulations) != 0:
            dict_ele = next(iter(self.simulations.values()))
            if len(dict_ele.cost_steps) != len(result.cost_steps):
                raise ValueError('This result does not fit the previous runs.')
        else:
            if (self.config.simulation_end - self.config.simulation_start) != len(result.cost_steps):
                raise ValueError('The amount of recorded simulation steps does not match the config')

        self.simulations[amount_vms] = result

    def __eq__(self, o: object):
        if not isinstance(o, SimulationResult):
            return False
        return \
            self.config == o.config and \
            self.requests == o.requests and \
            self.simulations == o.simulations

    def __str__(self):
        return str(self.__dict__)
