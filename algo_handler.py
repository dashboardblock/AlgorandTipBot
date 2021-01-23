import os
from algosdk import account, mnemonic
from algosdk.future.transaction import PaymentTxn
from algosdk.v2client import indexer, algod
import models


#  Set Configuration Values
ALGOD_ADDRESS = os.getenv('ALGOD_ADDRESS', 'Token Not found')
INDEXER_ADDRESS = os.getenv('INDEXER_ADDRESS', 'Token Not found')
API_KEY = os.getenv('API_KEY', 'Token Not found')
HEADERS = {"x-api-key":API_KEY}
ALGODCLIENT = algod.AlgodClient(algod_token=API_KEY, algod_address=ALGOD_ADDRESS, headers=HEADERS)
myindexer = indexer.IndexerClient(indexer_token=API_KEY, indexer_address=INDEXER_ADDRESS, headers=HEADERS)

def get_balance(username):
    address = models.fetch_user(username)[0][1]
    response = myindexer.account_info(address=address)
    if 'account' in response:
        balance = float(response['account']['amount'])/1000000
    else:
        balance = 0
    return balance

def algo_transaction(sender, private_key, receiver, amount):
    """Function for Algos transfer"""
    amount = int(amount*1000000)
    params = ALGODCLIENT.suggested_params()
    txn = PaymentTxn(sender, params, receiver, amount, None)
    signed_tx = txn.sign(private_key)
    ALGODCLIENT.send_transaction(signed_tx)
    return True

def wait_for_confirmation(client, txid):
	"""
	Utility function to wait until the transaction is
	confirmed before proceeding.
    
    # wait for confirmation
	wait_for_confirmation(algod_client, txid) 

	"""
	last_round = client.status().get('last-round')
	txinfo = client.pending_transaction_info(txid)
	while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
		print("Waiting for confirmation")
		last_round += 1
		client.status_after_block(last_round)
		txinfo = client.pending_transaction_info(txid)
	print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
	return txinfo

def check_account(username):
    if not models.fetch_user(username):
        private_key, address, passphrase = create_wallet()
        passphrase = mnemonic.from_private_key(private_key)
        models.insert_user(username,address,private_key,passphrase)
    return True

def create_wallet():
    """ Create new Algorand wallet """
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)
    return private_key, address, passphrase


def get_private_key(passphrase):
    private_key = mnemonic.to_private_key(passphrase)
    return private_key


def send_tip(username,target,amount):
    check_account(username)
    balance = get_balance(username)
    sender = models.fetch_user(username)[0][1]
    private_key = models.fetch_user(username)[0][2]
   
    if balance < amount+0.001:
        status = "@{0} you have insufficient funds.".format(username)
    elif target == username:
        status ="You can't tip yourself."   
    elif target == "algorandtipbot":
        receiver = models.fetch_user(target)[0][1]
        algo_transaction(sender, private_key, receiver, amount)
        status = "Thank you!"
    else:
        check_account(target)
        receiver = models.fetch_user(target)[0][1]
        algo_transaction(sender, private_key, receiver, amount)
        status="@{0} tipped \U0001F4B8 @{1} {2} ALGO".format(username, target, amount)
    return status