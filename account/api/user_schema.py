
class UserResourceSchema:

    @staticmethod
    def get_request_schema(req_type):
        input_body = {}

        if req_type == "POST":

            input_body = {
                "type": "object",
                "auth_token_required": ['admin'],
                "properties": {
                    "firstname": {
                        "type": "string",
                        "description": "The user’s first name"
                    },
                    "lastname": {
                        "type": "string",
                        "description": "The user’s last name"
                    },
                    "email": {
                        "type": "string",
                        "description": "The user’s account email address"
                    },
                    "password": {
                        "type": "string",
                        "description": "The user’s password"
                    }
                },
                "required": ["email", "password"]
            }
        elif req_type == "GET":
            input_body = {"Body": "GET NOT DEFINED"}
        else:
            input_body = {"Body": "NOT DEFINED"}

        return input_body

