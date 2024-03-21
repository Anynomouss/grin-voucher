# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 13:57:49 2024
@author: Anynomous
Licence: Apache v2.0.
Dislaimer: Software is provided as it without any waranty, use it at your own risk
WARNINGs: 
    -This tool is best adviced to be run in a secure environment since vouchers are by default not encrypted with a password.
    -Vouchers should not be used for any amount of Grin with significant value. 
    -Grin vouchers can be used to as two step transaction method, but do not generate
    payment proofs and as such should be only be used when the sender 100% accepts
    the receiver gains 100% control over the funds in the vouchers without any way 
    to settle disputes. 
BEFORE YOU START, RUN GRIN NODE, INIT A WALLET AND ENABLE OWNER API:
    grin-wallet.exe init -r --here 
    grin-wallet.exe  --testnet owner_api --run_foreign    
    grin.exe --testnet
    
PROCEDURE:
    ITERATIVEY - for each wallets/vouchers, do the following:
1) Create a wallet using mimblewimble-py, 
2) Initiate a SRS transaction through the grin-wallet API -> grinmw library
3) Sign the transaction using the voucher wallet, - >  mimblewimble-py library
4) Sign with grin-wallet using the API (grinmw library) and finalize/broadcast the transaction
5) Create output wallet backup in the log file and generate the vouchers
    
USEFULL LINKS:
https://github.com/grinventions/mimblewimble-py
https://grincc.github.io/grin-wallet-api-tutorial/
https://docs.rs/grin_wallet_api/latest/grin_wallet_api/trait.OwnerRpc.html#required-methods 
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
    parser.add_argument("-p", "--password", help = "Example: --password mimblewimble", required = False, default = "", type=str)
    parser.add_argument("-f", "--feesindcluded", help = "Example: --feesindcluded True", required = False, default = True, type=bool)
    
    argument = parser.parse_args()
    status = False
    
    if argument.Help:
        print("You have used '-H' or '--Help' with argument: {0}".format(argument.Help))
        status = True
    if argument.nvouchers:
        print("You have used '-n' or '--vouchers' with argument: {0}".format(argument.nvouchers))
        status = True
    if argument.value:
        print("You have used '-v' or '--value' with argument: {0}, meaning you want to send that much ツ".format(argument.value))
        status = True
    if argument.feesindcluded:
        print("You have used '-f' or '--feesindcluded with argument: {0}".format(argument.feesindcluded))
        status = True
    if argument.nvouchers:
        print("You have used '-n' or '--number' with argument: {0}".format(argument.nvouchers))
        status = True
    if argument.password:
        print("You have encrypted the vouchers/wallets with --pasword argument: {0}".format(argument.password))
        status = True  
    if not status:
        print("Maybe you want to use -H --Help or -n --nvouchers -v --value,  for example running 'grin-voucher.py -n 1 -v 1.0', creates a single voucher with a value of 1.0 ") 
    
    ## 0B)  Perform some basic sanity checks on the users input to avoid crashes
    args = vars(parser.parse_args()) #Dictionary containing all arguments
    if argument.value <0.000001:
        raise ValueError('You are not allowed to create such low value vouchers since the transaction fee for using the transactions is equal or higher than the value of the voucher!')
    if argument.nvouchers <= 0:
        raise ValueError('You cannot create a negative number or zero vouchers, that does not make sense...')    

    
    ###########################################################################
    ## ITERATIVELY FOR EACH WALLET/VOUCHER                                   ##
    ###########################################################################
    for i in range(0,argument.nvouchers):
        
        ## 1) Create a temporary wallet/voucher using Mimblewimble-py, store their data
        ## as json | mnemonic | QR
        #######################################################################
               
        ## instantiate two wallets wallet, path is path for address generation for account zero
        voucher_path = 'm/0/1/0'
        voucher_wallet = Wallet.initialize()
        voucher_slatepack_address = voucher_wallet.getSlatepackAddress()
        
        
        #######################################################################
        ## 2 Initiate an SRS transaction via the wallet owner API
        #######################################################################
        
        ## The path assumes you innitiated the sender wallet with grin-wallet --here
        pp = pprint.PrettyPrinter(indent=4)
        api_url = 'http://localhost:3420/v3/owner'
        
        ## change to your grin owner_api sercret file
        api_sercet_file = 'settings/.owner_api_secret'
        api_user = 'grin'
        api_password = open(api_sercet_file).read().strip()
        wallet = WalletV3(api_url, api_user, api_password)
        wallet.init_secure_api()
        
        ## change to you wallet password
        wallet_password = 'Test123' 
        wallet.open_wallet(None, wallet_password)
        ## pp.pprint(wallet.get_slatepack_address())
        
        ## send transaction, example from gate.io
        send_args = {
            'src_acct_name': None,
            'amount': int(argument.value * 1000000000),
            'minimum_confirmations': 10,
            'max_outputs': 500,
            'num_change_outputs': 1,
            'selection_strategy_is_use_all': False,
            'target_slate_version': None,
            'payment_proof_recipient_address': voucher_slatepack_address, 
            'ttl_blocks': None,
            'send_args': {
                "dest": 'grin1n26np6apy0757asdfads6qx6yz4qayuwxcpjvl87a2mjv3jpk6mnyz8y4vq65ahjm',
                "post_tx": True,
                "fluff": True,
                "skip_tor": True,
                "amount_includes_fee":argument.feesindcluded
            }
        }
        
        results = wallet.init_send_tx(send_args)
        print(results)
        
        
        #######################################################################
        ## 3) Sign the transaction using the voucher wallet
        #######################################################################
        
        #receive_slate = voucher_wallet.receive(send_slate)
        
        #######################################################################
        ## 4) Sign with grin-wallet using the API (grinmw library) and finalize/broadcast the transaction
        #######################################################################