import os
import simplejson as json
import subprocess
import pprint
from findinput.py import bitcoin_cli

rawT = bitcoin_cli.json_from_bitcoin_cli('getrawtransaction f5041e49e6e1a246c637e711a029986dc2878977d8a2fe370adde1a58f75148b')
pprint(rawT)