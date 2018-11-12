import falcon
import json
import jsonschema
from libservice.base.meta_info import MetaResource
from libservice.base.token import Token
from libservice.base.context import ContextInfo


def extract_json_request_body(req):
    """
    Read the body data stream inside http request, transform it to UTF-8 and cache it bace inside input request.
    If the stream is already cached, function returns it.
    This function allows multiple read of the same stream (not allowed by direct call to req.stream.read()).

    :param req: Http Request object
    :return: The request body in utf-8.  If not stream is found in req, return None if no body.
    """
    if 'stream_utf8' not in req.context:
        req.context['stream_utf8'] = '{}'
        if req.content_type in ('application/json', 'application/json; charset=UTF-8'):
            if req.content_length not in (None, 0):
                stream = req.stream.read()
                req.context['stream_utf8'] = stream.decode('utf-8')

    return req.context['stream_utf8']


class API(falcon.API):
    def __init__(self, *args, **kwargs):
        # Initialize falcon
        super().__init__(*args, **kwargs)


class ServiceException(Exception):
    def __init__(self, error_id, message=None, detail=None, custom_data=None, module=None):

        # http code no longer found at raise time
        # Matching is performed in service_exception_handler() function.
        self.error_id = error_id
        self.message = message
        self.detail = detail
        self.custom_data = custom_data
        self.module = module


def service_exception_handler(ex, req, resp, params):
    """
    This static method is called by falcon framework when ServiceException reach it
    """
    error = {
        "http_code":"400 Invalid Request",
        "error_title":"INVALID - REQUEST",
        "error_message":"INVALID REQUEST",
        "service_code": "400"
    }
    raise falcon.HTTPError(error['http_code'], ex.error_id, ex.message, None, None, None, error['service_code'])


def base_exception_handler(ex, req, resp, params):
    """
    This function is called when Exception isn't a ServiceException, so when error 500 is returned.

    :param ex: Exception thrown
    :param req: Request where the exception was thrown
    """

    raise falcon.HTTPError("500 Internal Error", "Internal ERR", None, None, None, None, "1")


class Validate(object):

    def process_request(self,req,resp):

        try:
            req.context['body'] = json.loads(extract_json_request_body(req))
            print(req.context['body'])
        except (ValueError, UnicodeDecodeError) as ex:
            raise ServiceException('INVALID_FORMAT', "Malformed JSON detected.", str(ex),
                                   module=find_module_associated_to_uri(req.path))
        except Exception as ex:
            raise ServiceException('INVALID_FORMAT', "Cannot decode the request body.", str(ex),
                                   module=find_module_associated_to_uri(req.path))

    def process_resource(self,req,resp,resource,params):

        schema = MetaResource._meta_resource_content['data'][resource.__class__.__name__][req.method]

        try:
            jsonschema.validate(req.context['body'], schema)
        except jsonschema.ValidationError as ex:
            str_path = ''
            for i, node in enumerate(ex.schema_path):
                if i != 0:
                    str_path = str_path + '>'
                str_path += node

            str_error = "parameter %r, reason %r" % (str_path, ex.message)
            raise ServiceException('INVALID_REQUEST', "JSON request body doesn't match expected format.", str_error,
                                   module=find_module_associated_to_uri(req.path))
        except Exception as ex:
            raise ServiceException('INVALID_REQUEST', "Cannot validate JSON request body.", str(ex),
                                   module=find_module_associated_to_uri(req.path))

    # def process_response(self,req,resp, resource, req_succeeded):
    #     print("processing response")
    #     # pass


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
        ContextInfo.clear_auth_token()

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

        ContextInfo.set_auth_token(decoded_token)

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
                    auth_token = ContextInfo.get_context_data('auth_token')

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


def find_resource_associated_to_uri(uri):
    """
    Search for the api resource associated with path as defined through falcon framework

    :param req: Http Request object
    :return: string: The resource of the api module associated with path in request object.  If the requested path doesn't match any api, returns None.
    """

    # Search with app router, so we are always up to date.
    resource = falcon_app._router.find(uri)

    if resource is not None:
        return resource
    else:
        return None


def find_module_associated_to_uri(uri):
    """
    Search for the api module associated with path as defined through falcon framework

    :param req: Http Request object
    :return: string: The name of the api module associated with path in request object.  If the requested path doesn't match any api, returns None.
    """
    resource = find_resource_associated_to_uri(uri)

    if resource and resource[0] is not None:
        return resource[0].__module__
    else:
        return None


middleware_list = [Validate(), ValidateAuthToken()]

falcon_app = API(middleware=middleware_list)


# The 'BaseException' handler must be declared BEFORE the other ones
falcon_app.add_error_handler(BaseException, base_exception_handler)

# Always catch ServiceException
falcon_app.add_error_handler(ServiceException, service_exception_handler)
