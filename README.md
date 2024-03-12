# grin-vouchers
This is an exploratory study done in my hobby time, not a commitment to this little endeavor.
This project aims to explore and create a prototype of a **Grin-vouchers** system. Grin-vouchers are a method to 1) generate temporary wallets/vouchers that can be shared as QR-code and, 2) load these wallet/vouchers and transfering their funds using a normal grin transaction. 

Vouchers can be generated and loaded using this command-line script/tool that uses mimblwimble-py to generate wallets to which funds are transferred via the grin-wallet/Grin++ API. Scanning a vouchers QR code loads the wallet into a temporary wallet file and subsequent transfer these funds to the main wallet after the user reviewed and approved the transaction. For testing purposes, loading of wallets can be done using their grin-wallet and Grin++ API, but hopefully in the future it will be supported to load/sweep wallet vouchers with a dedicated command and GUI button.

* **Use case 1**
  * Grin vouchers or top-up cards   
  * Paper money/Grin 
  * Cold wallet (cannot receive unless loaded)
  * NFC-chips used for example to make Grin-coins that hold Grin on a NFC chip (note life span of most chips is only few years)
  * Air drop/Gift cards etc.
    
* **Use case 2**
  * Vouchers can be used as a two step user asynchronous "non-interactive" (UNITX) transactions but  _**should be considered unsafe since there is no payment proofs for the sender of the voucher**_. 
  * Sweeping happens via a transaction that only involves the receivers machine since the receiver controls both the senders and receivers keys. In summary ***grin vouchers are in no way intended to replace normal transactions since there are no payment proofs and no ways to settle disputes!***.
 
 * **Use case 3**
   * Sweeping a normal wallet, e.g. remaining funds from a hot wallet to a new one. This would involve an encrypted wallet, so probably best to support full wallets with or without encryption for sweeping. This use case has little to do with grin vouchers,   although you could generate a paper wallet as cold storage-backup or a method to easily transfer a full wallet or its funds as a QR code between device. Note that in theory this method can also be loaded for easy wallet migration between devices without even swiping the funds. In this use case the wallet is still encrypted meaning that its transfer should be completely safe and does not create any security risks.

## Security considerations
* Sweeping of a voucher/wallet is done using a normal transaction with the only difference being that both wallets are on the receivers machine since the the senders handed over the voucher wallet to the receiver and simply gives full control to the receiver to do with the funds whatever the receiver wants. 
* Note a *grin voucher does requires interaction* from the sender to the receiver who simply gives the wallet/vouchers to the receiver. From a user perspective the transaction is asynchronous (async) and involves two steps *Receiver -> Sender (RS)*,  opposed to normal transaction contracts which are SRS or RSR and involve three steps. 
Potential attacks/mall-uses: 
1) Empty voucher is sold or will be sweeped before the receiver can sweep the funds. Note in theory the seller can start a race condition after the receiver sweeps the funds by having his transaction include higher transaction fees (no payment proof).
2) the receiver receives the voucher and refuses the pay the sender (no payment proof)
3) the receiver first pays in fiat or crypto, but does not receive the voucher after the purchase (no payment proof)
4) dust attack, the voucher contains more output than the receiver/sweeping wallet can handle, potentially making the receivers wallet unusable. Best to always show the number of outputs to be loaded to the user so he/she can decide himself whether the number of outputs poses a risk.
5) dust attack 2, the dust outputs do hold the value but will be consumed in transaction fees, I call this the *F#ck you attack* since the attack is costly for the sender since creating these outputs is 21 times more costly than using them as inputs in a transaction and such would only be done to F#ck with the receiver. See the transaction fee weight calculations for details
https://github.com/mimblewimble/grin-rfcs/blob/master/text/0017-fix-fees.md
In a far future this attack could be done by trying to 'sell' left over dust outputs in a wallet for some value as voucher.
This attack can be mitigated simply be refusing to load any outputs that have a value below the 0.00001 ツ.

**Vouchers do not generate usable payment proofs** since the proof is between the voucher temporary wallet and not with the original senders wallet, there is no payment proof between sender and receiver. Therefore, grin vouchers should only be used for small value transfers and "Fun" transactions since giving a voucher means giving 100% control to the receiver with no way for dispute settlements! In summary ***grin vouchers are in no way intended to replace normal transactions, use them at your own risk!***.

## TO DO
  * Check how Bitcoin paper wallets and others are shared through QR, do not reinvent, find a BIP if possible and follow standards
    * https://github.com/jujum4n/PyperWallet
    * https://github.com/mr-infty/paper-wallet
    * https://github.com/Bitcoin-com/paperwallet.bitcoin.com/ 
  * Read up on using the grin-wallet API, is Grin++ wallet API with identical API calls ready to use (ask David)?
  * Start testing
  * Make a feature request a sweep method (transaction) to be implemented in grin-wallet Grin++ to help facilitate this system, optionally just as a Python Add On.  
     * Asked Michael to look into whether grin-wallet can support two wallets under the hood for "sweeping" of funds, which would make loading vouchers way more user friendly.
   
## Dependencies, note for Linux use pip3 to install librararies for Python 3
* https://docs.python.org/3/howto/argparse.html
```
pip install argparse
```
* https://github.com/grinventions/mimblewimble-py
```
pip install mimblewimble
```
* https://github.com/grinfans/grinmw.py (API wrapper)
```
pip install grinmw
```
* https://pypi.org/project/qrcode/
```
pip install qrcode
```
* https://docs.python.org/3/library/tomllib.html](https://github.com/uiri/toml
```
pip install toml
```


  

