#!/usr/bin/python

from __future__ import print_function

import os
import sys
import argparse
import json

components = ['gbtmaker', 'blkmaker', 'jobmaker',
              'poolwatcher', 'sharelogger', 'sserver',
              'slparser', 'statshttpd',]

# Initiate the directories path
conf_dir  = os.path.join(os.path.dirname('/opt/btcpool/'), 'conf')
log_dir  = os.path.join(os.path.dirname('/opt/btcpool/'), 'log')
bin_dir  = os.path.dirname('/usr/local/bin/')

# Get the component name
parser = argparse.ArgumentParser(description='Start a btcpool component')
def btcpool_component(value):
    value = str(value)
    if value not in components:
         raise argparse.ArgumentTypeError("%s is not a btcpool component" % value)
    return value
parser.add_argument('component', type=btcpool_component, nargs=1,
                    help='the btcpool component to run')
args = parser.parse_args()

bin_name = args.component[0]
bin_file = os.path.join(bin_dir, bin_name)
conf_file = os.path.join(conf_dir, '%s.cfg'%bin_name)

# Generate config file from enviroment variables
conf = {}
for k,v in os.environ.iteritems():
    if not k.startswith(bin_name.upper()):
        continue
    k = k[len(bin_name)+1:].lower()
    k1, k2 = k.split('_', 1)
    if k1 not in conf:
        conf[k1] = {}
    conf[k1][k2] = v

with open(conf_file, 'w+') as f:
    for k1, d in conf.iteritems():
        f.write("%s = {\n"%k1)
        for k2, v in d.iteritems():
            if v in ['true', 'false']:
                f.write("\t%s = %s;\n"%(k2, v))
                continue
            try:
                v = int(v)
                f.write("\t%s = %d;\n"%(k2, v))
            except ValueError:
                f.write("\t%s = \"%s\";\n"%(k2, v))
        f.write("};\n\n")

# Execute the component
os.system("%s -c %s -l %s"%(bin_file, conf_file, log_dir))
