import json
from content.dal.content import FacadeContent
from libservice.base.service import ServiceException


class Content:
    """
    Content management class
    """
    @staticmethod
    def get_content_list(search):
        """
        Get a content list data

        :param search: search parameter
        :return: A List of Dictionary with all the item information
        """

        try:
            # Make sure the user exist
            content_list = FacadeContent.get_list(search)
            print("RETURNING CONTENT LIST")
            return json.dumps(content_list)
        except Exception as e:
            raise ServiceException('USER_DATABASE_QUERY_FAIL', "Unable to fetch content.", str(e))

    ####################################################################################################

    @staticmethod
    def add_content(entity):
        """
        Add content to content list data

        :param entity: content to be added
        :return: A List of Dictionary with all the added item information
        """

        try:
            FacadeContent.add(entity)
            print("ADDING CONTENT LIST")
        except Exception as e:
            raise ServiceException('CONTENT_DATABASE_QUERY_FAIL', "Unable to add content.", str(e))

    ####################################################################################################

    @staticmethod
    def delete_content_item(content_item_id):
        """
        Delete content item with id

        :param content_item_id: content item id to be deleted
        :return: A List of Dictionary with all the deleted item information
        """

        try:
            # Make sure the content exist
            content_item_exist = FacadeContent.get_content_by_id(content_item_id)
        except Exception as e:
            raise ServiceException('ADMIN_USER_DATABASE_QUERY_FAIL', "Unable to delete content.", str(e))

        print(content_item_exist)

        if not content_item_exist:
            raise ServiceException('INVALID_CONTENT_ID', 'Content id not found. Invalid content id')

        try:
            # Make sure the content exist
            FacadeContent.delete(content_item_id)
        except Exception as e:
            raise ServiceException('ADMIN_USER_DATABASE_QUERY_FAIL', "Unable to delete content.", str(e))

    ####################################################################################################

    @staticmethod
    def update_content_item(content_item_id, entity):
        """
        Update content item with id

        :param content_item_id: content item id to be updated
        :param entity: content to be updated
        :return: A List of Dictionary with all the updated item information
        """

        try:
            # Make sure the content exist
            content_item = FacadeContent.get_content_by_id(content_item_id)
        except Exception as e:
            raise ServiceException('CONTENT_DATABASE_QUERY_FAIL', "Unable to update content.", str(e))

        if not content_item:
            raise ServiceException('INVALID_CONTENT_ID', 'Content id not found. Invalid content id')

        # Retrieve the user current information
        try:
            content = FacadeContent.get_content_info_by_id(content_item_id)
        except Exception as e:
            raise ServiceException('CONTENT_DATABASE_LOAD_QUERY_FAIL', "Fail to load the Content current information.", str(e))

        # Update the content new information over the current information
        if entity.member_exist('title'):
            content['title'] = entity['title']
        if entity.member_exist('popularity'):
            content['popularity'] = entity['popularity']
        if entity.member_exist('director'):
            content['director'] = entity['director']
        if entity.member_exist('genre'):
            content['genre'] = entity['genre']
        if entity.member_exist('imdb_score'):
            content['imdb_score'] = entity['imdb_score']

        try:
            # Make sure the content exist
            FacadeContent.update(content_item_id, content)
        except Exception as e:
            raise ServiceException('ADMIN_CONTENT_DATABASE_QUERY_FAIL', "Unable to update content.", str(e))

    ##################################################################################################################

    @staticmethod
    def get_content_from_id(content_item_id):
        """
        Get content item with id

        :param content_item_id: content item id to be fetched
        :return: A Entity of Dictionary with all the item information
        """

        try:
            # Make sure the content exist
            content = FacadeContent.get_content_info_by_id(content_item_id)
            return content
        except Exception as e:
            raise ServiceException('ADMIN_USER_DATABASE_QUERY_FAIL', "Unable to fetch content item.", str(e))

