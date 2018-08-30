import falcon


class AuthMiddleware(object):
    TOKEN = '4e1717c8-c2b0-439e-b375-419e764801fe'

    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        if token is None:
            token = req.get_param('Authorization')

        account_id = req.get_header('Account-ID')
        challenges = ['Token type="Fernet"']

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token, account_id):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

    def _token_is_valid(self, token, account_id):
        return self.TOKEN == token
