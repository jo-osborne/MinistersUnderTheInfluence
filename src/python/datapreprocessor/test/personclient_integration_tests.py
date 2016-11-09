import unittest
import requests
from datapreprocessor.meetingsapiclient import personClient
from settings import INTEGRATION_TESTS
from settings import MEETINGS_API_BASE_URL

@unittest.skipUnless(INTEGRATION_TESTS, 'api integration tests')
class PersonClientTest(unittest.TestCase):

    def setUp(self):
        self.client = personClient(MEETINGS_API_BASE_URL)

    def tearDown(self):
        people = self.client.get_all()
        for person in people:
            self.client.delete(person['attributes']['name'])

    def test_person_lifecycle(self):
        """This test verifies that a person can be created, retrieved and deleted"""
        person_name = "Freddy the Frog"

        # Initial Retrieve (when person does not exist)
        no_person = self.client.get_by_name(person_name)
        self.assertEqual(None, no_person)

        # Create person
        create_response = self.client.add(person_name)
        self.assertEqual(requests.codes.created, create_response.status_code)

        # Retrieve person
        person = self.client.get_by_name(person_name)
        self.assertEqual(person_name, person['attributes']['name'])

        # Delete person
        delete_response = self.client.delete(person_name)
        self.assertEqual(requests.codes.no_content, delete_response.status_code)
