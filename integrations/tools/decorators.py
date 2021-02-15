# -*- coding: utf-8 -*-

import time


class Decorators:

    # All endpoints within the /api path must be called with a valid token
    @staticmethod
    def ensure_token(decorated):
        def wrapper(api, *args, **kwargs):
            if not api.token or time.time() > api.token.get('token_expiration', 0):
                api.get_access_token()
            return decorated(api, *args, **kwargs)

        return wrapper
