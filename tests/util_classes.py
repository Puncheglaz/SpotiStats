"""Module for tests util classes."""


class ResponseObject:
    """Class representing a response object
     from http-request with json data."""
    def __init__(self, json_line, status_code):
        self.json_line = json_line
        self.status_code = status_code

    def json(self):
        """Function returns json_line."""
        return self.json_line
