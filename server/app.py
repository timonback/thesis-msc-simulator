import logging
import os

import falcon

from util.logger import setup_logging
from .middleware.require_json import RequireJSON
from .resource.simulator import SimulatorResource

logger = logging.getLogger(__name__)


def create_app():
    setup_logging('server.log')

    api_path = '/api'

    app = falcon.API(
        middleware=[
            # AuthMiddleware(),
            RequireJSON([api_path]),
        ]
    )

    simulator = SimulatorResource()
    app.add_route(api_path + simulator.PATH, simulator)

    app.add_static_route('/', os.path.dirname(os.path.abspath(__file__)) + '/public/')
    app.add_static_route('/simulations', os.path.abspath('archive/'))

    return app


def get_app():
    return create_app()
