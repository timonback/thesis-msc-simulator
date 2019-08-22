import logging

from .configuration import Configuration
from .load.all import Loads
from .load.load_generator import LoadGenerator
from .request.request_generator import RequestGenerator
from .simulator_result import SimulatorResult
from .world import World

logger = logging.getLogger(__name__)


class Simulator:
    """
    Simulator to run the simulation using a configuration in a world
    """

    def __init__(self, configuration: Configuration, world: World, request_generation: RequestGenerator,
                 log_progress=False):
        self.config = configuration
        self.world = world
        self.request_generator = request_generation
        self.log_progress = log_progress

    def run(self, load_generator: LoadGenerator = None) -> (SimulatorResult, list):
        """
        Start the simulation. Load is generated by the load_generator. Otherwise, a load_generator based on the
        configuration is created
        :param load_generator: An optional LoadGenerator
        :return: The SimulatorResult as well as the recorded requests
        """
        history = list()
        instances = list()
        queued = list()
        requests = list()

        if load_generator is None:
            load_generator = Loads.get_load(self.config)

        for i in range(
                self.config.simulation_start,
                self.config.simulation_end):
            requests_amount = load_generator.get_load_interval(i)
            new_instances, requests = self._run_step(i, requests_amount)

            if self.log_progress and i % 100 == 0:
                logger.info('Current step is {step} out of {max} ({percent}%)'
                            .format(step=i, max=self.config.simulation_end,
                                    percent=(round(i / self.config.simulation_end * 100))))
            logger.debug('Step {step}: {instances} new instance(s) were added'.
                         format(step=i, instances=len(new_instances)))

            instances.append(new_instances)
            queued.append(self.world.get_queued())
            requests.append(requests)

        result = SimulatorResult(instances, queued)
        return result, requests

    def _run_step(self, step: int, requests_amount: int) -> (list, list):
        """
        Run a single simulation step
        :param step: The current step
        :param requests_amount: The amount of incoming requests
        :return: (new_instances, requests) Tuple with the new instances and the generated requests
        """
        requests = self.request_generator.generate(requests_amount, step, self.config.request_duration,
                                                   self.config.request_memory)
        logger.debug('Step {step}: {requests} new requests'.
                     format(step=step, requests=len(requests)))
        required_instances = self.world.handle_requests(requests, step)
        return required_instances, requests

    def _gen_result(self, history: list) -> (SimulatorResult, list):
        """
        Generate the SimulatorResult of this simulation run
        :param history: The collected data during the simulation run
        :return: The SimulatorResult as well as the recorded requests
        """
        instances = list()
        queued = list()
        requests = list()
        for history_step in history:
            instances.append(history_step['instances'])
            queued.append(history_step['queued'])
            requests.append(history_step['requests'])
        result = SimulatorResult(instances, queued)
        return result, requests
