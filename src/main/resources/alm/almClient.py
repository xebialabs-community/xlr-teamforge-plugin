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

    def get_context(self, resource):
        context = {
            "defects": "api",
            "attachments": "api",
            "list-items": "api",
            "test-set-folders": "rest",
            "test-sets": "rest",
            "test-instances": "rest",
            "tests": "rest",
            "runs": "rest"
        }
        context_parameters = {
            "rest": {
                "name": "rest",
                "query_delimiters": ["{", "}"],
                "data_key": "entities",
                "unwrap": True,
                "limit_key": "page-size",
                "start_key": "start-index",
                "start_num": 1
            },
            "api": {
                "name": "api",
                "query_delimiters": ["\"", "\""],
                "data_key": "data",
                "unwrap": False,
                "limit_key": "limit",
                "start_key": "offset",
                "start_num": 0
            }
        }
        current_context = context[resource]
        return context_parameters[current_context]

    def unwrap_data(self, entities):
        data = []
        for entity in entities:
            key_value_pairs = {}
            for field in entity["Fields"]:
                if len(field["values"]) == 1:
                    key_value_pairs[field["Name"]] = field["values"][0]["value"]
            data.append(key_value_pairs)
        return data

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
        api_url = "/qcbin/api/domains/%s/projects/%s/defects" % (domain, project)
        api_response = self.http_request.post(api_url, headers={"Content-Type":"application/json", "Accept":"application/json"}, content = content)
        return api_response.json()

    def update_defect(self, domain, project, defid, content):
        api_url = "/qcbin/api/domains/%s/projects/%s/defects/%s" % (domain, project, defid)
        api_response = self.http_request.put(api_url, headers={"Content-Type":"application/json", "Accept":"application/json"}, content = content)
        return api_response.json()

    def read_defect(self, domain, project, defid):
        api_url = "/qcbin/api/domains/%s/projects/%s/defects/%s" % (domain, project, defid)
        api_response = self.http_request.get(api_url, headers={"Content-Type":"application/json", "Accept":"application/json"})
        return api_response.json()

    def delete_defect(self, domain, project, defid):
        api_url = "/qcbin/api/domains/%s/projects/%s/defects/%s" % (domain, project, defid)
        api_response = self.http_request.delete(api_url, headers={"Content-Type":"text/plain", "Accept":"application/json"})
        return api_response.json()

    def query_status(self, domain, project, resource, query, fields):
        context = self.get_context(resource)
        results_per_page = 50
        keep_paging = True
        page = 0
        results = []
        while keep_paging:
            api_url = "/qcbin/%s/domains/%s/projects/%s/%s?" % (
                context["name"],
                domain,
                project,
                resource
            )
            api_url += "query=%s%s%s&fields=%s&%s=%s&%s=%s" % (
                context["query_delimiters"][0],
                query,
                context["query_delimiters"][1],
                ",".join(fields),
                context["limit_key"],
                results_per_page,
                context["start_key"],
                page*results_per_page+context["start_num"]
            )
            api_response = self.http_request.get(api_url, headers={"Content-Type":"application/json", "Accept":"application/json"})
            results_page = api_response.json()[context["data_key"]]
            if results_page == []:
                keep_paging = False
            elif context["unwrap"]:
                results += self.unwrap_data(results_page)
            else:
                results += results_page
            page += 1
        return results
