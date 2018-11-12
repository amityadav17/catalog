import json
from falcon.status_codes import (HTTP_200, HTTP_201)
from admin.bl.admin_user import Admin
from libservice.base.entity import Entity
from admin.api.admin_schema import AdminResourceSchema
from libservice.base.meta_info import MetaResource
from libservice.base.service import ServiceException


class AdminResource(object):

    """
    :description:
        Admin account management

    :title:
        Admin Account and Session
    """

    def __init__(self):
        self.input_body_GET = AdminResourceSchema.get_request_schema("GET")
        self.input_body_POST = AdminResourceSchema.get_request_schema("POST")
        self.input_body_PUT = AdminResourceSchema.get_request_schema("PUT")
        MetaResource.get_resource_metadata()
        MetaResource.add_meta_resource(__class__.__name__, "GET", self.input_body_GET)
        MetaResource.add_meta_resource(__class__.__name__, "POST", self.input_body_POST)
        MetaResource.add_meta_resource(__class__.__name__, "PUT", self.input_body_PUT)
        # MetaResource.get_resource_metadata()

    def on_post(self, req, resp):
        """
        :description:
            Create admin user account

        :title:
            Create admin user account

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

        if not entity['login']:
            raise ServiceException('ADMIN_CREATION_EMAIL_FAIL', "Login/Email required.")

        if not entity['password']:
            raise ServiceException('ADMIN_CREATION_PASSWORD_FAIL', "Password Required")

        # Process the request
        Admin.create_user(entity)

        # Retrieve the new user information
        user_info = Admin.get_user_from_login(entity.get('login'))

        if not user_info:
            raise ServiceException('ADMIN_USER_LOAD_FAIL',
                                   "Unable to load the user information that has just been created.")


        # Remove the unnecessary fields from the entity
        user_info.remove_member('uuid')
        user_info.remove_member('email')
        user_info.remove_member('password')

        # Fill the response
        resp.status = HTTP_201
        resp.body = json.dumps(user_info)

    #todo Fetch Admin account information
    # def on_get(self, req, resp):
    #     print("In AdminResource | GET ..")
    #
    #     Admin.create_user()
    #
    #     user_info = {
    #         "Success": "In GET "
    #     }
    #
    #     # Fill the response
    #     resp.status = HTTP_200
    #     resp.body = json.dumps(user_info)
    #
    #todo Update Admin account information
    # def on_put(self, req, resp):
    #     print("In AdminResource | PUT ..")
    #
    #     user_info = {
    #         "Success": "In PUT "
    #     }
    #
    #     # Fill the response
    #     resp.status = HTTP_201
    #     resp.body = json.dumps(user_info)
