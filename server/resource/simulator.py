import json
import logging

import falcon

from server.component.simulator import SimulatorComponent
from server.util.request_parser import RequestParser
from simulator.configuration import Configuration
from util.json_encoder import JsonEncoder

logger = logging.getLogger(__name__)


class SimulatorResource(object):
    PATH = '/simulator'

    def __init__(self):
        self.config = Configuration()
        self.simulator = SimulatorComponent(self.config)

    def on_get(self, req, resp):
        self.config.load_name = RequestParser.get_or_default(req, 'load', 'ndist')
        self.config.load_altitude = int(
            RequestParser.get_or_default(req, 'altitude', self.config.load_altitude))  # sigma
        self.config.load_spacing = int(RequestParser.get_or_default(req, 'spacing', self.config.load_spacing))
        self.config.request_duration = float(
            RequestParser.get_or_default(req, 'duration', self.config.request_duration))
        self.config.request_memory = int(RequestParser.get_or_default(req, 'memory', self.config.request_memory))
        self.config.simulation_end = int(RequestParser.get_or_default(req, 'test_duration', self.config.simulation_end))
        # Additional for ndist
        self.config.load_num_spikes = int(RequestParser.get_or_default(req, 'num_spikes', 1))
        self.config.load_num_requests = int(
            RequestParser.get_or_default(req, 'num_requests', self.config.load_num_requests))
        if self.config.load_name != 'ndist':
            self.config.load_num_spikes = 1
            self.config.load_num_requests = 0

        results = self.simulator.get_or_calc()

        logger.info('Sending result...')
        resp.body = json.dumps(results, ensure_ascii=False, cls=JsonEncoder)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200
