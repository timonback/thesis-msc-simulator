class RequestParser:
    @staticmethod
    def get_or_default(req, key, default_value):
        if req is not None and req.params is not None:
            if key in req.params:
                return req.params[key]
        return default_value
