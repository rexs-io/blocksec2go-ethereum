from typing import Tuple, Optional

import ecdsa
from eth_typing import ChecksumAddress
from web3 import Web3

from .exceptions import InvalidSignature

UnrecoverableSignature = Tuple[int, int]


def sigdecode_der(sig: bytes) -> UnrecoverableSignature:
    return ecdsa.util.sigdecode_der(sig, 0)


def find_recovery_id(sig: UnrecoverableSignature, tx_hash: bytes, pub_key: bytes) -> int:
    r, s = sig
    vk = ecdsa.VerifyingKey.from_string(pub_key, curve=ecdsa.SECP256k1)
    vk_point = vk.pubkey.point
    hash_number = ecdsa.util.string_to_number(tx_hash)

    public_keys = ecdsa.ecdsa.Signature(r, s).recover_public_keys(hash_number, ecdsa.SECP256k1.generator)
    if public_keys[0].point == vk_point:
        return 0
    elif public_keys[1].point == vk_point:
        return 1
    raise InvalidSignature


def address_from_public_key(public_key: bytes) -> ChecksumAddress:
    pk_hash = Web3.keccak(public_key)
    address_bytes = pk_hash[-20:]
    address = address_bytes.hex()
    return Web3.toChecksumAddress(address)


def get_v(sig: UnrecoverableSignature, tx_hash: bytes, pub_key: bytes, chain_id: Optional[int]) -> int:
    recovery_id = find_recovery_id(sig, tx_hash, pub_key)

    if not chain_id:
        return 27 + recovery_id
    return 35 + recovery_id + (chain_id * 2)
