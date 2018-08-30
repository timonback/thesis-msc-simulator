import logging

import falcon

logger = logging.getLogger(__name__)


class RequireJSON(object):
    def __init__(self, paths=None):
        self.paths = paths

    def process_request(self, req, resp):
        logger.info('Incoming request ' + req.path)

        enforce = False
        if self.paths is None:
            enforce = True
        else:
            for path in self.paths:
                if req.path.startswith(path):
                    enforce = True

        if enforce:
            if not req.client_accepts_json:
                logger.info('Client does not accept an JSON answer for {path}'.format(path=req.path))
                raise falcon.HTTPNotAcceptable(
                    'This API only supports responses encoded as JSON.',
                    href='http://docs.examples.com/api/json')

            if req.method in ('POST', 'PUT'):
                logger.info('For path {method}: {path} only JSON requests are accepted'.format(method=req.method,
                                                                                               path=req.path))
                if 'application/json' not in req.content_type:
                    raise falcon.HTTPUnsupportedMediaType(
                        'This API only supports requests encoded as JSON.',
                        href='http://docs.examples.com/api/json')
