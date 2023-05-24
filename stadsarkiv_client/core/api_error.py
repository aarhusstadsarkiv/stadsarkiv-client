from .openaws import (
    HTTPValidationError,
    ErrorModel,
)
from .translate import translate


class OpenAwsException(Exception):
    def __init__(self, status_code: int, message: str, text: str = ""):
        self.status_code = status_code
        self.message = message
        self.text = text
        super().__init__(message, status_code, text)

    def __str__(self) -> str:
        return self.message


def extract_validation_error(error_dict):
    try:
        error_detail = error_dict['detail']
        if isinstance(error_detail, list) and len(error_detail) > 0:
            first_error = error_detail[0]
            error_type = first_error.get('type')
            return error_type
    except (KeyError, IndexError):
        pass

    return "value_error.unknown_error"


def extract_model_error(error_dict):
    try:
        if isinstance(error_dict.get('detail'), dict):
            error_code = error_dict['detail'].get('code')
        else:
            error_code = error_dict.get('detail')
    except KeyError:
        error_code = "UNKNOWN_MODEL_ERROR"

    return error_code


def get_error_string(error):
    # register errors
    if error == "REGISTER_INVALID_PASSWORD":
        return translate("Password should be at least 8 characters long")
    if error == "REGISTER_USER_ALREADY_EXISTS":
        return translate("User already exists. Try to login instead.")
    if error == "value_error.email":
        return translate("Email needs to be correct.")

    # verify errors
    if error == "VERIFY_USER_BAD_TOKEN":
        return translate("The token is not valid. You will need to a new token to verify your email.")
    if error == "VERIFY_USER_ALREADY_VERIFIED":
        return translate("User is already verified.")

    # login errors
    if error == "LOGIN_BAD_CREDENTIALS":
        return translate("Email or password is not correct.")
    if error == "LOGIN_USER_NOT_VERIFIED":
        return translate("User is not verified. Please verify your email.")

    # reset password errors
    if error == "RESET_PASSWORD_BAD_TOKEN":
        return translate("The token is not valid. You need to request a new mail with a new token.")
    if error == "RESET_PASSWORD_INVALID_PASSWORD":
        return translate("Password should be at least 8 characters long")

    # unknow errors
    if error == "value_error.unknown_error":
        return translate("Unknown error. Please try again later.")
    if error == "UNKNOWN_MODEL_ERROR":
        return translate("Unknown error. Please try again later.")


def validate_response(error):
    raise_message = None
    if isinstance(error, ErrorModel):
        error_message = error.to_dict()
        error_code = extract_model_error(error_message)
        raise_message = get_error_string(error_code)

    if isinstance(error, HTTPValidationError):
        error_message = error.to_dict()
        error_code = extract_validation_error(error_message)
        raise_message = get_error_string(error_code)

    if raise_message:
        raise OpenAwsException(400, raise_message)
