import json
from .model import Test as Model
from ..utils import ListApi, SingleApi

import falcon

class TestList(ListApi.ListApi):
    def __init__(self):
        super(TestList, self).__init__(Model)

class Test(SingleApi.SingleApi):
    def __init__(self):
        super(Test, self).__init__(Model)