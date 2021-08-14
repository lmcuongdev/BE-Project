from constants import StatusCode


class Error(Exception):
    default_error_message = None
    status_code = None

    def __init__(self, message=None):
        self.error_message = message or self.default_error_message
        super().__init__(self.error_message)

    def get_response(self):
        return {'error_message': self.error_message}, self.status_code


class BadRequestError(Error):
    default_error_message = 'Bad request.'
    status_code = StatusCode.BAD_REQUEST


class SchemaValidationError(BadRequestError):
    default_error_message = 'Bad request input.'

    def __init__(self, error_messages, message=None):
        super().__init__(message)
        self.error_data = {
            field: error_messages[field][0] for field in error_messages
        }

    def get_response(self):
        response = super().get_response()
        response[0].update({'error_data': self.error_data})
        return response


class IncorrectCredentialError(Error):
    default_error_message = 'Incorrect username or password.'
    status_code = StatusCode.UNAUTHORIZED


class UnauthorizedError(Error):
    default_error_message = 'Unauthorized.'
    status_code = StatusCode.UNAUTHORIZED


class InvalidTokenError(UnauthorizedError):
    default_error_message = 'Invalid access token.'


class PermissionDeniedError(Error):
    default_error_message = 'Permission denied.'
    status_code = StatusCode.FORBIDDEN


class NotFoundError(Error):
    default_error_message = 'Not found.'
    status_code = StatusCode.NOT_FOUND


class InternalServerError(Error):
    default_error_message = 'Internal server error.'
    status_code = StatusCode.INTERNAL_SERVER_ERROR
