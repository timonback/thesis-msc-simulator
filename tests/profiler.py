import atexit
import cProfile
import io
import pstats
from pstats import SortKey

pr = cProfile.Profile()


def profiling_start():
    pr.enable()


def profiling_end():
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.dump_stats('profiler.dmp')


def register_profiling_atexit():
    atexit.register(profiling_end)
