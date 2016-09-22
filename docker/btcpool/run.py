#!/usr/bin/python

from __future__ import print_function

import os
import sys
import argparse

components = ['gbtmaker', 'blkmaker', 'jobmaker',
              'poolwatcher', 'sharelogger', 'sserver',
              'slparser', 'statshttpd',]

conf_dir  = os.path.join(os.path.dirname('/opt/btcpool/'), 'conf')
log_dir  = os.path.join(os.path.dirname('/opt/btcpool/'), 'log')
bin_dir  = os.path.dirname('/usr/local/bin/')

def btcpool_component(value):
    value = str(value)
    if value not in components:
         raise argparse.ArgumentTypeError("%s is not a btcpool component" % value)
    return value

parser = argparse.ArgumentParser(description='Start a btcpool component')
parser.add_argument('component', type=btcpool_component, nargs=1,
                    help='the btcpool component to run')
args = parser.parse_args()

bin_name = args.component[0]
bin_file = os.path.join(bin_dir, bin_name)
conf_file = os.path.join(conf_dir, '%s.cfg'%bin_name)

os.system("%s -c %s -l %s"%(bin_file, conf_file, log_dir))
