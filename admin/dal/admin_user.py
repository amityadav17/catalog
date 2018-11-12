from datetime import datetime
from libservice.db.db import mycursor, mydb
from libservice.base.entity import Entity


class FacadeAdmin:
    """
    Allow the users management into the database
    """

    # Define the requests for the following function(s)
    REQUEST_INSERT_ADMIN_USER_AUTH = "INSERT INTO admin_auth (uuid, username, password, created_on) " \
                                     "VALUES (%s, %s, %s, NOW());"
    REQUEST_INSERT_ADMIN_USER_INFO = "INSERT INTO admin_info (uuid, firstname, lastname, email, created_on) " \
                                     "VALUES (%s, %s, %s, %s, NOW());"

    @staticmethod
    def add(entity):
        print("In Dal | FacadeAdmin | add method ..." )

        # Make sure all the optional values are initialized
        entity.add_member_if_not_exist('firstname', None)
        entity.add_member_if_not_exist('lastname', None)
        entity.add_member_if_not_exist('created_on', datetime.now())

        # Make sure all pending values are initialized
        entity.replace_all_none_by_empty()

        mycursor.execute(FacadeAdmin.REQUEST_INSERT_ADMIN_USER_AUTH, (entity['uuid'],
                                                                     entity['login'],
                                                                     entity['password'],))
        mycursor.execute(FacadeAdmin.REQUEST_INSERT_ADMIN_USER_INFO, (entity['uuid'],
                                                                     entity['firstname'],
                                                                     entity['lastname'],
                                                                     entity['email'],))
        mydb.commit()

    #########################################################################################################

    # Define the requests for the following function(s)
    REQUEST_EXIST_ADMIN_USER_BY_LOGIN = "SELECT username FROM admin_auth WHERE lower(username) = lower(%s)"

    @staticmethod
    def is_exist_by_login(login):
        """
        Verify is a admin user with the requested login exist in the database

        :param login: The login on which we have to perform the verification [String, Required]
        :return: True if found.
        :return: False if not found.
        """

        mycursor.execute(FacadeAdmin.REQUEST_EXIST_ADMIN_USER_BY_LOGIN, (login,))

        result_set = mycursor.fetchall()
        return result_set

    ####################################################################################################

    # Define the requests for the following function(s)

    REQUEST_GET_ADMIN_USER_BY_LOGIN = """SELECT UA.username, UA.password, UI.*
                                FROM admin_auth AS UA, admin_info AS UI WHERE LOWER(username) = LOWER(%s) 
                                AND UA.uuid = UI.uuid;"""

    @staticmethod
    def get_by_login(login):
        """
        Load the user information for the requested login

        :param login: The login of the user wanted [String, Required]
        :return: None if the user has not been found
        :return: Entity of user values if the user has been found
                    user_id: The uuid of the user [String]
                    password: The password associated to this user [String]
                    email: The email associated to this user [String]
                    firstname: The first name of the user [String]
                    lastname: The last name of the user [String]
        """

        mycursor.execute(FacadeAdmin.REQUEST_GET_ADMIN_USER_BY_LOGIN, (login,))
        result_set = mycursor.fetchall()

        if result_set:
            return Entity({'login': result_set[0][0],
                           'password': result_set[0][1],
                           'uuid': result_set[0][2],
                           'firstname': result_set[0][3],
                           'lastname': result_set[0][4],
                           'email': result_set[0][5]
                           })

        return None
