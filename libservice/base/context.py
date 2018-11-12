import threading

from libservice.base.util import deep_get


def initialize(func):
    def wrapped(*args, **kwargs):
        if hasattr(ContextInfo.context_info, 'data') is False:
            ContextInfo.context_info.data = {}
        return func(*args, **kwargs)

    return wrapped


class ContextInfo:
    """
    Interface to store/retrieve the current thread context data
    """

    # Define a thread isolated variable
    context_info = threading.local()

    @staticmethod
    @initialize
    def get_context_data(key):
        """
        Get some context data

        :param key: The key of the desired context data
        :return: The stored context data
        """

        if key in ContextInfo.context_info.data:
            return ContextInfo.context_info.data[key]

        return None

    ####################################################################################################

    @staticmethod
    @initialize
    def set_context_data(key, data):
        """
        Set some context data

        :param key: The key of the desired context data
        :param data: The stored context data
        :return:
        """

        ContextInfo.context_info.data[key] = data

    ####################################################################################################

    @staticmethod
    @initialize
    def remove_context_data(key):
        """
        Remove some context data

        :param key: The key of the desired context data
        :return:
        """

        if key in ContextInfo.context_info.data:
            ContextInfo.context_info.data.pop(key)

    ####################################################################################################

    @staticmethod
    @initialize
    def set_auth_token(auth_token):
        """
        Set host information in the context data

        :param host: The host information dictionnary
        :return:
        """

        ContextInfo.context_info.data['auth_token'] = auth_token

    ####################################################################################################

    @staticmethod
    @initialize
    def clear_auth_token():
        """
        Clear host information from context data

        :return:
        """

        ContextInfo.remove_context_data('auth_token')

    ####################################################################################################

    @staticmethod
    @initialize
    def get_type():
        """
        Get the type from the context data

        :return: The type
        """

        if 'auth_token' in ContextInfo.context_info.data:
            return deep_get(ContextInfo.context_info.data['auth_token'], 'type')

    ####################################################################################################

    @staticmethod
    @initialize
    def get_uuid():
        """
        Get the user uuid from the context data

        :return: The user uuid
        """

        if 'auth_token' in ContextInfo.context_info.data:
            return deep_get(ContextInfo.context_info.data['auth_token'], 'uuid')

