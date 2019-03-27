import http
from flask import Flask, request, g

class OpticDocumentingMiddleware(object):
    def __init__(self, app):
        self.app = app
        request_logger = http.client.HTTPConnection('localhost', 30334)
        response_logger = http.client.HTTPConnection('localhost', 30335)

        @app.after_request
        def after(response):
            # Log Request
            request_body = request.data if request.content_length > 0 else None
            request_headers = {k: v for k, v in request.headers.items()}
            path = request.path + "?" + str(request.query_string, 'utf-8')
            request_logger.request(request.method, path, request_body, request_headers)
            logger_response = request_logger.getresponse()
            interactionId = logger_response.read(logger_response.length).decode("utf-8")

            # Log Response
            response_body = response.data if response.content_length > 0 else None
            response_headers = {k: v for k, v in response.headers.items()}
            response_logger_path = "/interactions/" + interactionId + "/status/" + str(response.status_code)
            response_logger.request("POST", response_logger_path, response_body, response_headers)
            response_logger_response = response_logger.getresponse()

            return response
