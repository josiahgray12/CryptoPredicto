import pprint
from findInput.py import bitcion_cli

exchGroupings = {}

dictWithOneAddressForEachExchange = {'Exch1':'Add1', 'Exch2':'Add2', 'Exch3':'Add3'}

specialAdd = "this will be a bitcoin address"
specialGroup = []
specialName = "ExchName"

for key, value in dictWithOneAddressForEachExchange:
    groupsJson = bitcoin_cli.json_from_bitcoin_cli('listAddressGroupings')
    data = json.load(groupJson)
    for x in data:
        if value in x:
            specialGroup = x
    exchGroupings[key] = specialGroup

