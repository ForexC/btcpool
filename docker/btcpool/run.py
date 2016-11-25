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
    if '__' not in k:
        conf[k] = v
        continue
    k1, k2 = k.split('__', 1)
    if k1 not in conf:
        conf[k1] = {}
    conf[k1][k2] = v


def write_line(f, k, v):
    if v in ['true', 'false']:
        f.write("%s = %s;\n"%(k, v))
        return
    try:
        v = int(v)
        f.write("%s = %d;\n"%(k, v))
    except ValueError:
        f.write("%s = \"%s\";\n"%(k, v))


with open(conf_file, 'w+') as f:
    for k1, v1 in conf.iteritems():
        if not isinstance(v1, dict):
            write_line(f, k1, v1)
            continue
        f.write("%s = {\n"%k1)
        for k2, v2 in v1.iteritems():
            write_line(f, k2, v2)
        f.write("};\n\n")

# Execute the component
os.system("%s -c %s -l %s"%(bin_file, conf_file, log_dir))
