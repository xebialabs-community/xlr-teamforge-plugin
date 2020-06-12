#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests
import org.slf4j.LoggerFactory as LoggerFactory

logger = LoggerFactory.getLogger("Teamforge")

# New Teamforge logic
# setup the request url
api_token_endpoint = "/oauth/auth/token"
url = configuration.url + "%s" % api_token_endpoint
scope="scope=urn:ctf:services:ctf urn:ctf:services:svn urn:ctf:services:gerrit urn:ctf:services:soap60"
grant_type = "grant_type=password"
client_id = "client_id=api-client"
username = "username=%s" % configuration.username
password = "password=%s" % configuration.password

# setup the request payload and headers
payload = grant_type + "&" + username + "&" + password + "&" + client_id + "&" + scope
headers = {
    'Content-Type': "application/x-www-form-urlencoded"
}

# send post request to services/oauth2/token endpoint
logger.error('Testing the Teamforge Server configuration...')
logger.error('Oauth2 url address is %s' % url)
logger.error('username: %s' % configuration.username)
logger.error('password: %s' % configuration.password)
logger.error('payload: %s' % payload)
logger.error('right before my actual request call')
r = requests.post(url, data=payload, headers=headers, verify=False)

logger.error('after post call - request call was successful.')

# check for good response
logger.info('Http Response code is %s' % r.status_code)
if r.status_code != 200:
    logger.error('response error code: %s' % r.status_code)
    logger.error('response error reason: %s' % r.reason)
    raise Exception(
        "Failed to connect to TeamForge Server. Reason: %s" % r.reason
    )
else:
    logger.error('Teamforge auth token: %s' % r.text)