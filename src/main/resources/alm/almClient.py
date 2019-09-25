#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import json
from alm.HttpClient import HttpClient

class almClient(object):
    def __init__(self, http_connection, username=None, password=None, authheaders= {}, cookies = {}):
        self.http_request = HttpClient(http_connection, username , password, authheaders, cookies) # Should not have to pass the empty P/W string, will work on fix.

    @staticmethod
    def create_client(http_connection, username=None, password=None, authheaders= {}, cookies = {}):
        return almClient(http_connection, username, password, authheaders, cookies)

    def check_connection(self):
        api_url = "/qcbin"
        return self.http_request.get(api_url)

    def login(self):
        api_url = "/qcbin/api/authentication/sign-in"
        api_response = self.http_request.post(api_url, headers={"Content-Type":"application/json"})
        return api_response.cookies

    def logout(self):
        api_url = "/qcbin/api/authentication/sign-out"
        api_response = self.http_request.get(api_url, headers={"Content-Type":"application/json"})
        return api_response

    def create_defect(self, domain, project, content):
        api_url = "/qcbin/rest/domains/%s/projects/%s/defects" % (domain, project)
        api_response = self.http_request.post(api_url, headers={"Content-Type":"application/json", "Accept":"application/json"}, content = content)
        return api_response.json()

    def update_defect(self, domain, project, defid, content):
        api_url = "/qcbin/rest/domains/%s/projects/%s/defects/%s" % (domain, project, defid)
        api_response = self.http_request.put(api_url, headers={"Content-Type":"application/json", "Accept":"application/json"}, content = content)
        return api_response.json()

    def read_defect(self, domain, project, defid):
        api_url = "/qcbin/rest/domains/%s/projects/%s/defects/%s" % (domain, project, defid)
        api_response = self.http_request.get(api_url, headers={"Content-Type":"application/json", "Accept":"application/json"})
        return api_response.json()

    def delete_defect(self, domain, project, defid):
        api_url = "/qcbin/rest/domains/%s/projects/%s/defects/%s" % (domain, project, defid)
        api_response = self.http_request.delete(api_url, headers={"Content-Type":"text/plain", "Accept":"application/json"})
        return api_response.json()

    def query_status(self, domain, project, resource, query):
        api_url = "/qcbin/rest/domains/%s/projects/%s/%s?query=%s" % (domain, project, resource, query)
        api_response = self.http_request.get(api_url, headers={"Content-Type":"application/json", "Accept":"application/json"})
        return api_response.json()
