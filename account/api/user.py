import json
from falcon.status_codes import (HTTP_200, HTTP_201)
from account.bl.user import User
from libservice.base.entity import Entity
from account.api.user_schema import UserResourceSchema
from libservice.base.meta_info import MetaResource
from libservice.base.service import ServiceException


class UserResource(UserResourceSchema):

    """
    :description:
        User account management

    :title:
        Account and Session
    """

    def __init__(self):
        self.input_body_GET = UserResourceSchema.get_request_schema("GET")
        self.input_body_POST = UserResourceSchema.get_request_schema("POST")
        self.input_body_PUT = UserResourceSchema.get_request_schema("PUT")
        MetaResource.add_meta_resource(__class__.__name__, "GET", self.input_body_GET)
        MetaResource.add_meta_resource(__class__.__name__, "POST", self.input_body_POST)
        MetaResource.add_meta_resource(__class__.__name__, "PUT", self.input_body_PUT)

    def on_post(self, req, resp):
        """
        :description:
            Create user account

        :title:
            Create user account

        :input_body::

            {
                "type": "object",
                "properties": {
                    "firstname": {
                        "type": "string",
                        "description": "The user’s first name"
                    },
                    "lastname": {
                        "type": "string",
                        "description": "he user’s last name"
                    },
                    "email": {
                        "type": "string",
                        "description": "he user’s account email address"
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
                    "firstname": {
                        "type": "string",
                        "description": "The user’s first name"
                    },
                    "lastname": {
                        "type": "string",
                        "description": "he user’s last name"
                    },
                    "email": {
                        "type": "string",
                        "description": "he user’s account email address"
                    }
                },
                "required": ["firstname", "lastname", "email"]
            }

        """

        # Extract the 'body' from the request
        entity = Entity(req.context['body'])

        # Make sure the entity has all required fields
        entity.add_member('login', entity['email'])

        # Process the request
        User.create_user(entity)

        # Retrieve the new user information
        user_info = User.get_user_from_login(entity.get('login'))

        if not user_info:
            raise ServiceException('USER_CREATION_FAIL',
                                   "Unable to load the user information that has just been created.")


        # Remove the unnecessary fields from the entity
        user_info.remove_member('uuid')
        user_info.remove_member('email')
        user_info.remove_member('password')

        # Fill the response
        resp.status = HTTP_201
        resp.body = json.dumps(user_info)

    #todo Fectch user information
    # def on_get(self, req, resp):
    #     print("In Userresource | GET ..")
    #
    #     User.create_user()
    #
    #     user_info = {
    #         "Success": "In GET "
    #     }
    #
    #     # Fill the response
    #     resp.status = HTTP_200
    #     resp.body = json.dumps(user_info)
    #
    #todo Update user information
    # def on_put(self, req, resp):
    #     print("In UserResource | PUT ..")
    #
    #     user_info = {
    #         "Success": "In PUT "
    #     }
    #
    #     # Fill the response
    #     resp.status = HTTP_201
    #     resp.body = json.dumps(user_info)
