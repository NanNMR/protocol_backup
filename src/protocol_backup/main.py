#!/usr/bin/env python3
import argparse
import logging

import yaml

from protocol_backup import backup_logger
from protocolbackup import BackupProtocols

#
# Fetch command line driver
#


logging.basicConfig()
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('yaml', help="Configuration file")
parser.add_argument('-l', '--loglevel', default='WARN', help="Python log level")
args = parser.parse_args()
backup_logger.setLevel(getattr(logging, args.loglevel))
with open(args.yaml) as f:
    config = yaml.safe_load((f))
bp = BackupProtocols(config)
bp.workspace_protocols()
