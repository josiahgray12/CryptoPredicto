import subprocess
import time
import json

# Helper to run bitcoin-cli
def bitcoin_cli(*args):
    cmd = ['bitcoin-cli']
    cmd.extend(args)
    return subprocess.run(cmd, universal_newlines=True, stdout=subprocess.PIPE)


# Helper to run bitcoin-cli, which shouldn't fail.  Returns stdout.
def bitcoin_cli_nofail(*args):
    cmd=['bitcoin-cli']
    cmd.extend(args)
    return subprocess.run(cmd, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout


# Helper to run bitcoin-cli, which shouldn't fail.  Returns stdout, \n removed.
def bitcoin_cli_simple(*args):
    return bitcoin_cli_nofail(*args).rstrip()


# Helper to parse bitcoin-cli output as JSON.
def json_from_bitcoin_cli(*args):
    return json.loads(bitcoin_cli_nofail(*args))


def get_mem_pool_amounts():
    end = time.clock() + 10
    # set to avoid duplicates
    test_set = set()
    index = 0
    while time.clock() < end:
        txs = json_from_bitcoin_cli('getrawmempool')
        for tx in txs:
            test_set.add(tx)
            if len(test_set) > index:
                raw_tx = bitcoin_cli_simple('getrawtransaction', tx)
                decoded_tx = json_from_bitcoin_cli('decoderawtransaction', raw_tx)
                if len(decoded_tx['vout']) > 1:
                    amount = decoded_tx['vout'][1]['value']
                    if 'addresses' in decoded_tx['vout'][1]['scriptPubKey']:
                        addr = decoded_tx['vout'][1]['scriptPubKey']['addresses'][0]
                    else:
                        addr = 'N/A'
                else:
                    amount = 0
                    addr = "N/A"

                print('{} : {}'.format(amount, addr))
                index = index+1

        time.sleep(0.5)


def main():
    get_mem_pool_amounts()


if __name__ == "__main__":
    main()