from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    code = 403
    message = 'no message'

class InputError(HTTPException):
    code = 400
    message = 'no message'

class DatabaseError(HTTPException):
    code = 500
    message = 'no message'

class UnauthorizedError(HTTPException):
    code = 401
    message = 'no message'
