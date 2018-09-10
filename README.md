# Cloud Load Simulator
[![CircleCI](https://circleci.com/gh/timonback/thesis-msc-simulator.svg?style=svg&circle-token=9c777812c1ea59fd70f1eb8092675cfa4657c088)](https://circleci.com/gh/timonback/thesis-msc-simulator)

It simulates various loads towards a cloud environment.
Based on the configuration, the cost for handling all requests is calculated.
In many cases (depending on the load characteristics), the cost can be reduced by moving certain requests to FaaS 
(Function as a Service).

This is a Python 3 project that requires the dependencies to be install via `python3 setup.py install` 
(virtualenv is recommended in general).

All of the configuration is done in the `simulator/configuration.py` file.

## Standalone

Run `python3 main.py`

## Server

Run `python3 serve.py`

Then open `http://localhost:8888/index.html`

![Screenshot](../master/README_screenshot.png?raw=true)

## Tests

Run the tests `python3 setup.py test`. A coverage report is generated in `./htmlcov`.

## Profiling

Run the tests `python3 setup.py test` to profile.
Convert the profiling file (`profiler.dmp`) into a readable file with `python3 util/analyze_dmp.py profiler.dmp 
profiler.log`.
