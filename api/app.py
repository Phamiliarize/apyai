import falcon
import json
import config


# Routes
from resources.test.test import TestList, Test

api = application = falcon.API()
api.req_options.strip_url_path_trailing_slash = True

testlist = TestList()
test = Test()

api.add_route('/test', testlist)
api.add_route('/test/{id:int}', test)