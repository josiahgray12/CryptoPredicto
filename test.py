from bitcoin.rpc import RawProxy
import pprint

p = RawProxy()

rawT = p.getrawtransaction("1c03c65d2a9f744c8b3ca5fe93096924b880c8ac10dbebf59531f5497bcb6eaa")

decoded_rawT = p.decoderawtransaction(rawT)

#goes through transactions and creates a list of dictionaries where each
#dictionary has the txid and vout# of each input
inputDict = {}
for x in decoded_rawT['vin']:
    inputDict[x['txid']] = x['vout']

ADDLIST = []
#goes through inputDict, and adds the addresses to ADDLIST
for key in inputDict:
    newAdd = findAddress(inputDict[key], key)
    if newAdd not in ADDLIST:
        ADDLIST.append(newAdd)

pprint.pprint(ADDLIST)