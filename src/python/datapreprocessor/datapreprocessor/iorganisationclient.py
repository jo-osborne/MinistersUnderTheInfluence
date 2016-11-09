from abc import ABCMeta, abstractmethod
import requests
import json

class IOrganisationClient:
    """This abstract client provides an interface for interacting with the meetings api to create, retrieve and
    delete organisations"""
    __metaclass__ = ABCMeta

    def __init__(self, url):
        self.url = url
        self.headers = {'content-type': 'application/vnd.api+json; charset=utf-8'}


    def _build_url(self, path):
        return self.url + path


    def _get(self, url):
        return requests.get(url, headers = self.headers)


    def _post(self, url, data):
        return requests.post(url, data = json.dumps(data), headers = self.headers)


    def _delete(self, url):
        return requests.delete(url, headers = self.headers)


    @abstractmethod
    def get_all(self):
        """Return a collection containing all organisations from the meetings api"""
        pass


    @abstractmethod
    def get_by_name(self, organisation_name):
        """Search for organisation by name. If they exist, return the organisation else return None"""
        pass


    @abstractmethod
    def add(self, organisation_name):
        """Check if organisation with this name exists and if not, create them.
        Return http response, or None if organisation already exists."""
        pass


    @abstractmethod
    def delete(self, organisation_name):
        """If organisation exists, delete it. Return http response, or None if organisation does not exist"""
        pass
