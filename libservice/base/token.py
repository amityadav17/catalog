
import time
import jwt

secret_key = "a random, long, sequence of characters that only the server knows"
auth_token_expiration = 86400


class Token:
    """
    Parse and generate JSON Web Tokens.

    Format::

    { "type": string, "data": object, "expiry": number }

    """

    def __init__(self, token):
        # Decode the token
        self.decoded = jwt.decode(token, secret_key, algorithms=['HS256'])

        # Check the format
        if 'data' not in self.decoded or 'type' not in self.decoded or 'expiry' not in self.decoded:
            raise Exception("Token is not compatible.")

    def __getitem__(self, name):
        """
        Get the data embedded in the JSON Web token.

        :param name: Attribute to get
        :return: JSON object
        """
        return self.decoded['data'][name]

    def contains(self, name):
        """
        Check if the data contains a specific attribute.

        :param name: Attribute to check
        :return: True/False
        """
        return name in self.decoded['data']

    def is_type(self, type):
        """
        Validate the JSON Web token type.

        :param type: Token type
        :return: True/False
        """
        return type == self.decoded['type']

    def is_expired(self):
        """
        Check if the JSON Web token is expired or not.

        :return: True/False
        """
        if self.decoded['expiry'] == 0:
            return False

        return time.time() > self.decoded['expiry']

    def get(self, key, default=None):
        # make token behave like dictionary
        if key in self.decoded['data']:
            return self.decoded['data'][key]
        else:
            return default

    @staticmethod
    def generate_token(type, data, expiry=0):
        """
        Generate a JSON Web token.

        :param type: Token type
        :param data: Data to be embedded in the token
        :param expiry: Expiry in second
        :return:
        """
        payload = {
            'type': type,
            'data': data,
            'expiry': time.time() + expiry if expiry > 0 else 0
        }

        encoded = jwt.encode(payload, secret_key, algorithm='HS256')
        return encoded.decode('utf-8')


class UserAuthTokenType:
    AUTH_TYPE_USER = 'user'
    AUTH_TYPE_GUEST = 'guest'
    AUTH_TYPE_ADMIN = 'admin'
