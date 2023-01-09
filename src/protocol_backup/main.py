#!/usr/bin/env python3
import argparse
import logging
import sys
import typing

import yaml

from protocolbackup import BackupProtocols

#
# Fetch command line driver
#


logging.basicConfig()
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('yaml',help="Configuration file")
parser.add_argument('-a', '--authconfig', default='protocolfetch.cfg' ,help="Config info")
args = parser.parse_args()
with open(args.yaml) as f:
    config = yaml.safe_load((f))
bp = BackupProtocols(config)
bp.workspace_protocols()
