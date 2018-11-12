
class ContentResourceSchema:

    @staticmethod
    def get_request_schema(req_type):
        input_body = {}

        if req_type == "GET":

            input_body = {
                "type": "object",
                "auth_token_required": ['admin', 'user', 'guest'],
                "properties": {
                    "Auth-Token": {
                        "type": "string",
                        "description": "The Session Auth-token"
                    }
                }
            }
        elif req_type == "POST":
            input_body = {
                "type": "object",
                "auth_token_required": ['admin'],
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "title of the content"
                    },
                    "genre": {
                        "type": "array",
                        "description": "The genre of the content"
                    },
                    "director": {
                        "type": "string",
                        "description": "The director of the movie"
                    },
                    "idbm_score": {
                        "type": "string",
                        "description": "The imdb score of the content"
                    },
                    "popularity": {
                        "type": "string",
                        "description": "The popularity of the content"
                    }
                },
                "required": ["title", "genre", "director"]
            }
        elif req_type == "DELETE":
            input_body = {
                "type": "object",
                "auth_token_required": ['admin'],
                "properties": {
                },
            }
        elif req_type == "PUT":
            input_body = {
                "type": "object",
                "auth_token_required": ['admin'],
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "title of the content"
                    },
                    "genre": {
                        "type": "array",
                        "description": "The genre of the content"
                    },
                    "director": {
                        "type": "string",
                        "description": "The director of the movie"
                    },
                    "idbm_score": {
                        "type": "string",
                        "description": "The imdb score of the content"
                    },
                    "popularity": {
                        "type": "string",
                        "description": "The popularity of the comntent"
                    }
                },
            }
        else:
            input_body = None

        return input_body
