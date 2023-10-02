from rest_framework import status
from rest_framework.response import Response


def error_404(error):
    return Response(
        {
            "Success":False,
            "data":error
        },
        status=status.HTTP_400_BAD_REQUEST
    )
def error_400(error):
    return Response(
        {
            "Success":False,
            "data":error
        },
        status=status.HTTP_400_BAD_REQUEST
    )
def error_422(error):
    return Response(
        {
            "Success":False,
            "data":error
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
def error_429(error):
    return Response(
        {
            "Success":False,
            "data":error
        },
        status=status.HTTP_429_TOO_MANY_REQUESTS
    )
def success_response(data):
    return Response(
        {
            "Success": True,
            "data": data,

        },
    status = status.HTTP_200_OK
    )