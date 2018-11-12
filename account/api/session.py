import json
from account.bl.user import User
from libservice.base.entity import Entity
from account.api.session_schema import SessionResourceSchema
from libservice.base.meta_info import MetaResource
from libservice.base.service import ServiceException
from falcon.status_codes import (HTTP_200, HTTP_201)


class SessionResource(object):
    """
    :description:
        User session management

    :title:
        Account and Session
    """
    def __init__(self):
        self._token_payload = None
        self.input_body_POST = SessionResourceSchema.get_request_schema("POST")
        MetaResource.add_meta_resource(__class__.__name__, "POST", self.input_body_POST)

    def on_post(self, req, resp):
        """
        :description:
            Login to user session

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

        if entity['email'] == "":
            i = 0
        else:
            i = 0

        # Process the request
        auth_token, self._token_payload = User.generate_token_from_credential(entity['login'], entity['password'])

        if not auth_token:
            raise ServiceException('USER_INVALID_CREDENTIALS_TOKEN', "Invalid credentials", "Token generation failed")

        # Fill the response
        resp.status = HTTP_200
        resp.body = json.dumps({'auth_token': auth_token})
