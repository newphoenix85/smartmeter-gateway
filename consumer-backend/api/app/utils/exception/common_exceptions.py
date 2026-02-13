from fastapi.exceptions import HTTPException

class RequiresLogin(HTTPException):
    pass

class RequiresDatas(HTTPException):
    pass