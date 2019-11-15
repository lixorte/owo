from voluptuous import Schema, MultipleInvalid
import flask
from loguru import logger
import functools

logger.add("api_utils.log", colorize=True,
           format="<green>{time}</green> <level>{message}</level>", rotation="1 day", backtrace=True, diagnose=True)


def schema_validator(schema: Schema):
    """Checks that combination of query and json content matches the schema"""
    def _validator(f):
        @functools.wraps(f)
        def __validator(*args, **kwargs):
            json_data = flask.request.get_json()
            query_data = flask.request.to_dict()
            to_check = {**json_data, **query_data}
            try:
                schema(to_check)
            except MultipleInvalid:
                logger.warning(f"Dropped invalid request on {f.__name__}")
                return flask.jsonify(
                    {
                        "message": "Invalid schema",
                        "code": 400
                    }
                ), 400
            return f(*args, **kwargs)
        return __validator
    return _validator
