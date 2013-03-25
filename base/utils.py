from request_provider.signals import get_request
import logging


def get_company():
    request = get_request()
    if not request:
        return None

    user = request.user
    company = None
    if not user.is_anonymous():
        company = user.company

    return company


def get_user():
    request = get_request()
    if not request:
        return None
    return request.user

