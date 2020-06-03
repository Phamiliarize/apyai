import json
import falcon
import config

from peewee_validates import ModelValidator
from playhouse.shortcuts import model_to_dict


class ListApi(object):
    def __init__(self, Model, sort="id", page_size=config.page_size):
        self.Model = Model
        self.sort_column = sort
        self.page_size = page_size
        

    def on_get(self, req, resp, **params):
        query = self.Model.select()
        sort_column = getattr(self.Model, self.sort_column)

        doc = {
            "total_count": query.count(),
            "page": int(req.params["page"] or 1) if "page" in req.params else 1,
            "next_page": None,
            "results": []
        }

        if "sort_column" in req.params:
            if req.params["sort_column"] in self.Model._meta.fields:
                sort_column = getattr(self.Model, req.params["sort_column"])
        if "order" in req.params:
            if req.params["order"] == 'DESC':
                sort_column = sort_column.desc()

        for result in query.order_by(sort_column).paginate(doc["page"],  self.page_size):
            doc["results"].append(model_to_dict(result))

        if doc["page"] == 1:
            doc["next_page"] = None if doc["total_count"] ==  self.page_size else doc["page"] + 1
        else:
            doc["next_page"] = None if doc["total_count"] - ((doc["page"] - 1) *  self.page_size + len(doc["results"])) == 0 else doc["page"] + 1

        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)


    def on_post(self, req, resp, **params):
        obj = req.media or {}

        # Validation
        validator = ModelValidator(self.Model(**obj))
        validator.validate()

        if bool(validator.errors):
            raise falcon.HTTPBadRequest(validator.errors)

        doc = model_to_dict(self.Model.create(**validator.data))
        
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_201