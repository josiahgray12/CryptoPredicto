#!/usr/bin/python

import simplejson as json
import subprocess
from decimal import Decimal
import re
import os
import pprint

BITCOIN_ERROR_RE = re.compile('error code: (?P<code>-?[0-9]+)\nerror message:\n(?P<message>.*)\n')

class BitcoinException(Exception):
        def __init__(self, message, stdout, stderr, code=None):
               super(BitcoinException, self).__init__(message)
               self.stdout = stdout
               self.stderr = stderr
               self.code = code



#dictionary to hold the clusters
CLUSTERDICT = {}

# Helper to run bitcoin-cli.  Returns stdout.
def bitcoin_cli(*args):
        cmd=['bitcoin-cli']
        cmd.extend(args)
        p = subprocess.Popen(cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode == 0:
                return stdout
        else:
                # we should have something interesting in stderr - try to parse it
                match = re.match(BITCOIN_ERROR_RE, stderr)
                if match:
                        raise BitcoinException(match.group('message'), stdout, stderr, match.group('code'))
                else:
                        raise BitcoinException('Unknown Bitcoin exception occurred', stdout, stderr)

# Helper to parse bitcoin-cli output as JSON.
def json_from_bitcoin_cli(*args):
        return json.loads(bitcoin_cli(*args), parse_float=Decimal)


