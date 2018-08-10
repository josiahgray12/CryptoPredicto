#!/usr/bin/python

import simplejson as json
import subprocess
from decimal import Decimal
import re
import os
import pprint
import time

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
                        return ((x['scriptPubKey'])['addresses'])[0]
        return "not there srry"

#goes through a list of transactions and checks if the transaction contains addresses from a passed list
#if it does then it adds the transaction to a new list to return
#parameters: exchaddr - a list containing all the addresses associated to an exchange
def findTxidsOfInterest(exchaddr):

        end = time.clock() + 10
        mempool = set()
        while time.clock() < end:
                mempoolList = json_from_bitcoin_cli('getrawmempool')
                for x in mempoolList:
                        mempool.add(x)
                time.sleep(0.5)

        returnList = []

        for x in mempool:
                #saves into a dictionary the input informaton from a transaction; in the format 'txid':'output#'
                inputDict ={}
                rawT = json_from_bitcoin_cli('getrawtransaction', x, 'true')
                for x in rawT['vin']:
                        if x['txid'] not in inputDict and x['txid'] != x['vout']:
                                inputDict[x['txid']] = x['vout']
                
                addsInvolved = []
                #adds input addresses to the list of addresses involved
                for key in inputDict:
                        newAdd = findAddress(inputDict[key], key)
                        addsInvolved.append(newAdd)

                #add output addresses to the addsInvolvedList
                for x in rawT['vout']:
                        if 'addresses' in x['scriptPubKey']:
                                addsInvolved.append(((x['scriptPubKey'])['addresses'])[0])

                #if addsInvolved contains addresses from exchaddr add it to a new list to be returned later
                if not set(exchaddr).isdisjoint(set(addsInvolved)):
                        returnList.append(x)
        return returnList

#returns address correspoinding to the vout# of that txid passed and the amount of coin in a list
def findAddressAndAmmount(vout, txid):
        rawT = json_from_bitcoin_cli('getrawtransaction', txid, 'true')

        retList = []
                
        for x in rawT['vout']:
                if x['n'] == vout:
                        retList.append(((x['scriptPubKey'])['addresses'])[0])
                        retList.append(x['value'])
                        return retList
        retList = ["NA", 0]
        return retList


#parameters: txids - a list of transactions to analyze
#prints an analysis of the transaction
def analyzeTxidsOfInterest(txids):

        for x in txids:
                #saves into a dictionary the input informaton from a transaction; in the format 'txid':'output#'
                inputDict ={}
                rawT = json_from_bitcoin_cli('getrawtransaction', x, 'true')
                #if txid not already recorded 
                if (rawT['vin'])['txid'] not in inputDict:
                        inputDict[(rawT['vin'])['txid']] = (rawT['vin'])['vout']
                
                addsInvolved = {}
                #adds input addresses to dictionary with format address:amount
                for key in inputDict:
                        info = findAddressAndAmmount(inputDict[key], key)
                        addsInvolved[info[0]] = info[1]

                #add output addresses to the addsInvolvedList
                for y in rawT['vout']:
                        if 'addresses' in y['scriptPubKey']:
                                addsInvolved[((y['scriptPubKey'])['addresses'])[0]] = -(y['value'])

                #print info, output amounts displayed as negative
                pprint.pprint(addsInvolved)


##input file name for address grouping that you are intersted in
file = open("GDAXONEFILE.txt", "r")
exchADDSDraft = file.readlines()
exchADDS = []
#this part simply goes through and removes the group headers, and the empty lines
#or, more accurately, adds the lines that are not headers or blanks to a new list
for x in exchADDSDraft:
    if "Page" not in x and x != "\n":
        exchADDS.append(x)

relevantTxids = findTxidsOfInterest(exchADDS)

analyzeTxidsOfInterest(relevantTxids)

pprint.pprint(relevantTxids)

