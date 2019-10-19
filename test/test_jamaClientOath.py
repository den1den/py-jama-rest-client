import os
import unittest
from unittest import TestCase
from py_jama_rest_client.client import JamaClient


class TestJamaClientOath(TestCase):
    jama_url = os.environ['JAMA_API_URL']
    jama_api_client_id = os.environ['JAMA_API_CLIENT_ID']
    jama_api_client_secret = os.environ['JAMA_API_CLIENT_SECRET']
    jama_client = JamaClient(jama_url, (jama_api_client_id, jama_api_client_secret), oauth=True)

    def test_is_authenticated_1(self):
        self.assertTrue(self.jama_client.is_authenticated())

    def test_is_authenticated_2(self):
        invalid_credentials = (self.jama_api_client_id, self.jama_api_client_secret + '_invalid')
        self.jama_client = JamaClient(self.jama_url, invalid_credentials, oauth=True)
        self.assertFalse(self.jama_client.is_authenticated())

    def test_is_authenticated_3(self):
        invalid_host = self.jama_url + '.invalid'
        self.jama_client = JamaClient(invalid_host, (self.jama_api_client_id, self.jama_api_client_secret), oauth=True)
        self.assertFalse(self.jama_client.is_authenticated())

    def test_is_authenticated_4(self):
        invalid_url = ''
        self.jama_client = JamaClient(invalid_url, (self.jama_api_client_id, self.jama_api_client_secret), oauth=True)
        self.assertFalse(self.jama_client.is_authenticated())
