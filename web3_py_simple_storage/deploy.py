import json
import os

import solcx
from web3 import Web3
from dotenv import load_dotenv

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

solcx.install_solc('0.8.0')
load_dotenv()
# Solidity source code
compiled_sol = solcx.compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/9bc637ca65144048a4fc77a43b3979ec"))
chain_id = 4
my_address = "0x5B42291934d644CC2e79392B46352cdCE297f03D"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address)
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce
    }
)
signed_txn =w3.eth.account.sign_transaction(transaction, private_key)

tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

store_transaction = simple_storage.functions.store(11).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce +1
    }
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key)
tx_hash = w3.eth.sendRawTransaction(signed_store_txn.rawTransaction)
w3.eth.wait_for_transaction_receipt(
    tx_hash
)
print(simple_storage.functions.retrieve().call())