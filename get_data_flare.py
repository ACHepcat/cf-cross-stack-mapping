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
    print("Setting profilename to ", profilename)

inuser = boto3.session.Session(profile_name=profilename)
client = inuser.client('cloudformation')
response = client.list_exports()
tempfile = open('temp.in', 'w+')
l = response.get('Exports', {})
tempfile.write('id,value\n')
tempfile.write('Templates,\n')
for x in l:
    s = x['ExportingStackId']
    t = x["Name"]
    print(s)
    print(t)
    tempfile.write('.'.join(['Templates',
                             re.search('.*/(.*)/.*', s).group(1), t]) + ',\n')
    print ('.'.join(['Templates',
                     re.search('.*/(.*)/.*', s).group(1), t]) + ',\n')
    j = re.search('.*/(.*)/.*', s).group(1)
    tempfile.write('.'.join(['Templates', j]) + ',')
    print('.'.join(['Templates', j]) + ',')
    try:
        if client.list_imports(ExportName=t):
            cl = client.list_imports(ExportName=t)
            im = cl["Imports"]
            for x in im:
                print >>tempfile, '.'.join(['Templates', j, t, x]) + ','
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
