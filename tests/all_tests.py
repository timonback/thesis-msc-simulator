# start coverage early to include also the package imports
# Comment out the coverage_start() line to enable debugging
from tests.coverage import coverage_start
from tests.profiler import profiling_start, register_profiling_atexit

coverage_start()

profiling_start()
register_profiling_atexit()

from .suite import create_suite


###
# Run the test and create a coverage report
###

def suite():
    return create_suite()
