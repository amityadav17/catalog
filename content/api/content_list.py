import json

from falcon.status_codes import HTTP_200, HTTP_204
from content.bl.content import Content
from content.api.content_schema import ContentResourceSchema
from libservice.base.meta_info import MetaResource
from libservice.base.entity import Entity
from libservice.base.service import ServiceException


class ContentListResource(object):
    """
    :description:
        Allow the access to the content list

    :title:
        Content list data management
    """

    def __init__(self):
        self.input_body_GET = ContentResourceSchema.get_request_schema("GET")
        self.input_body_POST = ContentResourceSchema.get_request_schema("POST")
        self.input_body_PUT = ContentResourceSchema.get_request_schema("PUT")
        self.input_body_DELETE = ContentResourceSchema.get_request_schema("DELETE")
        MetaResource.add_meta_resource(__class__.__name__, "GET", self.input_body_GET)
        MetaResource.add_meta_resource(__class__.__name__, "POST", self.input_body_POST)
        MetaResource.add_meta_resource(__class__.__name__, "PUT", self.input_body_PUT)
        MetaResource.add_meta_resource(__class__.__name__, "DELETE", self.input_body_DELETE)

    def on_get(self, req, resp):
        """
        :description:
            Get a list of items

        :title:
            Get list of items

        :auth_token_required: admin user guest

        :url_param: search
            Optional - The text search parameter

        :url_param: filter (NOT IMPLEMENTED)
            Optional - Specify search terms to filter the data. (Format: https://....?filter=FIELD_NAME1=@VALUE1|FIELD_NAME2=@VALUE2)

        :url_param: sort (NOT IMPLEMENTED)
            Optional - Specify the sort parameter and the sort order (Format: https://....?sort=FIELD_NAME:(ASC|DESC)

        :url_param: is_flat_list (NOT IMPLEMENTED)
            Optional - Specify if the result will be a flat list or the whole tree structure (with parent and children of the items found), format: 'true' or 'false', default 'false'

        :url_param: items_per_page (NOT IMPLEMENTED for PAGINATION)
            Optional - The number of items per page

        :url_param: page_number
            Optional - The page to return based on the items_per_page parameter

        :output_body::

            {

                "definitions":{
                    "base_structure": {
                        "type":"array",
                        "content_id": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "title of the content"
                                },
                                "genre": {
                                    "type": "string",
                                    "description": "The genre of the content"
                                },
                                "director": {
                                    "type": "array",
                                    "description": "The director of the movie"
                                },
                                "idbm_score": {
                                    "type": "integer",
                                    "description": "The imdb score of the content"
                                },
                                "popularity": {
                                    "type": "integer",
                                    "description": "The popularity of the comntent"
                                }
                            },
                            "required":["title", "genre", "popularity", "imdb_score", "director"]
                        }
                    }
                },

                "type":"object",
                "description":"List of content items",
                "properties":{
                    "items": {
                        "allOf":[
                            {"$ref": "#/definitions/base_structure"},
                            {
                                "properties": {
                                    "child_items": {
                                         "description": "Please refer child items structure from content_item api"
                                    }
                                }
                            }
                        ]
                    }
                }
            }

        """

        # Extract the content information
        search = req.get_param('search', default=None)
        print(search)

        tree = Content.get_content_list(search)

        # Fill the response
        resp.status = HTTP_200
        resp.body = tree

    def on_post(self, req, resp):
        """
        :description:
            Create a list of items

        :title:
            Create list of items

        :auth_token_required: admin

        :url_param: filter (NOT IMPLEMENTED)
            Optional - Specify search terms to filter the data. (Format: https://....?filter=FIELD_NAME1=@VALUE1|FIELD_NAME2=@VALUE2)

        :url_param: sort (NOT IMPLEMENTED)
            Optional - Specify the sort parameter and the sort order (Format: https://....?sort=FIELD_NAME:(ASC|DESC)

        :url_param: is_flat_list (NOT IMPLEMENTED)
            Optional - Specify if the result will be a flat list or the whole tree structure (with parent and children of the items found), format: 'true' or 'false', default 'false'

        :url_param: items_per_page (NOT IMPLEMENTED for PAGINATION)
            Optional - The number of items per page

        :url_param: page_number
            Optional - The page to return based on the items_per_page parameter

        :input_body::

            {
                "type": "object",
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
                        "description": "The director of the media"
                    },
                    "idbm_score": {
                        "type": "integer",
                        "description": "The imdb score of the content"
                    },
                    "popularity": {
                        "type": "integer",
                        "description": "The popularity of the content"
                    }
                },
                "required": ["title", "genre", "director"]
            }

        :output_body::

            {

                "definitions":{
                    "base_structure": {
                        "type":"array",
                        "content_id": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "title of the content"
                                },
                                "genre": {
                                    "type": "string",
                                    "description": "The genre of the content"
                                },
                                "director": {
                                    "type": "array",
                                    "description": "The director of the movie"
                                },
                                "idbm_score": {
                                    "type": "integer",
                                    "description": "The imdb score of the content"
                                },
                                "popularity": {
                                    "type": "integer",
                                    "description": "The popularity of the comntent"
                                }
                            },
                            "required":["title", "genre", "popularity", "imdb_score", "director"]
                        }
                    }
                },

                "type":"object",
                "description":"List of content items",
                "properties":{
                    "items": {
                        "allOf":[
                            {"$ref": "#/definitions/base_structure"},
                            {
                                "properties": {
                                    "child_items": {
                                         "description": "Please refer child items structure from content_item api"
                                    }
                                }
                            }
                        ]
                    }
                }
            }

        """

        # Extract the 'body' from the request
        entity = Entity(req.context['body'])

        Content.add_content(entity)

        # Fill the response
        resp.status = HTTP_200
        resp.body = json.dumps({"Success": "Content added Successfully"})

    def on_delete(self, req, resp, content_item_id=None):
        """
        :description:
            Delete a Content

        :title:
            Admin - Delete's a Item

        :auth_token_required: admin

        :code: 204
            DELETED - 0 - The item deleted

        :code: 400
            CONTENT_ITEM_DELETE_FAIL - Item delete fail

        """

        if content_item_id is None:
            raise ServiceException('CONTENT_ITEM_DELETE_FAIL', 'A content item id needs to be specified')

        Content.delete_content_item(content_item_id)

        try:
            content_item = Content.get_content_from_id(content_item_id)
        except Exception as e:
            raise ServiceException('CONTENT_ITEM_DELETE_VALIDATION_FAIL', 'An error occured while validating the content deletion', str(e))

        if content_item is not None:
            raise ServiceException('CONTENT_ITEM_DELETE_FAIL', 'Unable to delete the content')

        resp.status = HTTP_204

    def on_put(self, req, resp, content_item_id=None):
        """
        :description:
            Update a Content

        :title:
            Admin - Update a Item

        :auth_token_required: admin

        :input_body::

            {
                "type": "object",
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
                        "description": "The director of the media"
                    },
                    "idbm_score": {
                        "type": "integer",
                        "description": "The imdb score of the content"
                    },
                    "popularity": {
                        "type": "integer",
                        "description": "The popularity of the content"
                    }
                },
            }

        """

        if content_item_id is None:
            raise ServiceException('CONTENT_ITEM_UPDATE_FAIL', 'A content item id needs to be specified')

        # Extract the 'body' from the request
        entity = Entity(req.context['body'])

        Content.update_content_item(content_item_id, entity)

        # Retrieve the updated content information
        try:
            content_item = Content.get_content_from_id(content_item_id)
        except Exception as e:
            raise ServiceException('CONTENT_UPDATE_FAIL',
                                   "Unable to load the content information that has just been updated.", str(e))

        if not content_item:
            raise ServiceException('CONTENT_UPDATE_FAIL',
                                   "Unable to load the content information that has just been updated.")

        resp.status = HTTP_200
        resp.body = json.dumps(content_item)

