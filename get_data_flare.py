#!/usr/bin/env python
"""
Get the flare data:
Takes a parameter that is the name of the AWS profile to use.
Default profile is 'default'.
"""

import boto3
import re
import os
import sys

profilename = 'default'
if len(sys.argv) == 2:
    profilename = sys.argv[1]
    print('-- Using %(profile)s profile --' % {'profile': profilename})
else:
    print("-- Using 'default' profile --")

inuser = boto3.session.Session(profile_name=profilename)
client = inuser.client('cloudformation')
response = client.list_exports()
tempfile = open('temp.in', 'w+')
l = response.get('Exports', {})
tempfile.write('id,value\n')
tempfile.write('Templates,\n')
for x in l:
    stackARN = x['ExportingStackId']
    exportedVariableName = x["Name"]
    print('Stack ARN: %(stackId)s' % {'stackId': stackARN})
    print('Export Name: %(stackName)s' % {'stackName': exportedVariableName})
    tempfile.write('.'.join(['Templates',
                             re.search('.*/(.*)/.*', stackARN).group(1), exportedVariableName]) + ',\n')
    # print ('.'.join(['Templates',
    #                  re.search('.*/(.*)/.*', stackARN).group(1), exportedVariableName]) + ',\n')
    j = re.search('.*/(.*)/.*', stackARN).group(1)
    tempfile.write('.'.join(['Templates', j]) + ',\n')
    # print('.'.join(['Templates', j]) + ',')
    try:
        if client.list_imports(ExportName=exportedVariableName):
            cl = client.list_imports(ExportName=exportedVariableName)
            im = cl["Imports"]
            for x in im:
                print >> tempfile, '.'.join(['Templates', j, exportedVariableName, x]) + ','
    except:
        pass
tempfile.close()

lines_seen = set()
outfile = open('flare.csv', "w")
for line in open('temp.in', "r"):
    if line not in lines_seen:  # not a duplicate
        outfile.write(line)
        lines_seen.add(line)
outfile.close()

os.remove('temp.in')
