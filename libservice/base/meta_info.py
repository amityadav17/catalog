import json


class MetaResource(object):
    _meta_resource_content = {}


    @classmethod
    def get_resource_metadata(cls):
        return cls._meta_resource_content

    @classmethod
    def add_meta_resource(cls, resource, req_type, value):

        if "data" not in cls._meta_resource_content:
            cls._meta_resource_content['data'] = {}
            # print("DATA Absent")

        if resource not in cls._meta_resource_content['data']:
            cls._meta_resource_content['data'][resource] = {}
            # print("Resource Absent")

        if req_type not in cls._meta_resource_content['data'][resource]:
            cls._meta_resource_content['data'][resource][req_type] = {}
            # print("Req_type Absent")

        cls._meta_resource_content['data'][resource][req_type] = value
