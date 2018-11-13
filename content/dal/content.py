from libservice.db.db import db_object
from libservice.base.entity import Entity
import json


class FacadeContent:
    """
    Allow the users management into the database
    """

    # Define the requests for the following function(s)
    REQUEST_CONTENT_LIST = "SELECT content_id, title, CAST(popularity AS CHAR), " \
                           "director, genre, CAST(imdb_score AS CHAR) FROM content"

    @staticmethod
    def get_list(search=None):

        query = FacadeContent.REQUEST_CONTENT_LIST

        if search is not None:
            query += " WHERE MATCH(title, genre, director) AGAINST('"+search+"*' IN BOOLEAN MODE ) "

        cursor = db_object.query(query)
        my_list = {}

        result_set = cursor.fetchall()

        for content in result_set:

            my_list[content[0]] = {}
            my_list[content[0]]['title'] = content[1]
            my_list[content[0]]['popularity'] = content[2]
            my_list[content[0]]['director'] = content[3]
            my_list[content[0]]['genre'] = content[4]
            my_list[content[0]]['imdb_score'] = content[5]

        return my_list

    ###########################################################################################

    # Define the requests for the following function(s)
    REQUEST_INSERT_CONTENT_LIST = "INSERT INTO content (title, popularity, director, genre, imdb_score) " \
                                  "VALUES (%s, %s, %s, %s, %s);"

    @staticmethod
    def add(entity):

        # Make sure all pending values are initialized
        entity.replace_all_none_by_empty()

        db_object.query(FacadeContent.REQUEST_INSERT_CONTENT_LIST, (entity['title'],
                                                                    entity['popularity'],
                                                                    entity['director'],
                                                                    json.dumps(entity['genre']),
                                                                    entity['imdb_score'],))
        db_object.commit_query()


###########################################################################################

    # Define the requests for the following function(s)
    REQUEST_EXIST_CONTENT_ITEM = "SELECT content_id FROM content WHERE content_id = lower(%s)"

    @staticmethod
    def get_content_by_id(content_item_id):
        """
        Verify is a content item with the requested id exist in the database

        :param content_item_id: The content_item_id on which we have to perform the verification [String, Required]
        :return: True if found.
        :return: False if not found.
        """

        cursor = db_object.query(FacadeContent.REQUEST_EXIST_CONTENT_ITEM, (int(content_item_id),))
        result_set = cursor.fetchall()
        return result_set

    #######################################################################################

    # Define the requests for the following function(s)
    REQUEST_DELETE_CONTENT_ITEM = """DELETE FROM content WHERE content_id = %s;"""

    @staticmethod
    def delete(content_item_id):
        """
        Delete's a Content item with id

        :param content_item_id: The content item id to remove [String, Required]
        :return: True if deleted.
        :return: False if not deleted.
        """

        db_object.query(FacadeContent.REQUEST_DELETE_CONTENT_ITEM,(int(content_item_id),))

    #######################################################################################

    # Define the requests for the following function(s)
    REQUEST_UPDATE_CONTENT_ITEM = """UPDATE content SET title = %s, popularity = %s, director = %s, genre = %s, 
    imdb_score = %s WHERE content_id = %s"""

    @staticmethod
    def update(content_item_id, entity):
        """
        Update a Content item with id

        :param content_item_id: The content item id to update [String, Required]
        :param entity: The content data to update [String, Required]
        :return: True if deleted.
        :return: False if not deleted.
        """

        db_object.query(FacadeContent.REQUEST_UPDATE_CONTENT_ITEM, (entity['title'],
                                                                    entity['popularity'],
                                                                    entity['director'],
                                                                    json.dumps(entity['genre']),
                                                                    entity['imdb_score'],
                                                                    int(content_item_id),))

    #######################################################################################

    # Define the requests for the following function(s)
    REQUEST_GET_CONTENT_ITEM = """SELECT title, popularity, director, genre, imdb_score FROM content 
    WHERE content_id = %s"""

    @staticmethod
    def get_content_info_by_id(content_item_id):
        """
        Fetch a Content item with id

        :param content_item_id: The content item id to update [String, Required]
        :return: Entity of content item information.
        """

        cursor = db_object.query(FacadeContent.REQUEST_GET_CONTENT_ITEM, (content_item_id,))

        result_set = cursor.fetchall()

        if result_set:
            return Entity({'title': result_set[0][0],
                           'popularity': float(result_set[0][1]),
                           'director': result_set[0][2],
                           'genre': result_set[0][3],
                           'imdb_score': float(result_set[0][4])
                           })
        return None
