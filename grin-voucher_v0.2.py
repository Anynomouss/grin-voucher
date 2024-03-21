# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:57:49 2024
@author: Anynomous
Licence: Apache v2.0.
Dislaimer
WARNINGs: 
    -This tool is best adviced to be run in a secure environment since vouchers are by default not encrypted with a password.
    -Vouchers should not be used for any amount of Grin with significant value. 
    -Grin vouchers can be used to as two step transaction method, but do not generate
    payment proofs and as such should be only be used when the sender 100% accepts
    the receiver gains 100% control over the funds in the vouchers without any way 
    to settle disputes. 
    
PROCEDURE
    ITERATIVEY: for each wallets/vouchers, do the following:
1) Create a wallet using mimblewimble-py, 
2) Innitiate a SRS transaction through the grin-wallet API -> grinmw library
3) Sign the transaction using the voucher wallet, - >  mimblewimble-py library
4) Sign with grin-wallet using the API (grinmw library) and finalize/broadcast the transaction
5) Create output wallet backup in the log file and generate the vouchers
"""



## Dependencies, not on linux use pip3 to istall for Python 3
import argparse # pip install argparse
import pprint, os, time
from mimblewimble.wallet import Wallet # pip install mimblewimble

from grinmw.wallet_v3 import WalletV3
import pprint, os
from pathlib import Path
home = str(Path.home())


if __name__ == '__main__':
    ###############################################################################
    ## 0A) Parse command line arguments using arparse
    parser = argparse.ArgumentParser(description = "Grin-voucher command line parser using argparse")
    parser.add_argument("-H", "--Help", help = "Example: Help argument", required = False, default = "")
    parser.add_argument("-n", "--nvouchers", help = "Example: --nvouchers = 10", required = False, default = 1,type=int)
    parser.add_argument("-v", "--value", help = "Example: --value 42.00", required = True, type=float)
    parser.add_argument("-p", "--password", help = "Example: --password mimblewimble", required = True, type=str)
    parser.add_argument("-f", "--feesindcluded", help = "Example: --feesindcluded True", required = False, default = True, type=bool)
    
    argument = parser.parse_args()
    status = False
    
    if argument.Help:
        print("You have used '-H' or '--Help' with argument: {0}".format(argument.Help))
        status = True
    if argument.nvouchers:
        print("You have used '-n' or '--vouchers' with argument: {0}".format(argument.nvouchers))
        status = True
    if argument.end:
        print("You have used '-v' or '--value' with argument: {0}, meaning you want to send that much ツ".format(argument.value))
        status = True
    if argument.feesindcluded:
        print("You have used '-f' or '--feesindcluded with argument: {0}".format(argument.feesindcluded))
        status = True
    if argument.number:
        print("You have used '-n' or '--number' with argument: {0}".format(argument.number))
        status = True
    if argument.password:
        print("You have encrypted the vouchers/wallets with --pasword argument: {0}".format(argument.number))
        status = True  
    if not status:
        print("Maybe you want to use -H --Help or -n --nvouchers -v --value,  for example running 'grin-voucher.py -n 1 -v 1.0', creates a single voucher with a value of 1.0 ") 
    
    ## 0B)  Perform some basic sanity checks on the users input to avoid crashes
    args = vars(parser.parse_args()) #Dictionary containing all arguments
    if args.value <0.000001:
        raise ValueError('You are not allowed to create such low value vouchers since the transaction fee for using the transactions is equal or higher than the value of the voucher!')
    if args.nvouchers <=0:
        raise ValueError('You cannot create a negative number or zero vouchers, that does not make sence...')    

    
    ###############################################################################
    ## ITERATIVELY FOR EACH WALLET/VOUCHER                                      ##
    ###############################################################################
    for i in argument.number:
        
        ## 1) Create a temporary wallet/voucher using Mimblewimble-py, store their data
        ## as json | mnemonic | QR
        ###############################################################################
        
        ###############################################################################
        ## 3A) Build transaction on Mimnblewimble-py side
        ###############################################################################
        
        # instantiate two wallets wallet, path is path for address generation for account zero
        alice_path = 'm/0/1/0,'
        alice_wallet = Wallet.initialize()
        alice_address = alice_wallet.getSlatepackAddress()
        
        bob_path = 'm/0/1/0,'
        bob_wallet = Wallet.initialize()
        bob_address = bob_wallet.getSlatepackAddress()
        
        print('Alice: ', alice_address)
        print('Bob:   ', bob_address)
        
        # Alice makes 60 coins coinbase output
        coinbase_amount = 60000000000
        kernel, output = alice_wallet.createCoinbase(
            coinbase_amount, path=alice_path)
        
        # attempts to send 30 coins to Bob
        num_change_outputs = 1
        amount = 30000000000
        fee_base = 7000000
        block_height = 99999
        send_slate, secret_key, secret_nonce = alice_wallet.send(
            [output], num_change_outputs, amount, fee_base, block_height,
            path=alice_path, receiver_address=bob_address)
        
        print()
        print('send slate from Alice')
        print(send_slate.toJSON())
        
        # build the receive slate using Bob's wallet
        receive_slate = bob_wallet.receive(send_slate)
        
        print()
        print('receive slate from Bob')
        print(receive_slate.toJSON())
        
        # finalize the receive slate using Alice's wallet
        finalized_slate = alice_wallet.finalize(
            receive_slate, secret_key, secret_nonce, path=alice_path)
        
        print()
        print('finalized slate that Alice has')
        print(finalized_slate.toJSON())
        
        ###############################################################################
        ## 3 B) Create RSR transaction using Mimblewimble-py for all temporary wallets, 
        ## prerably as a single transaction
        ## Go to grin-wallet and sign tranaction, return via API, sign using mimblewimble-py
        ###############################################################################
        
        pp = pprint.PrettyPrinter(indent=4)
        api_url = 'http://localhost:3420/v3/owner'
        
        # change to your grin owner_api sercret file
        api_sercet_file = 'settings/.owner_api_secret'
        api_user = 'grin'
        api_password = open(api_sercet_file).read().strip()
        wallet = WalletV3(api_url, api_user, api_password)
        wallet.init_secure_api()
        
        # change to you wallet password
        wallet_password = 'Test123'
        
        wallet.open_wallet(None, wallet_password)
        pp.pprint(wallet.node_height())
        pp.pprint(wallet.get_slatepack_address())
        
        # send transaction, example from gate.io
        send_args = {
            'src_acct_name': None,
            'amount': int(2.67020546 * 1000000000),
            'minimum_confirmations': 10,
            'max_outputs': 500,
            'num_change_outputs': 1,
            'selection_strategy_is_use_all': False,
            'target_slate_version': None,
            'payment_proof_recipient_address': 'grin1n26np6apy07576qxasdfsdfasdfyz4qayuwxcpjvl87a2mjv3jpk6mnyz8y4vq65ahjm',
            'ttl_blocks': None,
            'send_args': {
                "dest": 'grin1n26np6apy0757asdfads6qx6yz4qayuwxcpjvl87a2mjv3jpk6mnyz8y4vq65ahjm',
                "post_tx": True,
                "fluff": True,
                "skip_tor": True
            }
        }
        print(wallet.init_send_tx(send_args))
        ## 