
# from libservice.base.context import ContextInfo
from libservice.base.service import ServiceException
from libservice.base.service import find_module_associated_to_uri
from libservice.base.meta_info import MetaResource
from libservice.base.token import Token


class ValidateAuthToken(object):
    """
    This class is a middleware used to intercept all HTTP requests.
    It adds the result to request.context['auth_token'].
    """

    def process_request(self, request, response):
        """
        This method extracts and decodes the API-Key and Auth-Token headers.
        It's called before a request is routed to the proper resource.

        :param request: HTTP request structure
        :param response: HTTP response structure
        :return:
        """
        # ContextInfo.clear_auth_token()

        auth_token = request.get_header('Auth-Token')
        if auth_token is None:
            return

        # Decode the token
        try:
            decoded_token = Token(auth_token)
        except:
            raise ServiceException('INVALID_REQUEST', "Failed to decode 'Auth-Token'.", "Check SSL certificate.",
                                   module=find_module_associated_to_uri(request.path))

        # Make sure it's a Auth-Token
        if not decoded_token.is_type('Auth-Token'):
            raise ServiceException('INVALID_FORMAT', "'Auth-Token' is not valid.", "Not a 'Auth-Token'.",
                                   module=find_module_associated_to_uri(request.path))

        # Validate the format
        if not decoded_token.contains('uuid'):
            raise ServiceException('INVALID_FORMAT', "'Auth-Token' is malformed.", "'uuid' is missing.",
                                   module=find_module_associated_to_uri(request.path))
        if not decoded_token.contains('type'):
            raise ServiceException('INVALID_FORMAT', "'Auth-Token' is malformed.", "'type' is missing.",
                                   module=find_module_associated_to_uri(request.path))

        request.context['auth_token'] = decoded_token

        # ContextInfo.set_auth_token(decoded_token)

    def process_resource(self, request, response, resource, params):
        """
        This method validate that the user is authenticated if required by the entry point.
        """
        # meta_resource = MetaResource.get_meta_resource(resource)
        meta_resource = MetaResource._meta_resource_content['data'][resource.__class__.__name__]
        if meta_resource is not None:
            if request.method in meta_resource:
                method_meta_info = meta_resource[request.method]
                # Check authentication
                if 'auth_token_required' in method_meta_info:
                    user_types = method_meta_info['auth_token_required']
                    # auth_token = ContextInfo.get_context_data('auth_token')
                    auth_token = request.context['auth_token']

                    # Authenticated?
                    if auth_token is None:
                        raise ServiceException('UNAUTHORIZED_NOT_AUTHENTICATED',
                                               module=find_module_associated_to_uri(request.path))

                    # Still valid?
                    if auth_token.is_expired():
                        raise ServiceException('UNAUTHORIZED_SESSION_EXPIRED',
                                               module=find_module_associated_to_uri(request.path))

                    # Has access?
                    if auth_token['type'] not in user_types:
                        raise ServiceException('FORBIDDEN', "User doesn't have access to this resource.",
                                               module=find_module_associated_to_uri(request.path))
