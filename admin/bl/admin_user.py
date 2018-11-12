import uuid as uuid_generator
from passlib.hash import pbkdf2_sha256
from admin.dal.admin_user import FacadeAdmin
from libservice.base.entity import Entity
from libservice.base.service import ServiceException
from libservice.base.token import Token, UserAuthTokenType, auth_token_expiration
from libservice.base.util import check_password, validate_email, datetime_to_string, get_datetime, to_datetime


class Admin:
    """
    Allow user management systems
    """

    @staticmethod
    def create_user(entity):
        """
        Create a new admin user

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
            is_user_exists = FacadeAdmin.is_exist_by_login(entity['login'])
        except Exception as e:
            raise ServiceException('ADMIN_USER_DATABASE_QUERY_FAIL', "Fail to verify if the user already exist.", str(e))

        if is_user_exists:
            raise ServiceException('ADMIN_USER_ALREADY_EXIST_FAIL', "User already exists in the database.")

        # Validate email address
        if not validate_email(entity['login']):
            raise ServiceException('ADMIN_USER_CREATION_EMAIL_FAIL', "Email doesn't meet requirements.")

        # Validate the password
        if not check_password(entity['password']):
            raise ServiceException('ADMIN_USER_CREATION_PASSWORD_FAIL', "Password doesn't meet requirements.")

        entity['uuid'] = str(uuid_generator.uuid1())
        # Hash the user password
        try:
            entity['password'] = pbkdf2_sha256.encrypt(entity['password'], rounds=2000, salt_size=16)
        except:
            raise ServiceException('ADMIN_USER_ENCRYPTION_FAIL', "The encryption of the password has failed.")

        # Create a new user using the dal
        try:
            FacadeAdmin.add(entity)
        except Exception as e:
            raise ServiceException('ADMIN_USER_DATABASE_QUERY_FAIL', "The creation of the user has failed.", str(e))

    ####################################################################################################

    @staticmethod
    def get_user_from_login(login):
        """
        Get the admin user information

        :param login: The login of the admin user [String, Required]
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
            if not FacadeAdmin.is_exist_by_login(login):
                return None
            return FacadeAdmin.get_by_login(login)
        except Exception as e:
            raise ServiceException('USER_DATABASE_QUERY_FAIL', "Unable to load the user information.", str(e))

    ####################################################################################################

    @staticmethod
    def generate_token_from_credential(login, password):
        """
        Verify the authentication information of a admin user

        :param login: The login associated to this user [String, Required]
        :param password: The password associated to this user [String, Required]

        :return: An authentication token if credential are valid
        """

        if not login and not password:
            raise ServiceException('ADMIN_USER_DATABASE_QUERY_FAIL', "Fail to load the user current information.", str(e))

        try:
            user = FacadeAdmin.get_by_login(login)
        except Exception as e:
            raise ServiceException('ADMIN_USER_LOAD_QUERY_FAIL', "Fail to load the user current information.", str(e))

        if user is None:
            raise ServiceException('ADMIN_USER_UNKNOWN_CREDENTIALS', "Invalid credentials", "Unknown user")

        # If the password is valid, generate the authentication token
        if not pbkdf2_sha256.verify(password, user['password']):
            raise ServiceException('ADMIN_USER_INVALID_PASSWORD_CREDENTIALS', "Invalid credentials", "Invalid password")

        try:
            # Build the json payload
            payload = dict()

            payload['uuid'] = user['uuid']
            payload['type'] = UserAuthTokenType.AUTH_TYPE_ADMIN

            # Generate the token
            return Token.generate_token('Auth-Token', payload, auth_token_expiration), payload

        except Exception as e:
            raise ServiceException('ADMIN_USER_INVALID_CREDENTIALS', "Invalid credentials", str(e))

