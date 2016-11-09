from abc import ABCMeta, abstractmethod
import requests
import json

from iorganisationclient import IOrganisationClient

class OrganisationClient(IOrganisationClient):
    def get_all(self):
        """Return a collection containing all organisations from the meetings api"""
        response = self._get(self._build_url('organisations'))
        items = response.json()['data']
        return items


    def get_by_name(self, organisation_name):
        """Search for organisation by name. If they exist, return the organisation else return None"""
        org = filter((lambda p: p['attributes']['name'] == organisation_name), self.get_all())
        if org:
            return org[0]
        else:
            return None


    def add(self, organisation_name):
        """Check if organisation with this name exists and if not, create them.
        Return http response, or None if organisation already exists."""
        if self.get_by_name(organisation_name):
            return None
        else:
            data = {'data': {'type': 'organisations', 'attributes': {'name': organisation_name}}}
            response = self._post(self._build_url('organisations'), data)
            return response


    def delete(self, organisation_name):
        """If organisation exists, delete it. Return http response, or None if organisation does not exist"""
        org = self.get_by_name(organisation_name)
        if org:
            return self._delete(org['links']['self'])
        else:
            return None
