class ApiAuth:

    def authenticated(method):
        def decorated(*args, **kwargs):
            if check_authenticated(kwargs['user']):
                return method(*args, **kwargs)
            else:
                raise Exception

        return decorated