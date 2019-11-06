import os
from unittest import TestCase

from py_jama_rest_client.client import JamaClient
from test import CountedJamaClient

jama_url = os.environ['JAMA_API_URL']
jama_api_client_id = os.environ['JAMA_API_CLIENT_ID']
jama_api_client_secret = os.environ['JAMA_API_CLIENT_SECRET']


class TestJamaClientIter(TestCase):
    jama_client = CountedJamaClient(jama_url, (jama_api_client_id, jama_api_client_secret), oauth=True)

    def test_iter(self):
        # Check if only an API call is made on demand
        i = 0
        project = self.jama_client.get_projects()[0]
        i += 1
        self.assertEqual(self.jama_client.core.gets, i)
        item_iter = self.jama_client.get_iter('items', page_size=2, params={'project': project['id']})
        self.assertEqual(self.jama_client.core.gets, i)
        for items in item_iter:
            i += 1
            self.assertEqual(len(items), 2)
            self.assertEqual(self.jama_client.core.gets, i)
            if i > 2:
                break
        self.assertEqual(self.jama_client.core.gets, i)


class TestJamaClientOath(TestCase):
    jama_client = JamaClient(jama_url, (jama_api_client_id, jama_api_client_secret), oauth=True)

    def test_is_authenticated_1(self):
        self.assertTrue(self.jama_client.is_authenticated())

    def test_is_authenticated_2(self):
        invalid_credentials = (jama_api_client_id, jama_api_client_secret + '_invalid')
        self.jama_client = JamaClient(jama_url, invalid_credentials, oauth=True)
        self.assertFalse(self.jama_client.is_authenticated())

    def test_is_authenticated_3(self):
        invalid_host = jama_url + '.invalid'
        self.jama_client = JamaClient(invalid_host, (jama_api_client_id, jama_api_client_secret), oauth=True)
        self.assertFalse(self.jama_client.is_authenticated())

    def test_is_authenticated_4(self):
        invalid_url = ''
        self.jama_client = JamaClient(invalid_url, (jama_api_client_id, jama_api_client_secret), oauth=True)
        self.assertFalse(self.jama_client.is_authenticated())
