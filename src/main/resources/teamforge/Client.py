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
import json
import org.slf4j.LoggerFactory as LoggerFactory

logger = LoggerFactory.getLogger("Teamforge")


def getTeamforgeAuthToken(serverParams):
    # setup the request url
    api_token_endpoint = "/oauth/auth/token"
    url = serverParams.get('url') + "%s" % api_token_endpoint
    scope = "scope=urn:ctf:services:ctf urn:ctf:services:svn urn:ctf:services:gerrit urn:ctf:services:soap60"
    grant_type = "grant_type=password"
    client_id = "client_id=api-client"
    username = "username=%s" % serverParams.get('username')
    password = "password=%s" % serverParams.get('password')

    # setup the request payload and headers
    payload = grant_type + "&" + username + "&" + password + "&" + client_id + "&" + scope
    headers = {
        'Content-Type': "application/x-www-form-urlencoded"
    }

    # send post request to services/oauth2/token endpoint
    r = requests.post(url, data=payload, headers=headers, verify=False)

    # check for good response
    if r.status_code != 200:
        raise Exception(
            "Error retrieving authorization token from TeamForge Server. Reason: %s" % r.reason
        )
    else:
        return r


def getArtifactDetails(serverParams, artifactId):
    authToken = getTeamforgeAuthToken(serverParams)
    rest_api_endpoint = "/ctfrest/tracker/v1/artifacts/%s" % artifactId
    api_url = serverParams.get('url') + "%s" % rest_api_endpoint

    # set the auth string to the header
    headers = {"Accept": "application/json", "Authorization": createAuthString(authToken)}
    data = {}

    # make the request get call
    api_response = requests.get(api_url, headers=headers, data=data, verify=False)

    # handle our response
    if api_response.status_code != 200:
        raise Exception(
            "Error retrieving artifact details from TeamForge Server. Reason: %s" % api_response.reason
        )
    else:
        data = json.loads(api_response.content)
        return parseApiResponse(data)


def getArtifactChildren(serverParams, parentArtifactId):
    authToken = getTeamforgeAuthToken(serverParams)
    rest_api_endpoint = "/ctfrest/tracker/v1/artifacts/%s" % parentArtifactId
    rest_api_endpoint = rest_api_endpoint + "/dependencies/children"
    api_url = serverParams.get('url') + "%s" % rest_api_endpoint

    # set the auth string to the header
    headers = {"Accept": "application/json", "Authorization": createAuthString(authToken)}
    data = {}

    # make the request get call
    api_response = requests.get(api_url, headers=headers, data=data, verify=False)

    # handle our response
    if api_response.status_code != 200:
        raise Exception(
            "Error retrieving artifact details from TeamForge Server. Reason: %s" % api_response.reason
        )
    else:
        data = json.loads(api_response.content)
        childrenArtifactIds = []
        for key in data:
            if key == "items":
                logger.error('in my items key')
                for subKey in data['items']:
                    logger.error('in my loop, my child artifactId is: %s' % subKey['id'])
                    childrenArtifactIds += [subKey['id']]
        logger.error('my value for childrenArtifactIds is: %s' % childrenArtifactIds)
        return childrenArtifactIds


def getAssociations(serverParams, objectId):
    authToken = getTeamforgeAuthToken(serverParams)
    rest_api_endpoint = "/ctfrest/foundation/v1/objects/%s" % objectId
    rest_api_endpoint = rest_api_endpoint + "/associations?depth=0&includeDependencies=false&includeEvents=true&includePhantoms=false&limit=0"
    api_url = serverParams.get('url') + "%s" % rest_api_endpoint

    # set the auth string to the header
    headers = {"Accept": "application/json", "Authorization": createAuthString(authToken)}
    data = {}

    # make the request get call
    api_response = requests.get(api_url, headers=headers, data=data, verify=False)

    # handle our response
    if api_response.status_code != 200:
        raise Exception(
            "Error retrieving object association from TeamForge Server. Reason: %s" % api_response.reason
        )
    else:
        data = json.loads(api_response.content)
        return parseApiResponse(data)


def createAssociations(serverParams, objectIds, targetId):
    authToken = getTeamforgeAuthToken(serverParams)
    for objectId in objectIds:
        rest_api_endpoint = "/ctfrest/foundation/v1/objects/%s" % objectId
        rest_api_endpoint = rest_api_endpoint + "/associations/%s" % targetId
        api_url = serverParams.get('url') + "%s" % rest_api_endpoint

        # set the auth string to the header
        headers = {"Content-Type": "application/json", "Accept": "application/json",
                   "Authorization": createAuthString(authToken)}
        payload = {}

        # make the request put call
        api_response = requests.put(api_url, headers=headers, data=json.dumps(payload), verify=False)

        # handle our response
        if api_response.status_code != 204:
            raise Exception(
                "Error retrieving artifact details from TeamForge Server. Reason: %s" % api_response.reason
            )
    # Now that the association(s) have been made, make a get call for the associations
    return getAssociations(serverParams, targetId)


def createAuthString(authToken):
    payload = authToken.json()
    token_type = payload["token_type"]
    access_token = payload["access_token"]
    authString = token_type + " " + access_token
    return authString


def updateArtifact(serverParams, artifactIds, status, comment):
    data = {}
    for artifactId in artifactIds:
        authToken = getTeamforgeAuthToken(serverParams)
        rest_api_endpoint = "/ctfrest/tracker/v1/artifacts/%s" % artifactId
        api_url = serverParams.get('url') + "%s" % rest_api_endpoint

        # set the auth string to the header
        headers = {"Content-Type": "application/json", "Accept": "application/json", "If-Match": "*",
                   "Authorization": createAuthString(authToken)}
        payload = {'status': status, 'comment': comment}

        # make the request patch call
        api_response = requests.patch(api_url, headers=headers, data=json.dumps(payload), verify=False)

        # handle our response
        if api_response.status_code != 200:
            raise Exception(
                "Error retrieving artifact details from TeamForge Server. Reason: %s" % api_response.reason
            )
        else:
            data = json.loads(api_response.content)

    return parseApiResponse(data)


def parseApiResponse(data):
    flexFields = {}
    fields = {}
    cleanData = cleanNullTerms(data)
    for key in cleanData:
        if key == "flexFields":
            for subKey in cleanData['flexFields']:
                flexFields[subKey['name']] = subKey['values'][0]
        else:
            fields[key] = cleanData[key]
    return fields, flexFields


def cleanNullTerms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None and v != "":
            clean[k] = v
    return clean
