#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from alm.almClientUtil import almClientUtil

if not almServer:
    raise Exception("ALM server ID must be provided")

def get_row_data(item):
    row_map = {}
    for field in test_instance['Fields']:
        row_map[field['Name']] = field['values'][0]['value']
    return row_map

print "Performing Login"
alm_client = almClientUtil.create_alm_client(almServer, username, password)
result = alm_client.login()
print "Setting cookies and making call to query for release cycle"
alm_client = almClientUtil.create_alm_client(almServer, cookies=result.get_dict())
test_sets = alm_client.query_status(domain, project,"test-sets", query)
rows= {}
print "Now finding test intsances under each test set"
for item in test_sets['entities']:
    testset_id = item['Fields'][0]['values'][0]['value']
    test_instances = alm_client.query_status(domain, project,"test-instances", "{test-set.id[%s]}&fields=id,status,name,owner" % testset_id)
    for test_instance in test_instances['entities']:
        test_instance_obj = get_row_data(test_instance)
        rows[test_instance_obj['id']] = test_instance_obj

data = rows
