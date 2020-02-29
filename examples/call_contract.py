import json

from blocksec2go_ethereum import Blocksec2GoSigner
from web3 import Web3

WEB3_ENDPOINT = 'YOUR_ENDPOINT_HERE'

web3 = Web3(Web3.HTTPProvider(WEB3_ENDPOINT))
chain_id = web3.eth.chainId

signer = Blocksec2GoSigner(chain_id=chain_id, key_id=1)
address = signer.get_address()

with open('artifact.json', 'r') as artifact_file:
    artifact = json.loads(artifact_file.read())
    contract = web3.eth.contract(address=artifact['address'], abi=artifact['abi'])

nonce = web3.eth.getTransactionCount(address)
raw_tx = contract.functions.setValue(42).buildTransaction({'nonce': nonce, 'from': address})
signed_tx = signer.sign_transaction(raw_tx)

tx_hash = web3.eth.sendRawTransaction(signed_tx)
print(f'Sent transaction with hash: {tx_hash.hex()}')
