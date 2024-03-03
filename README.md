# grin-voucher
This is an explorative study done in my hobby time, not a commitment to this endavour.
This little projects aims to to explore and create a prototype of a Grin-vouchers system. Grin-vouchers is a method to generate temporary wallets/vouchers that can be represented and shared as QR-code 
Vouchers can be generated and loaded using mimblwimble-py and subsequently sweeped/transfered to an associated grin-wallet or Grin++ wallet through its API.

* **Use case 1**
  * Grin vouchers or top-up cards   
  * Paper money/Grin 
  * Cold wallet (cannot receive unles loaded)
  * NFC-chips used for exaple to make Grin-coins that hold Grin on a NFC chip (note life spann of chip)
  * Air drop/Gift cards etc.
    
* **Use case 2**
  * Vouchers can be used as semi "non-interactive" (NITX) and "non-secure" transactions methods for those who wish to do so
  * Sweeping happens via a transaction that only involves the receiver since the voucher contains the senders keys. The transaction is therefore partly non-interactive since the sender of the coins does not need to be online.   
  * Vouchers do not involve payment proofs and should only be used for fun. I cannot stress this enough, but payment proofs are a requirement for a regular transactions, vouchers are in no way ever intended to replace normal transactions.
 
* TO DO
  * Check how Bitcoin paper wallets and others are shared through QR, do not reinvent, find a BIP if possible and follow standards
  * Read up on using the grin-wallet API, is Grin++ wallet API with identicals ready to use (ask David)
  * Start testing
  * For the future, ask a sweep method (transaction) to be implemented in grin-wallet Grin++
