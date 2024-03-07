# grin-voucher
This is an explorative study done in my hobby time, not a commitment to this little endeavour.
This project aims to explore and create a prototype of a Grin-vouchers system. Grin-vouchers is a method to generate temporary wallets/vouchers that can be represented and shared as QR-code. 
Vouchers can be generated and loaded using mimblwimble-py and subsequently sweeped/transferred to an associated grin-wallet or Grin++ wallet through its API.

* **Use case 1**
  * Grin vouchers or top-up cards   
  * Paper money/Grin 
  * Cold wallet (cannot receive unless loaded)
  * NFC-chips used for example to make Grin-coins that hold Grin on a NFC chip (note life span of most chips is only few years)
  * Air drop/Gift cards etc.
    
* **Use case 2**
  * Vouchers can be used as semi "non-interactive" (NITX) and "non-secure" transactions methods for those who wish to do so
  * Sweeping happens via a transaction that only involves the receivers machine since the voucher contains the senders’ keys or a full wallet. The transaction therefore is asynchronous interactive (most would call this non-interactive) since the sender of the coins does not need to be online.   
  * Vouchers do not involve payment proofs and should only be used for fun. I cannot stress this enough, but payment proofs are a requirement for a regular transaction, vouchers are in no way ever intended to replace normal transactions.
 
 *  **Use case 3**
   * Sweeping a normal wallet, e.g. remaining funds from a hot wallet to a new one. This would involve an encrypted wallet, so probably best to support full wallets with or without encryption for sweeping  
 
* TO DO
  * Check how Bitcoin paper wallets and others are shared through QR, do not reinvent, find a BIP if possible and follow standards
    * https://github.com/jujum4n/PyperWallet
    * https://github.com/mr-infty/paper-wallet
    * https://github.com/Bitcoin-com/paperwallet.bitcoin.com/ 
  * Read up on using the grin-wallet API, is Grin++ wallet API with identical API calls ready to use (ask David)?
  * Start testing
  * For the future, make a feature request a sweep method (transaction) to be implemented in grin-wallet Grin++ to help facilitate this system, optionally just as a Python Add On.

