import unittest
import requests

from settings import INTEGRATION_TESTS
from settings import MEETINGS_API_BASE_URL

from datapreprocessor.organisationclient import OrganisationClient

@unittest.skipUnless(INTEGRATION_TESTS, 'api integration tests')
class OrganisationClientTest(unittest.TestCase):

    def setUp(self):
        self.client = OrganisationClient(MEETINGS_API_BASE_URL)

    def tearDown(self):
        for org in self.client.get_all():
            self.client.delete(org['attributes']['name'])

    def test_organisation_lifecycle(self):
        """This test verifies that an organisation can be created, retrieved and deleted"""
        org_name = "Hogwarts"

        # Initial Retrieve (when organisation does not exist)
        no_org = self.client.get_by_name(org_name)
        self.assertEqual(None, no_org)

        # Create organisation
        create_response = self.client.add(org_name)
        self.assertEqual(requests.codes.created, create_response.status_code)

        # Retrieve organisation
        organisation = self.client.get_by_name(org_name)
        self.assertEqual(org_name, organisation['attributes']['name'])

        # Delete person
        delete_response = self.client.delete(org_name)
        self.assertEqual(requests.codes.no_content, delete_response.status_code)
