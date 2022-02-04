from flask import Flask, request
from flask_cors import CORS

from database.backend_database import set_users, validate_user, update_user

# flask_cors is to handle the CORS issue in the API for web
backend_app = Flask(__name__, template_folder='templates')
CORS(backend_app)


@backend_app.route('/')
def root_page():
    return {"description": "Welcome to base API"}


@backend_app.route('/register', methods=['POST'])
def register_user():
    """
    The request body must be a of {
                                    "username": "string",
                                    "mail_id" : "string",
                                    "password": "string"
                                 }
    :return:
    """
    if request.method == 'POST':
        payloads = request.json
        if ("username" not in payloads) or ("password" not in payloads) or ("mail_id" not in payloads):
            return {"status": "Registration failed", "description": "Missing one or more input payloads"}
        set_users(payloads)
        return {"status": "Registration Success", "description": "User is successfully registered"}

    else:
        return {"status": "Registration failed", "description": "Incorrect Request method"}


@backend_app.route('/login', methods=['POST'])
def login_user():
    """
    The request body must be a of {
                                    "mail_id" : "string",
                                    "password": "string"
                                 }
    :return:
    """
    if request.method == 'POST':
        payloads = request.json
        if ("password" not in payloads) or ("mail_id" not in payloads):
            return {"status": "Login failed", "description": "Missing one or more input payloads"}
        result = validate_user(payloads)
        if result:
            return {"status": "Login Success", "description": "User is successfully Logged In"}

        return {"status": "Login Failed", "description": "Given credential not matched"}

    else:
        return {"status": "Login failed", "description": "Incorrect Request method"}


@backend_app.route('/update_password', methods=['PUT'])
def update_password():
    """
    The request body must be a of {
                                    "mail_id" : "string",
                                    "new_password": "string"
                                 }
    :return:
    """
    if request.method == 'PUT':
        payloads = request.json
        if ("new_password" not in payloads) or ("mail_id" not in payloads):
            return {"status": "Password reset failed", "description": "Missing one or more input payloads"}
        result = update_user(payloads)
        if result:
            return {"status": "Password reset Success", "description": "Password reset successfully"}

        return {"status": "Password reset Failed", "description": "Given input not matched"}

    else:
        return {"status": "Password reset failed", "description": "Incorrect Request method"}

