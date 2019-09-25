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
import json, ast
cookies = ast.literal_eval(cookies)
alm_client = almClientUtil.create_alm_client(server, cookies = cookies)
content = '''
{
    "data": [
        {
            "type": "defect",
            "name": "%s",
            "description": "%s",
            "priority": "%s",
            "detected-by": "xl-release",
            "severity": "%s"
        }
    ]
}
''' % (title, description, priority, severity)
result = alm_client.create_defect(domain, project, content)
defectId = result['id']
output = json.dumps(result)
print "Successfully created a defect with id [ %s ]" % result['id']
