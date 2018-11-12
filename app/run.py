from wsgiref import simple_server
from libservice.base.service import falcon_app
import json

from account.api.user import UserResource
from account.api.session import SessionResource
from content.api.content_list import ContentListResource
from admin.api.admin_user import AdminResource
from admin.api.admin_session import AdminSessionResource


class Test(object):
    def on_get(self, res, resp):
        # print("Success")
        resp.body = json.dumps({"Success": "Test"})


falcon_app.add_route('/test', Test())
falcon_app.add_route('/user', UserResource())
falcon_app.add_route('/session', SessionResource())
falcon_app.add_route('/admin/user', AdminResource())
falcon_app.add_route('/admin/session', AdminSessionResource())
falcon_app.add_route('/content/list', ContentListResource())
falcon_app.add_route('/content/list/{content_item_id}', ContentListResource())

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, falcon_app)
    httpd.serve_forever()
