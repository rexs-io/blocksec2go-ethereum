# Blocksec2Go-Ethereum

This repository contains the source code of `blocksec2go-ethereum` Python package which wraps the `blocksec2go` package to allow easier interaction with Ethereum blockchain.

__Read more about rationale behind this package [on our blog post](https://link.medium.com/HPJLdyKpd7)__

If you're unsure what Blockchain Security 2 Go is, [you can find more info here](https://github.com/Infineon/Blockchain).

## Installation

```bash
pip install blocksec2go-ethereum
```

## Usage

After creating an instance of `Blocksec2Go` you can use it to generate signatures for transaction dicts. When passed raw tx, `sign_transaction()` will return a hex string of RLP-encoded signed transaction that can be directly consumed by `web3.eth.sendRawTransaction()`.

The replay attack protection introduced with [EIP-155](https://eips.ethereum.org/EIPS/eip-155) is used by default. Set `chain_id=None` to force the legacy behaviour for backward compatibility.
### Transfer Ether

Below you will find an example of signing a simple Ether transfer:

```python
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
```

### Call a contract function

You can also sign any contract calls/creation transactions by leveraging `buildTransaction()`.

Please note that for some contracts `buildTransaction()` may require explicitly setting `from` field to properly estimate gas.

```python
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
``` 

## License
ISC © 2020 rexs.io
