import copy
import logging
import os

from simulator.configuration import Configuration
from simulator.load.load_generator import LoadGenerator
from simulator.plot import plot
from simulator.request.random_request_generator import RandomRequestGenerator
from simulator.request.replay_request_generator import ReplayRequestGenerator
from simulator.request.request_generator import RequestGenerator
from simulator.resource.instance_creator import InstanceCreator
from simulator.resource.instance_creator_faas import InstanceCreatorFaaS
from simulator.resource.instance_creator_vm import InstanceCreatorVm
from simulator.simulation_archive import SimulationArchive
from simulator.simulation_result import SimulationResult
from simulator.simulator import Simulator, SimulatorResult
from simulator.world import World

logger = logging.getLogger(__name__)


class SimulationRunner:
    """
    Class to ease the use of the simulation.
    Using the supplied configuration, a simulation is run and the results returned.
    Results are cached.
    """

    def __init__(self, config: Configuration):
        """
        Initalizes the simulator
        :param config: The configuration used to run the simulation. Values regarding the simulation can still be
        changed later.
        """
        self.config = config
        self.archive = SimulationArchive(config)

    def run(self, load_generator: LoadGenerator = None) -> SimulationResult:
        """
        Start the simulation. Configurations values are read during run-time from the constructor object.
        First it processes all requests with VMs and then starts replacing VMs with FaaS instances.
        Note: This always re-runs the simulation. Check the cache beforehand for previous simulation runs.
        :param load_generator: Use a custom load-generator. If None, the load generator creates a load based on the
        values from the configuration. This is useful if a LoadRandomizer is desired
        :return: dict() where the keys are the amount of VMs and the value is the according SimulatorResult
        """
        logger.info('Start simulation for config: {config}'.format(config=self.config.get_ident_values()))

        request_generator = RandomRequestGenerator(self.config.request_variation, self.config.request_generator_seed)
        # load = LoadRandomizer(load, config.load_generator_seed, config.load_generator_non_zeros)

        # run vm simulation
        logger.info('Start the simulation')
        instance_creator_vm = InstanceCreatorVm(self.config)
        result, requests = self._simulate(instance_creator_vm, request_generator, load_generator, log_progress=True)

        simulation_result = SimulationResult(copy.deepcopy(self.config), requests)
        simulation_result.add_simulator_result(result.total_instances, result)
        logger.info('Total cost: {cost} [instances: {instances}]'
                    .format(cost=result.total_cost, instances=result.total_instances))
        logger.info('Finished the simulation')

        # simulate with starting to replace vms by FaaS
        logger.info('Start the patching')
        self._patch(simulation_result, result)
        logger.info('Finished the patching')

        return simulation_result

    def _simulate(self, instance_creator: InstanceCreator, request_generator: RequestGenerator,
                  load_generator: LoadGenerator = None, log_progress=False) -> (SimulatorResult, list):
        """
        Runs a single simulation. To process the incoming requests by the request_generator (quantity per simulation
        step determinted by the load_generator), new instances are created using the instance_creator.
        :param instance_creator: InstanceCreator, to create instances
        :param request_generator: RequestGenerator, to create requests
        :param load_generator: LoadGenerator, to generate load
        :return: SimulatorResult
        """
        world = World(instance_creator)

        simulator = Simulator(self.config, world, request_generator, log_progress)
        result, requests = simulator.run(load_generator)

        return result, requests

    def _patch(self, simulation_result: SimulationResult, simulator_result: SimulatorResult) -> SimulationResult:
        """
        Replace iteratively VM instances with FaaS instances
        :param simulation_result: The SimulationResult that will be patched
        :param simulator_result: The all VM SimulatorResult
        :return: the adjusted SimulatorResult
        """
        instance_creator_faas = InstanceCreatorFaaS(self.config)

        # create a clone, due to in-place modifications
        patched_simulator_result = copy.deepcopy(simulator_result)

        replace_instances = self._generate_instance_replace_order(patched_simulator_result)
        for i in range(0, len(replace_instances)):
            logger.info('Patching vm instance {i} out of {total}'.format(i=i + 1, total=len(replace_instances)))
            instance = replace_instances[i]

            # remove instance and collect the requests
            unhandled_requests = list()
            for unhandled_request_step in patched_simulator_result.queued:
                unhandled_requests.extend(unhandled_request_step)
            if hasattr(instance, 'requests') is True:
                unhandled_requests.extend(instance.requests)
                for index, instances in enumerate(patched_simulator_result.instances):
                    if instance in instances:
                        patched_simulator_result.instances[index].remove(instance)
                        break

            # re-simulate the unhandled_requests and get newly generated faas instances
            replayer = ReplayRequestGenerator(unhandled_requests)
            load_replay = replayer.get_load()
            result, requests = self._simulate(instance_creator_faas, replayer, load_generator=load_replay)

            # merge results together
            patched_simulator_result = SimulatorResult.merge(result,
                                                             SimulatorResult(patched_simulator_result.instances,
                                                                             [[] for i in range(len(
                                                                                 patched_simulator_result.instances))]))

            merged_result_copy = copy.deepcopy(patched_simulator_result)
            simulation_result.add_simulator_result(simulator_result.total_instances - i - 1, merged_result_copy)
            logger.info('Total cost: {cost} [instances: {instances}]'
                        .format(cost=patched_simulator_result.total_cost,
                                instances=patched_simulator_result.total_instances))
        return simulation_result

    def _generate_instance_replace_order(self, simulator_result: SimulatorResult) -> list:
        instances = list()
        for instances_step in simulator_result.instances:
            instances.extend(instances_step)
        instances = sorted(instances, key=lambda x: x.utilization)
        return instances

    def load_cache(self) -> SimulationResult:
        """
        Get a cached SimulatorResult based on the configuration
        :return: SimulatorResult if it exists, otherwise None
        """
        if self.archive.exists(self.config):
            return self.archive.retrieve(self.config)
        return None

    def persist(self, simulation_result: SimulationResult, extra_ident_keys: list = list()):
        """
        Save a SimulatorResult to disk
        :param simulation_result: The SimulationResults
        :param extra_ident_keys: extra identification items for the filename
        """
        if os.path.exists(self.config.plotting_folder) is False:
            os.mkdir(self.config.plotting_folder)

        logger.info('Persisting to archive and plotting...')

        self.archive.save(simulation_result)

        plotting_paths = list()
        if self.config.plotting:
            ident = extra_ident_keys + self.config.get_ident_values()
            for num_vms, result in simulation_result.simulations.items():
                ident_vm = ident + [str(num_vms)]
                filename = ('_'.join(ident_vm)) + '.json'

                logger.debug('Plot for {} VMs'.format(num_vms))
                path = plot(result, simulation_result.requests, self.config.plotting_folder + filename)
                plotting_paths.append(path)

        logger.info('Persisting to archive and plotting... Done')
        return plotting_paths
