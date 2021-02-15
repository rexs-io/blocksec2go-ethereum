import logging
import time
from typing import Tuple, Optional

import blocksec2go
from blocksec2go.comm.pyscard import open_pyscard
from eth_account._utils.transactions import (
    encode_transaction,
    serializable_unsigned_transaction_from_dict
)
from eth_typing import ChecksumAddress, HexStr
from web3.types import TxParams

from . import _utils
from .exceptions import CardNotAvailable

Signature = Tuple[int, int, int]


class Blocksec2GoSigner:
    def __init__(self, key_id: int = 1, chain_id: Optional[int] = 1, connect_retry_count: int = 5):
        self._key_id = key_id
        self._chain_id = chain_id
        self._connect_retry_count = connect_retry_count
        self._reader = None
        self._pub_key: bytes = bytes(0)

        self._logger = logging.getLogger('security2go_ethereum')
        self._init()

    def _init(self):
        retries_left = self._connect_retry_count

        while not self._reader and retries_left >= 0:
            try:
                self._reader = open_pyscard()
            except RuntimeError as details:
                self._logger.debug(details)

                self._logger.info(f'Reader or card not found. {retries_left} retries left.')
                retries_left = retries_left - 1
                time.sleep(1)

        if not self._reader:
            self._logger.error('Exceeded connection retry count')
            raise CardNotAvailable

        blocksec2go.select_app(self._reader)
        self._pub_key = self._get_pub_key()
        self._logger.debug(f'Using public key {self._pub_key.hex()}')
        self._logger.info(f'Initialized for address {self.get_address()}')

    @property
    def chain_id(self):
        return self._chain_id

    @property
    def key_id(self):
        return self._key_id

    def get_address(self) -> ChecksumAddress:
        return _utils.address_from_public_key(self._pub_key)

    def sign_transaction(self, raw_tx: TxParams) -> HexStr:
        raw_tx.pop('from', None)
        raw_tx['chainId'] = self._chain_id

        tx = serializable_unsigned_transaction_from_dict(raw_tx)
        tx_hash = tx.hash()

        self._logger.debug(f'Signing transaction hash {tx_hash.hex()}')
        sig = self._generate_signature(tx_hash)
        signed_tx = encode_transaction(tx, vrs=sig)

        return HexStr(signed_tx.hex())

    def _generate_signature(self, tx_hash: bytes) -> Signature:
        _, _, signature_der = blocksec2go.generate_signature(
            self._reader, self._key_id, tx_hash
        )
        self._logger.debug('Generated signature')

        rs_sig = _utils.sigdecode_der(signature_der)
        v = _utils.get_v(rs_sig, tx_hash, self._pub_key, self._chain_id)
        r, s = rs_sig

        return v, r, s

    def _get_pub_key(self) -> bytes:
        _, _, pub_key = blocksec2go.get_key_info(self._reader, self._key_id)
        unprefixed_pub_key = pub_key[1:]
        return unprefixed_pub_key
