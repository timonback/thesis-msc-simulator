import atexit

import coverage

cov = coverage.Coverage(omit=['virtualenv/*'], branch=True)
cov.exclude('pragma: no cover')
cov.exclude('return str(self.__dict__)')
cov.exclude('raise NotImplementedError')
cov.exclude('pass')
cov.exclude('if __name__ == .__main__.:')


def coverage_start():
    cov.start()


def coverage_stop():
    cov.stop()
    cov.save()
    cov.html_report()


atexit.register(coverage_stop)
