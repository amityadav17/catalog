import uuid as uuid_generator
from passlib.hash import pbkdf2_sha256
from account.dal.user import FacadeUser
from libservice.base.entity import Entity
from libservice.base.service import ServiceException
from libservice.base.token import Token, UserAuthTokenType, auth_token_expiration
from libservice.base.util import check_password, validate_email, datetime_to_string, get_datetime, to_datetime


class User:
    """
    Allow user management systems
    """

    @staticmethod
    def create_user(entity):
        """
        Create a new user

        :param entity: A Entity object with required values
                    email: The email associated to this user [String, Required]
                    password: The password associated to this user [String, Required]
                    email: The email associated to this user [String, Required]
                    firstname: The first name of the user [String, Required]
                    lastname: The last name of the user [String, Required]
        :return:
        """

        print("In bl | User | create User method")

        # Make sure the user does not already exist
        try:
            is_user_exists = FacadeUser.is_exist_by_login(entity['login'])
        except Exception as e:
            raise ServiceException('USER_DATABASE_QUERY_FAIL', "Fail to verify if the user already exist.", str(e))

        if is_user_exists:
            raise ServiceException('USER_ALREADY_EXIST_FAIL', "User already exists in the database.")

        # Validate email address
        if not validate_email(entity['login']):
            raise ServiceException('USER_CREATION_EMAIL_FAIL', "Email doesn't meet requirements.")

        # Validate the password
        if not check_password(entity['password']):
            raise ServiceException('USER_CREATION_PASSWORD_FAIL', "Password doesn't meet requirements.")

        entity['uuid'] = str(uuid_generator.uuid1())
        # Hash the user password
        try:
            entity['password'] = pbkdf2_sha256.encrypt(entity['password'], rounds=2000, salt_size=16)
        except:
            raise ServiceException('USER_CREATION_ENCRYPTION_FAIL', "The encryption of the password has failed.")

        # Create a new user using the dal
        try:
            FacadeUser.add(entity)
        except Exception as e:
            raise ServiceException('USER_DATABASE_CREATION_QUERY_FAIL', "The creation of the user has failed.", str(e))

        # FacadeUser.add(entity)
        # pass

    ####################################################################################################

    @staticmethod
    def get_user_from_login(login):
        """
        Get the user information

        :param login: The login of the user [String, Required]
        :return: If not user found, return None
        :return: If user found, return a Entity with the user information
                    user_id: The uuid associated to this user [String]
                    email: The email associated to this user [String]
                    password: The password associated to this user [String]
                    email: The email associated to this user [String]
                    firstname: The first name of the user [String]
                    lastname: The last name of the user [String]
        """
        try:
            # Make sure the user exist
            if not FacadeUser.is_exist_by_login(login):
                return None
            return FacadeUser.get_by_login(login)
        except Exception as e:
            raise ServiceException('USER_DATABASE_QUERY_FAIL', "Unable to load the user information.", str(e))

    ####################################################################################################

    @staticmethod
    def generate_token_from_credential(login, password):
        """
        Verify the authentication information of a user

        :param login: The login associated to this user [String, Required]
        :param password: The password associated to this user [String, Required]

        :return: An authentication token if credential are valid
        """

        # Identify guest login
        is_guest = False

        if not login and not password:
            is_guest = True

        # Try to retrieve the user information
        user = None

        if not is_guest:
            try:
                user = FacadeUser.get_by_login(login)
            except Exception as e:
                raise ServiceException('USER_DATABASE_QUERY_FAIL', "Fail to load the user current information.", str(e))

            if user is None:
                raise ServiceException('USER_UNKNOWN_INVALID_CREDENTIALS', "Invalid credentials", "Unknown user")

        # If the password is valid, generate the authentication token
        if not is_guest and not pbkdf2_sha256.verify(password, user['password']):
            raise ServiceException('USER_INVALID_PASSWORD_CREDENTIALS', "Invalid credentials", "Invalid password")

        try:
            # Build the json payload
            payload = dict()

            if is_guest:
                payload['uuid'] = str(uuid_generator.uuid1())
                payload['type'] = UserAuthTokenType.AUTH_TYPE_GUEST
            else:
                payload['uuid'] = user['uuid']
                payload['type'] = UserAuthTokenType.AUTH_TYPE_USER

            # Generate the token
            return Token.generate_token('Auth-Token', payload, auth_token_expiration), payload

        except Exception as e:
            raise ServiceException('USER_INVALID_CREDENTIALS', "Invalid credentials", str(e))

