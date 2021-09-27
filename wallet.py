import subprocess
import json
import os

from constants import BTC, BTCTEST, ETH
from pprint import pprint

#from dotenv import load_dotenv

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

from web3 import Web3, middleware, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER', 'http://localhost:8545')))

#enable PoA
w3.middleware_onion.inject(geth_poa_middleware, layer = 0)

#set up gas price
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

#Set up mnemonic

mnemonic=os.getenv("Mnemonic", "false bracket rally company deposit reopen injury absent prize warfare voice unknown")

# Create a function called `derive_wallets`
def derive_wallets(coin=BTC, mnemonic=mnemonic, depth = 3):
    command = f"./derive -g --mnemonic='{mnemonic}' --coin={coin} --numderive={depth} --format=json"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {ETH:derive_wallets(coin=ETH),BTCTEST:derive_wallets(coin=BTCTEST),
}

pprint(coins)

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, private_key):
    if coin == ETH:
        return Account.privateKeyToAccount(private_key)
    if coin == BTCTEST:
        return PrivateKeyTestnet(private_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == ETH:
        value = w3.toWei(amount, "ether")
        EstimatedGas = w3.eth.estimateGas({"to": to, "from": account.address, "amount": value})
        return{"to":to,
            "from": account.address,
            "value": value,
            "Gas": EstimatedGas,
            "GasPrice": w3.eth.generateGasPrice(),
            "Nonce": w3.eth.getTransactionCount(account.address),
            "ChainID": w3.net.chainId}
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    if coin == ETH:
        RawEth = create_tx(coin, account, to, amount)
        SignETH = account.signTransaction(RawEth)
        return w3.eth.sendRawTransaction(SignETH.rawTransaciton)

    if coin == BTCTEST:
        RawBTCTEST = create_tx(coin, account, to, amount)
        SignBTCTEST = account.sign_transaction(RawBTCTEST)
        return NetworkAPI.broadcast_tx_testnet(SignBTCTEST)


