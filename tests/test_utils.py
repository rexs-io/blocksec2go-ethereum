from blocksec2go_ethereum._signer import Signature
from blocksec2go_ethereum._utils import get_v, address_from_public_key, sigdecode_der

test_signature: Signature = (119, 13721599831162923456657927172105796262173750250904149654514422912453024879155,
                             6849172825415158877547000581141514992709599875997948052677375877797118790017)
test_unrecoverable_signature = (test_signature[1], test_signature[2])
test_der_signature = bytes.fromhex(
    '304402201e562678e9038586672e801c521740e50474012bca0de8a8681c0117ee2b123302200f247e93b6258d981beaecdcc16c294d771a60a54481003f2a4af8b2d02cc981'
)
test_tx_hash = bytes.fromhex('86d4fe468d2b569c620da14500e7f455dbba5905cf8d8a74d34e55c9abfe454b')
test_pub_key = bytes.fromhex(
    'ab181ec96d7eebadc7e16fd67e8d91ea14f4671c87193aee9bd1c817803fe25fbda4fa44a502179b427b4e5d7c08c7de901e74c97aa1a1939f4a77ad7d3e4259'
)
test_address = '0x71A5fB76Ad2a284872b876D5B2e33AE83d48690b'
test_chain_id = 42


def test_sigdecode_der():
    returned_unrecoverable_sig = sigdecode_der(test_der_signature)
    assert test_unrecoverable_signature == returned_unrecoverable_sig


def test_address_from_public_key():
    returned_address = address_from_public_key(test_pub_key)
    assert test_address == returned_address


def test_get_v():
    returned_v = get_v(test_unrecoverable_signature, test_tx_hash, test_pub_key, test_chain_id)
    assert test_signature[0] == returned_v
