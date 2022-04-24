from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def validatorV1(request_type="default", validator=None, path_validator=None):
    def inner_validator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[-1]
            if path_validator:
                path_serializer = path_validator(data=kwargs)
                if not path_serializer.is_valid():
                    return Response(path_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                path_serializer = None
            if not validator and not path_validator:
                print(
                    "Validator Decorator return - 400 - validator not sent to funtion")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if request_type == "query_string":
                serializer = validator(data=request.GET)
            elif request_type == "body":
                serializer = validator(data=request.data)
            else:
                serializer = None

            if serializer:
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            res = func(*args, **kwargs, serializer=serializer,
                       path_serializer=path_serializer)
            return res
        return wrapper
    return inner_validator
