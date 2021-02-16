# -*- coding: utf-8 -*-

import time


class Decorators:

    limiter_start = None
    limiter_last = None
    limiter_counter = 0

    # All endpoints within the /api path must be called with a valid token
    @staticmethod
    def ensure_token(decorated):
        def wrapper(api, *args, **kwargs):
            if not api.token or time.time() > api.token.get('token_expiration', 0):
                api.token = api.get_access_token()
            return decorated(api, *args, **kwargs)

        return wrapper

    @staticmethod
    def limit_request(per_hour, per_day):
        def decorator(function):
            def wrapper(api, *args, **kwargs):
                now = time.time()
                if not Decorators.limiter_start:
                    Decorators.limiter_start = now

                if Decorators.limiter_counter > per_hour and (now - Decorators.limiter_start <= 3600):
                    sleep = 3600 - (now - Decorators.limiter_start)
                    print('Wait %d seconds..' % sleep)
                    time.sleep(sleep)
                    Decorators.limiter_counter = 0
                    Decorators.limiter_start = None

                    # TODO: limit per day

                Decorators.limiter_last = now
                result = function(api, *args, **kwargs)
                Decorators.limiter_counter += 1
                return result

            return wrapper
        return decorator