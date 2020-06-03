import json
import falcon

from peewee_validates import ModelValidator
from playhouse.shortcuts import model_to_dict


class SingleApi(object):
    def __init__(self, Model):
        self.Model = Model


    def on_get(self, req, resp, **params):
        try:
            doc = model_to_dict(self.Model.get(**params))
        except self.Model.DoesNotExist:
            raise falcon.HTTPNotFound
            
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)


    def on_patch(self, req, resp, **params):
        obj = req.media or {}
        patch_model = self.Model(**obj)

        # Disable required fields
        for name, field in patch_model._meta.fields.items():
            if getattr(field, 'primary_key', False):
                continue
            setattr(field, 'null', True)
        
        # Validation
        validator = ModelValidator(patch_model)
        validator.validate()

        if bool(validator.errors):
            raise falcon.HTTPBadRequest(validator.errors)

        try:
            doc = self.Model.get(**params)
        except self.Model.DoesNotExist:
            raise falcon.HTTPNotFound

        # Update only if not none.
        for key in validator.data:
            if validator.data[key] is not None:
                setattr(doc, key, validator.data[key])
        
        doc.save()
        
        resp.body = json.dumps(model_to_dict(doc), ensure_ascii=False)


    def on_put(self, req, resp, **params):
        obj = req.media or {}

        # Validation
        validator = ModelValidator(self.Model(**obj))
        validator.validate()

        if bool(validator.errors):
            raise falcon.HTTPBadRequest(validator.errors)

        try:
            doc = self.Model.get(**params)
        except self.Model.DoesNotExist:
            raise falcon.HTTPNotFound

        # Update
        for key in validator.data:
            setattr(doc, key, validator.data[key])
        
        doc.save()
        
        resp.body = json.dumps(model_to_dict(doc), ensure_ascii=False)


    def on_delete(self, req, resp, **params):
        # Check for existence
        try:
            doc = self.Model.get(**params)
        except self.Model.DoesNotExist:
            raise falcon.HTTPNotFound

        # Perform a cascading delete
        doc.delete_instance(recursive=True)

        resp.status = falcon.HTTP_204