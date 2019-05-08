#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests, sys, traceback
from requests.auth import HTTPBasicAuth

class HttpClient(object):
    def __init__(self, http_connection, username=None, password=None, authheaders= {}, cookies={}, pass_auth_after_login = True):
        self.http_connection = http_connection
        self.url = http_connection['url']
        self.username = username if username else http_connection['username']
        self.password = password if password else http_connection['password']
        self.proxy = None
        self.auth_mode = http_connection['authenticationMethod']
        if http_connection['proxyHost']:
            self.proxy = {'http': '%s:%s' % (
                http_connection['proxyHost'], http_connection['proxyPort'])}
        self.verify_ssl = http_connection['enableSslVerification']
        self.authheaders = authheaders
        self.cookies = cookies
        self.pass_auth_after_login = pass_auth_after_login

    def get(self, context_root, content=None, headers={}, cookies = {}):
    	if (self.cookies or self.authheaders) and not self.pass_auth_after_login :
    		auth=None
    	else:
    		auth=(self.username, self.password)
    	cookies.update(self.cookies)
    	headers.update(self.authheaders)
        request_url = self.url + context_root
        response = None
        try:
        	response = requests.get(request_url, auth=auth, params = content, headers = headers,
                            proxies = self.proxy, verify = self.verify_ssl, cookies = cookies)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise Exception(exc_value)

        if response.raise_for_status():
            reason = "Unknown"
            if response.status == 400:
                reason = "Bad request"
            elif response.status == 401:
                reason = "Unauthorized"
            elif response.status == 403:
                reason = "Forbidden"
            raise Exception("HTTP response code %s (%s), message : %s" % (response.status, reason,response.getResponse()))
        return response

    def post(self, context_root, content="", headers = {}, cookies = {}):
    	if (self.cookies or self.authheaders) and not self.pass_auth_after_login :
    		auth=None
    	else:
    		auth=(self.username, self.password)
    	cookies.update(self.cookies)
    	headers.update(self.authheaders)    	
        request_url=self.url + context_root     
        try:
        	response = requests.post(request_url, auth=auth, headers = headers,
                             proxies = self.proxy, verify = self.verify_ssl, data = content , cookies = cookies)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise Exception(exc_value)

        if response.raise_for_status():
            reason = "Unknown"
            if response.status == 400:
                reason = "Bad request"
            elif response.status == 401:
                reason = "Unauthorized"
            elif response.status == 403:
                reason = "Forbidden"
            raise Exception("HTTP response code %s (%s), message : %s" % (response.status, reason,response.getResponse()))
        return response

    def put(self, context_root, content="", headers = {}, cookies = {}):
    	if (self.cookies or self.authheaders) and not self.pass_auth_after_login :
    		auth=None
    	else:
    		auth=(self.username, self.password)
    	cookies.update(self.cookies)
    	headers.update(self.authheaders)
        request_url=self.url + context_root
        try:
        	response = requests.put(request_url, auth=auth, headers = headers,
                            proxies = self.proxy, verify = self.verify_ssl, data = content, cookies = cookies)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise Exception(exc_value)

        if response.raise_for_status():
            reason = "Unknown"
            if response.status == 400:
                reason = "Bad request"
            elif response.status == 401:
                reason = "Unauthorized"
            elif response.status == 403:
                reason = "Forbidden"
            raise Exception("HTTP response code %s (%s), message : %s" % (response.status, reason,response.getResponse()))
        return response

    def delete(self, context_root, headers = {}, cookies = {}):
    	if (self.cookies or self.authheaders) and not self.pass_auth_after_login :
    		auth=None
    	else:
    		auth=(self.username, self.password)
    	cookies.update(self.cookies)
    	headers.update(self.authheaders)
        request_url=self.url + context_root
        try:
        	response = requests.delete(request_url, auth=auth, headers = headers,
                               proxies = self.proxy, verify = self.verify_ssl, cookies = cookies)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise Exception(exc_value)

        if response.raise_for_status():
            reason = "Unknown"
            if response.status == 400:
                reason = "Bad request"
            elif response.status == 401:
                reason = "Unauthorized"
            elif response.status == 403:
                reason = "Forbidden"
            raise Exception("HTTP response code %s (%s), message : %s" % (response.status, reason,response.getResponse()))
        return response
