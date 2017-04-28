#!/usr/bin/env python
"""
Get data sankey:
Takes a parameter that is the name of the AWS profile to use.
Default profile is 'default'.
"""

import boto3
import re
import sys

profilename = 'default'
if len(sys.argv) == 2:
    profilename = sys.argv[1]
    print("Setting profilename to ", profilename)


sourcedatafile = open('sourcedata-output.json', 'w+')
inuser = boto3.session.Session(profile_name=profilename)
client = inuser.client('cloudformation')
response = client.list_exports()
l = response.get('Exports', {})
sourcedatafile.write('{ "links": [')
output1 = []
for x in l:
    s = x['ExportingStackId']
    t = x["Name"]
    o1 = str('{"source":"' + re.search('.*/(.*)/.*', s).group(1) + '","target":"' + t + '","value":"1.0"}')
    output1.append(o1)
    try:
        if client.list_imports(ExportName=t):
            cl = client.list_imports(ExportName=t)
            im = cl["Imports"]
            for x in im:
                o2 = str('{"source":"' + t + '","target":"' + x + '","value":"1.0"}')
                output1.append(o2)
    except:
        pass
sourcedatafile.write(",\n".join(output1))
sourcedatafile.write('], "nodes": [')
output2 = []
for x in l:
    s = x['ExportingStackId']
    o1 = str('{"name":"' + re.search('.*/(.*)/.*', s).group(1) + '"}')
    output2.append(o1)
for x in l:
    o2 = str('{"name":"' + x["Name"] + '"}')
    output2.append(o2)
    t = x["Name"]
    try:
        if client.list_imports(ExportName=t):
            cl = client.list_imports(ExportName=t)
            im = cl["Imports"]
            for z in im:
                o3 = str('{"name":"' + z + '"}')
                output2.append(o3)
    except:
        pass
sourcedatafile.write(",\n".join(list(set(output2))))
sourcedatafile.write(']}')
sourcedatafile.close()
