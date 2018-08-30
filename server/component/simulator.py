import json
import logging
import os

from simulator.configuration import Configuration
from simulator.runner import SimulationRunner
from simulator.simulation_result import SimulationResult
from util.json_encoder import JsonEncoder

logger = logging.getLogger(__name__)


class SimulatorComponent:
    JSON_EXT = '.json'

    def __init__(self, config: Configuration):
        self.config = config
        self.runner = SimulationRunner(config)

    def calc(self) -> SimulationResult:
        cached = self.runner.load_cache()
        if cached is None:
            results = self.runner.run()
            self.runner.persist(results)
            logger.info('Finished simulation for config: {}'.format(self.get_ident()))

            return results
        logger.info('Found simulation cache')
        return cached

    def exists(self):
        return os.path.exists(self.config.archive_folder + self._filename())

    def get_or_calc(self) -> str:
        logger.info('Incoming request for config: {}'.format(self.get_ident()))
        if not self.exists():
            result = self.calc()

            logger.info('Creating webserver json cache')

            # write simulation files
            for vms, simulation in result.simulations.items():
                with open(self.config.archive_folder + self._filename(vms), 'w') as simulation_file:
                    logger.info('Create json cache for vm {vms}'.format(vms=vms))
                    json.dump(simulation, simulation_file, cls=JsonEncoder, indent="\t")

            # write index
            with open(self.config.archive_folder + self._filename(), 'w') as index_file:
                logger.info('Create json index cache')
                obj = dict()
                obj['config'] = result.config
                obj['requests'] = result.requests
                obj['simulations'] = dict()
                for vms, simulation in result.simulations.items():
                    obj['simulations'][vms] = self._filename(vms)
                json.dump(obj, index_file, cls=JsonEncoder, indent="\t")
            logger.info('json cache generation finished')

        logger.info('Finished retrival')
        return self.retrieve()

    def get_ident(self):
        return '_'.join(self.config.get_ident_values())

    def retrieve(self, vms=None):
        res = None
        with open(self.config.archive_folder + self._filename(vms), 'r') as file:
            res = file.readlines()
        return '\n'.join(res)

    def _filename(self, vms=None):
        if vms is None:
            return self.get_ident() + self.JSON_EXT
        return self.get_ident() + "_" + str(vms) + self.JSON_EXT
