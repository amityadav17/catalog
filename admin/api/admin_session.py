import json
from admin.bl.admin_user import Admin
from libservice.base.entity import Entity
from admin.api.admin_session_schema import AdminSessionResourceSchema
from libservice.base.meta_info import MetaResource
from libservice.base.service import ServiceException
from falcon.status_codes import (HTTP_200, HTTP_201)


class AdminSessionResource(object):
    """
    :description:
        Admin session management

    :title:
        Account and Session
    """
    def __init__(self):
        self._token_payload = None
        self.input_body_POST = AdminSessionResourceSchema.get_request_schema("POST")
        MetaResource.get_resource_metadata()
        MetaResource.add_meta_resource(__class__.__name__, "POST", self.input_body_POST)

    def on_post(self, req, resp):
        """
        :description:
            Login to admin session

        :title:
            Login

        :input_body::

            {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The user’s registered account email address"
                    },
                    "password": {
                        "type": "string",
                        "description": "The user’s password"
                    }
                },
                "required": ["email", "password"]
            }

        :output_body::

            {
                "type": "object",
                "properties": {
                    "auth_token": {
                        "type": "string",
                        "description": "The user authentication token"
                    }
                },
                "required": ["auth_token"]
            }

        """

        # Extract the 'body' from the request
        entity = Entity(req.context['body'])

        # Make sure the entity has all required fields
        entity.add_member('login', entity['email'])

        if not entity['login']:
            raise ServiceException('ADMIN_CREATION_EMAIL_FAIL', "Login/Email required.")

        if not entity['password']:
            raise ServiceException('ADMIN_CREATION_PASSWORD_FAIL', "Password Required")

        # Process the request
        auth_token, self._token_payload = Admin.generate_token_from_credential(entity['login'], entity['password'])

        if not auth_token:
            raise ServiceException('ADMIN_USER_INVALID_CREDENTIALS_TOKEN', "Invalid credentials", "Token generation failed")

        # Fill the response
        resp.status = HTTP_200
        resp.body = json.dumps({'auth_token': auth_token})
