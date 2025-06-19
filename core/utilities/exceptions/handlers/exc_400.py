# import fastapi
# from fastapi import Request, status
# from fastapi.responses import RedirectResponse
# from fastapi.exceptions import RequestValidationError
# from fastapi import FastAPI, HTTPException
#
# from core.utilities.exceptions.api import app
#
#
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     if exc.status_code == 401:
#         response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
#
#         response.delete_cookie("access_token")
#         response.delete_cookie("is_login")
#         return response
#
#     from fastapi.exception_handlers import http_exception_handler
#     return await http_exception_handler(request, exc)
