import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append('../')
# sys.path.append('../../')

# sys.path.remove('/home/woi/Workspace/Heroku/app/catalog/app')
# sys.path.append('/home/woi/Workspace/Heroku/app/catalog/app')

# absFilePath = os.path.abspath(__file__)
# print(absFilePath)
# fileDir = os.path.dirname(os.path.abspath(__file__))
# print(fileDir)
# parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(parentDir)

import os
# ON_HEROKU = os.environ.get('ON_HEROKU')
#
# if ON_HEROKU:
#     # get the heroku port
#     port = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995
#     print(port)
# else:
#     port = 3000
#
# print(port)
# print(os.environ.get('ON_HEROKU'))
port = int(os.environ.get("PORT", 8000))
print(port)

from wsgiref import simple_server
from libservice.base.service import falcon_app
import json

from account.api.user import UserResource
from account.api.session import SessionResource
from content.api.content_list import ContentListResource
from admin.api.admin_user import AdminResource
from admin.api.admin_session import AdminSessionResource
from libservice.base.meta_info import MetaResource
# from libservice.db.db import DatabaseResource


test_input_body = {
    "type": "object",
    "properties": {
    }
}


class Test(object):
    def __init__(self):
        MetaResource.add_meta_resource('Test', 'GET', test_input_body)
        MetaResource.add_meta_resource('Test', 'POST', test_input_body)

    def on_get(self, res, resp):
        # print("Success")
        resp.body = json.dumps({"Success": "Test"})

    def on_post(self, res, resp):
        # print("Success")
        resp.body = json.dumps({"Success": "Test"})


# DatabaseResource()

falcon_app.add_route('/test', Test())
falcon_app.add_route('/user', UserResource())
falcon_app.add_route('/session', SessionResource())
falcon_app.add_route('/admin/user', AdminResource())
falcon_app.add_route('/admin/session', AdminSessionResource())
falcon_app.add_route('/content/list', ContentListResource())
falcon_app.add_route('/content/list/{content_item_id}', ContentListResource())

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', port, falcon_app)
    httpd.serve_forever()
