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
import json

alm_client = almClientUtil.create_alm_client(almServer, username, password)
cookies = alm_client.login()
alm_client = almClientUtil.create_alm_client(almServer, cookies=cookies.get_dict())

instances = alm_client.query_status(domain, project, resource, query, list(fields))

# Note the exclusive use of lists (as opposed to the more intuitive dict) - used to retain ordering (important for detail view)
rows = []
for instance in instances:
    row = []
    for field in list(fields):
        row.append([field, instance[field]])
    rows.append(row)

for val in rows[0]:
    if val[0] == categorizeBy:
        categorizeByIndex = rows[0].index(val)

instance_totals = {}
for row in rows:
    category = row[categorizeByIndex][1]
    if category is None:
        category = "Undefined"
    if category not in instance_totals.keys():
        instance_totals[category] = 1
    else:
        instance_totals[category] += 1

data = {
    "categories": instance_totals.keys(),
    "instance_totals": [{"name": category, "value": instance_totals[category]} for category in instance_totals.keys()],
    "rows": rows
}

logout = alm_client.logout()
