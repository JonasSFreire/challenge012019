from app.api.resources import api_bp
from app.errors import error_response


@api_bp.app_errorhandler(400)
def invalid_service(error):
    return error_response(400)


@api_bp.app_errorhandler(401)
def not_authorized(error):
    return error_response(401)


@api_bp.app_errorhandler(403)
def forbidden(error):
    return error_response(403)


@api_bp.app_errorhandler(404)
def not_found(error):
    return error_response(404)


@api_bp.app_errorhandler(500)
def server_error(error):
    return error_response(500)