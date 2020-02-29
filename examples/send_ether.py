from blocksec2go_ethereum import Blocksec2GoSigner
from web3 import Web3

WEB3_ENDPOINT = 'YOUR_ENDPOINT_HERE'

web3 = Web3(Web3.HTTPProvider(WEB3_ENDPOINT))
chain_id = web3.eth.chainId

signer = Blocksec2GoSigner(chain_id=chain_id, key_id=1)
address = signer.get_address()

nonce = web3.eth.getTransactionCount(address)
raw_tx = {
    'to': '0xBaBC446aee039E99d624058b0875E519190C6758',
    'nonce': nonce,
    'value': Web3.toWei(0.00005, 'ether'),
    'gas': 21000,
    'gasPrice': Web3.toWei(5, 'gwei'),
}
signed_tx = signer.sign_transaction(raw_tx)

tx_hash = web3.eth.sendRawTransaction(signed_tx)
print(f'Sent transaction with hash: {tx_hash.hex()}')
