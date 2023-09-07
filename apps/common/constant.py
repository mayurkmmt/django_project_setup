class ErrorMsg:
    INVALID_EMAIL = "Email is not valid"
    USER_NOT_FOUND = "Sorry, User not found."
    NOT_ACTIVATE_ACCOUNT = (
        "Your account is not active please contact admin for more details."
    )
    ACCOUNT_NOT_VERIFIED = (
        "Your account is not verified, please verify your account before login."
    )
    INVALID_CREDENTIALS = "Unable to log in with provided credentials."
    COMPANY_NOT_FOUND = "Sorry, company not found"
    COMPANY_REQUIRED_ERROR = "Please enter company"
    EMAIL_VERIFICATION_FAILED = "This verification link is not validated or has expired. Please resend a verification link."


class SystemMsg:
    # user messages
    LOGIN_SUCCESS = "Login successfully"
    COMPANY_CREATED_SUCCESS = "Company registered successfully, Please verify link send to your registered email address"
    EMAIL_VERIFIED_SUCCESS = "Your email has been successfully verified."
