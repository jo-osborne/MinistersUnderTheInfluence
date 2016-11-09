from abc import ABCMeta, abstractmethod
import requests
import json

class MeetingsApiClient:
    """This abstract client provides an interface for interacting with the meetings api to create, retrieve and
    delete entities such as people, organisations, roles etc"""

    __metaclass__ = ABCMeta

    def __init__(self, base_url, entity_name):
        self._url = base_url + entity_name
        self._entity_type = entity_name
        self._headers = {'content-type': 'application/vnd.api+json; charset=utf-8'}


    def _get(self):
        return requests.get(self._url, headers = self._headers)


    def _post(self, data):
        return requests.post(self._url, data = json.dumps(data), headers = self._headers)


    def _delete(self, entity_url):
        return requests.delete(entity_url, headers = self._headers)


    def get_all(self):
        """Return a collection containing all entities of this type from the meetings api"""
        response = self._get()
        items = response.json()['data']
        return items


    def get_by_name(self, name):
        """Search for an entity by name. If it exists, return the entity else return None"""
        matching_entities = filter((lambda p: p['attributes']['name'] == name), self.get_all())
        if matching_entities:
            return matching_entities[0]
        else:
            return None


    def add(self, name):
        """Check if entity with this name exists and if not, create it.
        Return http response, or None if entity already exists."""
        if self.get_by_name(name):
            return None
        else:
            data = {'data': {'type': self._entity_type, 'attributes': {'name': name}}}
            response = self._post(data)
            return response


    def delete(self, name):
        """If entity exists, delete it. Return http response, or None if entity does not exist"""
        entity = self.get_by_name(name)
        if entity:
            return self._delete(entity['links']['self'])
        else:
            return None


def personClient(base_url):
    return MeetingsApiClient(base_url, 'people')

def organisationClient(base_url):
    return MeetingsApiClient(base_url, 'organisations')
