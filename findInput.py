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

#returns output number vout from txid txid
def findAddress(vout, txid):
        rawT = json_from_bitcoin_cli('getrawtransaction', txid, 'true')
                
        for x in rawT['vout']:
                if x['n'] == vout:
                        return (x['scriptPubKey'])['addresses']
        return "not there srry"


#saves into a dictionary the input informaton from a transaction; in the format 'txid':'output#'
rawT = json_from_bitcoin_cli('getrawtransaction', 'b4df8f5bf75c52910db5e6af007e783d5c8dc892ab212b84e129543e6ecc8b30', 'true')
inputDic = {}
for x in rawT['vin']:
        inputDic[x['txid']] = x['vout']
print(inputDic)

#adds a watch only address to your bitcoin system, which allows all transactions involving that address to be listed
bitcoin_cli('importaddress', 'mxA6NXJMsTxWpVVxraSgni3u9w4teUQteK', '"watchonly1"', 'false' )

#adds the txids of your watch only addresses where the address was used as an input
transactions = []
transactionList = json_from_bitcoin_cli('listtransactions', '*', '999999999', '0', 'true')
for x in transactionList:
        if x['category'] == "send":
                transactions.append(x['txid'])

pprint.pprint(set(transactions))
        
print(findAddress(2, 'ac8cd50671b871dbd02cf5a2d5fdd3d8b7119c2aae46e21695fb03b12895c4c8'))

        

