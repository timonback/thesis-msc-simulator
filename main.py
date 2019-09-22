import csv
import logging

from simulator.configuration import Configuration
from simulator.runner import SimulationRunner
from tests.profiler import profiling_start, register_profiling_atexit
from util.logger import setup_logging

profiling_start()
register_profiling_atexit()


def main():
    setup_logging('main.log', level=logging.INFO)

    # use-case configuration
    param = 131072
    request_memory = 229
    vm_request_duration = 30575.03 / 1000  # in seconds

    # prepare the simulation
    config = Configuration()
    runner = SimulationRunner(config)

    config.load_name = 'ndist'
    config.load_spacing = 3600
    config.load_num_requests = 36000  # only relevant for ndist load
    config.simulation_end = 3600
    config.request_memory = request_memory
    config.request_duration = vm_request_duration

    #for load_name in ['constant', 'sawtooth', 'sinusoid', 'square', 'triangle']:
    for load_name in ['ndist']:
        config.load_name = load_name

        path = 'pareto_optimal_{load}.csv'.format(load=config.load_name)
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(config.get_ident_keys() + ['vms', 'cost'])

            #for altitude in [1, 2, 4, 8, 16, 32, 64]:
            for altitude in [700]:
                config.load_altitude = altitude

                try:
                    results = runner.load_cache()
                    if results is None:
                        results = runner.run()
                        runner.persist(results)

                    for num_vms, simulation in results.simulations.items():
                        writer.writerow(results.config.get_ident_values() + [num_vms, simulation.total_cost])

                    with open('_'.join(config.get_ident_values()) + '.csv', 'w', newline='') as loadfile:
                        loadwriter = csv.writer(loadfile)
                        loadwriter.writerow(['timestamp', 'requests'])
                        for step, request_step in enumerate(results.requests):
                            loadwriter.writerow([step, len(request_step)])
                except Exception as e:
                    logging.error('Execution in run with sigma {sigma} failed: {e}'
                                  .format(sigma=altitude, e=e))


# Execute
if __name__ == "__main__":
    # execute only if run as a script
    main()
