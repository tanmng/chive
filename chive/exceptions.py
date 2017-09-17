class CoinHiveError(Exception):
    def __init__(self, message=None, errors=None):
        if errors:
            message = ', '.join(errors)

        self.errors = errors

        super(CoinHiveError, self).__init__(message)

class InvalidRequest(CoinHiveError):
    pass

class Unauthorized(CoinHiveError):
    pass

class Forbidden(CoinHiveError):
    pass

class InvalidPath(CoinHiveError):
    pass

class RateLimitExceeded(CoinHiveError):
    pass

class InternalServerError(CoinHiveError):
    pass

class CoinHiveNotInitialized(CoinHiveError):
    pass

class CoinHiveDown(CoinHiveError):
    pass

class UnexpectedError(CoinHiveError):
    pass
