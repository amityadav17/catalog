

"""
@apiDefine HeaderRequired

@apiHeader {object} Content-Type application/json
@apiHeader {object} Auth-Token Auth-Token required for authorization. Run session api to get Auth-Token

@apiHeaderExample {json} Header-Example:
    {
        "Content-Type" : "application/json",
        "Auth-Token" : "eyJ0eXAiOiJKV1QiCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InV1aWQiOiJoiZ3Vlc3QifSwiZXhwaXJ5IjoxNTQyMTA0OD
        gxLjQxNTYzNzUsInR5cGUOiJBdXRoLVRva2VuIn0.K2xdhYQLXu27O7pgIJGi5rmsAqhZpazItiKpk7NOi8"
    }

@apiError {Object} INVALID_REQUEST Failed to decode Auth-Token. Not a 'Auth-Token'.
@apiError {Object} INVALID_FORMAT_UUID Auth-Token is not valid. 'uuid' is missing.
@apiError {Object} INVALID_FORMAT_TYPE Auth-Token' is malformed.'type' is missing.
@apiError {Object} UNAUTHORIZED_NOT_AUTHENTICATED Auth-Token is not valid
@apiError {Object} UNAUTHORIZED_SESSION_EXPIRED Auth-Token has expired
@apiError {Object} FORBIDDEN User doesn't have access to this resource.

"""


"""

@apiGroup Content
@api {get} /content/list Get Content Tree
@apiName Get Content Tree
@apiDescription Request the whole content tree

@apiPermission admin, user, guest

@apiUse HeaderRequired

@apiParam {String} [search] URL query parameter to do a full text search based on database.

@apiError {Object} DATA_RETRIEVAL_FAILED Failed to retrieve content data
@apiError {Object} METHOD_NOT_ALLOWED Method not allowed

@apiError (Error - 404) {Object} DATA_RETRIEVAL_FAILED Failed to retrieve content data
@apiError (Error - 405) {Object} METHOD_NOT_ALLOWED Method not allowed

@apiSuccess (200) {Object[]} Content-List List of all content

@apiSuccessExample {json} Success-Response:
    {
        "112": {
            "genre": ["Action", " Adventure", " Fantasy", "Sci-Fi"],
            "title": "Star Wars : Episode VI - Return of the Jedi",
            "imdb_score": "8.3",
            "popularity": "83.0",
            "director": "Richard Marquand"
        },
        "174": {
            "genre": ["Comedy", "Music", "Talk-Show"],
            "title": "The Tonight Show Starring Johnny Carson",
            "imdb_score": "8.3",
            "popularity": "83.0",
            "director": "Bobby Quinn"
        },
        "224": {
            "genre": ["Action", " Adventure", "Sci-Fi"],
            "title": "Star Trek : The Next Generation",
            "imdb_score": "8.8",
            "popularity": "88.0",
            "director": "Cliff Bole"
        },
        "244": {
            "genre": ["Action", "Adventure", " Fantasy", "Sci-Fi"],
            "title": "Star Wars : Episode I - The Phantom Menace",
            "imdb_score": "6.4",
            "popularity": "64.0",
            "director": "George Lucas"
        }
    }

"""

"""

@apiGroup Content
@api {post} /content/list/ Add Content to Content Tree
@apiName Add Content to Content Tree
@apiDescription Add media content item information to content Tree

@apiPermission admin

@apiUse HeaderRequired

@apiParam {String} title The title of the content.
@apiParam {array} genre The genre of the content.
@apiParam {String} director The director of the media.
@apiParam {String} [idbm_score] The imdb score of the content.
@apiParam {String} [popularity] The popularity of the content.

@apiError {Object} CONTENT_DATABASE_QUERY_FAIL Unable to add content.
@apiError {Object} INVALID_REQUEST_FORMAT JSON request body doesn't match expected format.
@apiError {Object} INVALID_REQUEST_JSON Cannot validate JSON request body.

@apiSuccess (201) {Object[]} Content-item Media content item information

@apiSuccessExample {json} Success-Response:
    {
        "Success": "Content added Successfully"
    }
"""

"""

@apiGroup Content
@api {PUT} /content/list/{content_id} Update Content item
@apiName Update Content information for the provided content id
@apiDescription Update media content item information with the provided content id 

@apiPermission admin

@apiUse HeaderRequired

@apiParam {String} [title] The title of the content.
@apiParam {array} [genre] The genre of the content.
@apiParam {String} [director] The director of the media.
@apiParam {String} [idbm_score] The imdb score of the content.
@apiParam {String} [popularity] The popularity of the content.

@apiError {Object} CONTENT_DATABASE_QUERY_FAIL Unable to update content.
@apiError {Object} CONTENT_ITEM_UPDATE_FAIL A content item id needs to be specified
@apiError {Object} CONTENT_UPDATE_FAIL Unable to load the content information that has just been updated.
@apiError {Object} CONTENT_DATABASE_QUERY_FAIL Unable to delete content.
@apiError {Object} INVALID_CONTENT_ID 'Content id not found. Invalid content id.
@apiError {Object} CONTENT_DATABASE_LOAD_QUERY_FAIL Fail to load the Content current information.
@apiError {Object} ADMIN_CONTENT_DATABASE_QUERY_FAIL Unable to update content.

@apiSuccess (200) {Object[]} Updated-Content-Item Updated Content item information


@apiSuccessExample {json} Success-Response:
    {
        "content_id":"254"
        "genre": ["Action", " Adventure", " Fantasy", "Sci-Fi"],
        "title": "Star Wrs : Episo VI - Return of the Jdi",
        "imdb_score": "8.3",
        "popularity": "83.0",
        "director": "Richard Marquand"
    }
"""

"""

@apiGroup Content
@api {DELETE} /content/list/{content_id} Delete Content item
@apiName Delete Content information for the provided content id
@apiDescription Delete media content item information with the provided content id 

@apiPermission admin

@apiUse HeaderRequired

@apiError {Object} CONTENT_ITEM_DELETE_FAIL A content item id needs to be specified
@apiError {Object} CONTENT_ITEM_DELETE_VALIDATION_FAIL An error occured while validating the content deletion.

@apiError {Object} CONTENT_ITEM_DELETE_FAIL Unable to delete content.

@apiError {Object} INVALID_CONTENT_ID 'Content id not found. Invalid content id.
@apiError {Object} ADMIN_CONTENT_DATABASE_QUERY_FAIL Unable to delete content.

@apiSuccess (204) {Object[]} Updated-Content-Item Updated Content item information


@apiSuccessExample {json} Success-Response:
    {
    }
"""

"""

@apiGroup USER
@api {post} /user Add User account
@apiName Add a new user account
@apiDescription Add a new user account

@apiPermission admin

@apiUse HeaderRequired

@apiParam {String} [firstname] The user’s first name.
@apiParam {String} [lastname] The user’s last name.
@apiParam {String} email The email address associated with the user’s account.
@apiParam {String} password The password associated with the user’s account. Must Have minimum 8 charcters, 1 Capital Letter and Numeric value

@apiError {Object} USER_CREATION_FAIL Unable to load the user information that has just been created.
@apiError {Object} INVALID_REQUEST_FORMAT JSON request body doesn't match expected format.
@apiError {Object} INVALID_REQUEST_JSON Cannot validate JSON request body.

@apiError {Object} USER_DATABASE_QUERY_FAIL Fail to verify if the user already exist.
@apiError {Object} USER_ALREADY_EXIST_FAIL User already exists in the database.
@apiError {Object} USER_CREATION_EMAIL_FAIL Email doesn't meet requirements.
@apiError {Object} USER_CREATION_PASSWORD_FAIL Password doesn't meet requirements.
@apiError {Object} USER_CREATION_ENCRYPTION_FAIL The encryption of the password has failed.
@apiError {Object} USER_DATABASE_CREATION_QUERY_FAIL The creation of the user has failed.

@apiSuccess (201) {Object[]} User-Account User account information

@apiSuccessExample {json} Success-Response:
    {
        "lastname": "lname123",
        "firstname": "fname123",
        "login": "test12345@email.com"
    }
"""

"""

@apiGroup USER
@api {post} /session User session management
@apiName User session management
@apiDescription Create a User session. If email and password are both empty then user will be logged in as guest and if not they will be logged in as user. Session is valid for 24 hrs

@apiParam {String} email The email address associated with the user’s account.
@apiParam {String} password The password associated with the user’s account.

@apiError {Object} USER_INVALID_CREDENTIALS_TOKEN Invalid credentials. Token generation failed.
@apiError {Object} INVALID_REQUEST_FORMAT JSON request body doesn't match expected format.
@apiError {Object} INVALID_REQUEST_JSON Cannot validate JSON request body.

@apiError {Object} USER_DATABASE_QUERY_FAIL Fail to load the user current information.
@apiError {Object} USER_UNKNOWN_INVALID_CREDENTIALS Invalid credentials Unknown user.
@apiError {Object} USER_INVALID_CREDENTIALS Invalid credentials.

@apiError {Object} USER_INVALID_PASSWORD_CREDENTIALS Invalid credentials Invalid password.

@apiSuccess (200) {Object[]} User-Account User account information

@apiSuccessExample {json} Success-Response:
{
    "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cpXVCJ9.eyJleHBpcnkiOjE1NDIxMTUzNTIuNDgwNTMsInR5cGUiOiJBdLVRva2VuIiwiZGF0YSI
    6eyJ1dWlkIjoiMDJmNZTY3ZS0xMWU4LTg1NzgtMDgwMDI3OGQxMjQ3IiwidHlwZSI6Imd1ZXN0In19.D9TAQMpDCumiquC11435-LXVy-12Eni6PwZr
    h0JXBwE"
}
"""

"""

@apiGroup ADMIN
@api {post} /admin/user Create Admin account
@apiName Create a new admin account
@apiDescription Create a new admin account

@apiUse HeaderRequired

@apiParam {String} [firstname] The admin user’s first name.
@apiParam {String} [lastname] The admin user’s last name.
@apiParam {String} email The email address associated with the admin user’s account.
@apiParam {String} password The password associated with the admin user’s account. Must Have minimum 8 charcters, 1 Capital Letter and Numeric value

@apiError {Object} ADMIN_CREATION_EMAIL_FAIL Login/Email required..
@apiError {Object} INVALID_REQUEST_FORMAT JSON request body doesn't match expected format.
@apiError {Object} INVALID_REQUEST_JSON Cannot validate JSON request body.

@apiError {Object} ADMIN_CREATION_PASSWORD_FAIL "Password Required".

@apiError {Object} ADMIN_USER_LOAD_FAIL Unable to load the user information that has just been created.
@apiError {Object} ADMIN_USER_ALREADY_EXIST_FAIL User already exists in the database.
@apiError {Object} ADMIN_USER_CREATION_EMAIL_FAIL Email doesn't meet requirements.
@apiError {Object} ADMIN_USER_CREATION_PASSWORD_FAIL Password doesn't meet requirements.
@apiError {Object} ADMIN_USER_ENCRYPTION_FAIL The encryption of the password has failed.
@apiError {Object} ADMIN_USER_DATABASE_CREATION_QUERY_FAIL The creation of the user has failed.

@apiSuccess (201) {Object[]} Admin-Account Admin account information

@apiSuccessExample {json} Success-Response:
    {
        "lastname": "lname123",
        "firstname": "fname123",
        "login": "test12345@email.com"
    }
"""

"""

@apiGroup ADMIN
@api {post} /admin/session Admin session management
@apiName Admin session management
@apiDescription Create a admin session. Session is valid for 24 hrs

@apiParam {String} email The email address associated with the user’s account.
@apiParam {String} password The password associated with the user’s account.

@apiError {Object} ADMIN_USER_INVALID_CREDENTIALS_TOKEN Invalid credentials. Token generation failed.
@apiError {Object} INVALID_REQUEST_FORMAT JSON request body doesn't match expected format.
@apiError {Object} INVALID_REQUEST_JSON Cannot validate JSON request body.

@apiError {Object} ADMIN_CREATION_EMAIL_FAIL Login/Email required.
@apiError {Object} ADMIN_CREATION_PASSWORD_FAIL Password Required.
@apiError {Object} ADMIN_USER_INVALID_PASSWORD_CREDENTIALS Invalid credentials Invalid password.

@apiError {Object} ADMIN_USER_DATABASE_QUERY_FAIL Fail to load the user current information.
@apiError {Object} ADMIN_USER_LOAD_QUERY_FAIL Fail to load the user current information.
@apiError {Object} ADMIN_USER_UNKNOWN_CREDENTIALS Invalid credentials", "Unknown user.
@apiError {Object} ADMIN_USER_INVALID_CREDENTIALS Invalid credentials.

@apiSuccess (200) {Object[]} Admin-Account Admin account information

@apiSuccessExample {json} Success-Response:
{
    "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cpXVCJ9.eyJleHBpcnkiOjE1NDIxMTUzNTIuNDgwNTMsInR5cGUiOiJBdLVRva2VuIiwiZGF0YSI
    6eyJ1dWlkIjoiMDJmNZTY3ZS0xMWU4LTg1NzgtMDgwMDI3OGQxMjQ3IiwidHlwZSI6Imd1ZXN0In19.D9TAQMpDCumiquC11435-LXVy-12Eni6PwZr
    h0JXBwE"
}
"""
