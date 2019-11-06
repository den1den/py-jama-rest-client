from py_jama_rest_client.client import JamaClient
from py_jama_rest_client.core import Core


class CountedJamaCore(Core):
    def __init__(self, host_name, user_credentials, api_version='/rest/v1/', oauth=False):
        super().__init__(host_name, user_credentials, api_version, oauth)
        self.gets = 0

    def get(self, resource, params=None, **kwargs):
        self.gets += 1
        return super().get(resource, params, **kwargs)


class CountedJamaClient(JamaClient):

    def __init__(self, host_domain, credentials=('username|clientID', 'password|clientSecret'), api_version='/rest/v1/',
                 oauth=False):
        super().__init__(host_domain, credentials, api_version, oauth)
        self._JamaClient__core = CountedJamaCore(host_domain, credentials, api_version=api_version, oauth=oauth)
        self.core = self._JamaClient__core
