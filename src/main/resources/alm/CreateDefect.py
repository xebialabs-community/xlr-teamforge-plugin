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
import ast
from java.util import Calendar
import json

cookies = ast.literal_eval(cookies)
alm_client = almClientUtil.create_alm_client(server, cookies = cookies)
content = {
    "data": [
        {
            "type": "defect",
            "name": title,
            "description": description,
            "severity": severity,
            "detected-by": detectedBy,
            "creation-time": "%s-%s-%s" % (
                str(Calendar.getInstance().get(Calendar.YEAR)),
                str(Calendar.getInstance().get(Calendar.MONTH)+1),  # zero indexed
                str(Calendar.getInstance().get(Calendar.DAY_OF_MONTH))
            )
        }
    ]
}
for additionalField in additionalFields.keys():
    content["data"][0][additionalField] = additionalFields[additionalField]
print json.dumps(content)
result = alm_client.create_defect(domain, project, json.dumps(content))
defectId = result["data"][0]["id"]
output = json.dumps(result)
print "Successfully created a defect with id [ %s ]" % defectId
