import logging
import os
import pickle

from simulator.configuration import Configuration
from simulator.simulation_result import SimulationResult

logger = logging.getLogger(__name__)


class SimulationArchiveIndex:
    def __init__(self, config, requests):
        self.config = config
        self.requests = requests
        self.index = dict()


class SimulationArchive:
    FILENAME_JOIN_STR = '_'
    JSON_EXT = '.pickle'

    def __init__(self, config: Configuration):
        self.config = config

        if os.path.exists(self._get_archive_folder()) is False:
            os.mkdir(self._get_archive_folder())

    def exists(self, config: Configuration) -> bool:
        ident = config.get_ident_values()
        path = self._get_archive_folder() + self.FILENAME_JOIN_STR.join(ident) + self.JSON_EXT
        return os.path.exists(path)

    def retrieve(self, config: Configuration) -> SimulationResult:
        if self.exists(config) is False:
            return None

        ident = config.get_ident_values()
        index_filename = self._get_archive_folder() + self.FILENAME_JOIN_STR.join(ident) + self.JSON_EXT
        with open(index_filename, 'rb') as json_index_file:
            index = pickle.load(json_index_file)

            results = SimulationResult(index.config, index.requests)
            for vms, index_result in index.index.items():
                filename = index_result.strip()
                entry = self._read_file(filename)
                results.add_simulator_result(vms, entry)
        return results

    def _read_file(self, filename: str):
        res = None
        with open(self._get_archive_folder() + filename, 'rb') as file:
            # res = file.read().replace('\n', '')
            res = pickle.load(file)
        return res

    def remove(self, config: Configuration):
        ident = config.get_ident_values()
        path = self._get_archive_folder() + self.FILENAME_JOIN_STR.join(ident) + self.JSON_EXT
        if os.path.exists(path):
            os.remove(path)

    def save(self, result: SimulationResult):
        # Assumption: All results have the same configuration settings
        ident = result.config.get_ident_values()
        logger.debug('Archiving {ident}...'.format(ident=ident))

        # Write first in temporary file, in case execution is interrupted
        index_filename = self._get_archive_folder() + self.FILENAME_JOIN_STR.join(ident) + self.JSON_EXT
        index_filename_tmp = index_filename + '.tmp'

        try:
            index = SimulationArchiveIndex(result.config, result.requests)
            with open(index_filename_tmp, 'wb') as json_index_file:
                for num_vms, result in result.simulations.items():
                    ident_vm = ident + [str(num_vms)]
                    filename = (self.FILENAME_JOIN_STR.join(ident_vm)) + self.JSON_EXT

                    # single results
                    try:
                        with open(self._get_archive_folder() + filename, 'wb') as json_file:
                            pickle.dump(result, json_file)
                        index.index[num_vms] = filename
                    except Exception as e:
                        logger.exception('Error while saving {ident}'.format(ident=ident_vm))

                pickle.dump(index, json_index_file)
            os.replace(index_filename_tmp, index_filename)

            logger.debug('Archiving {ident} Done'.format(ident=ident))
        except Exception as e:
            logger.exception('Error while saving the index file')

    def _get_archive_folder(self) -> str:
        return self.config.archive_folder
