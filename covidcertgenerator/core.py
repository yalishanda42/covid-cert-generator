"""Opa"""

import segno

import zlib
import json
from base45 import b45decode, b45encode
import cbor2
from cose.messages import CoseMessage


def decode_from_qr_text(text):
    """Return decoded JSON from a QR code text"""
    text_without_prefix = text[4:]
    compressed = b45decode(text_without_prefix)
    cwt = zlib.decompress(compressed)
    cose = CoseMessage.decode(cwt)
    original_json = cbor2.loads(cose.payload)
    return original_json


def encode_to_qr_text(json_object):
    """Return QR code text from a JSON object"""
    cbor_encoded = cbor2.dumps(json_object)

    # cose_message = Sign1Message(
    #     phdr={Algorithm: Es256},
    #     uhdr={KID: b'&:\xa5\xf6\xb0k\x8cr'},
    #     payload=cbor_encoded
    # )
    # cose_encoded = cose_message.encode()  # not this time, pal:

    head = b'\xd2\x84C\xa1\x01&\xa1\x04H&:\xa5\xf6\xb0k\x8cr'
    signature = b'X@q\xa5X{\x03\xb9\x17\x90@\x8b$\x9e\xb3\xf0\x7f(\xbf\xe7\xd6\xfc<G\xd2\xd0\xe3B?b\xbd\x82\xbd\x8a\xb3~\xd6\x19P\rYS"\x8c+\xbd\xdb3\x1e\xe7#\xef\xcb\xc5}add\x9dfND\t,\xb9\x94'

    payload_len = len(cbor_encoded)
    payload_len_bytes = payload_len.to_bytes(2, byteorder='big')  # because it's larger than 255 bytes
    cbor_payload_type = b'\x59' + payload_len_bytes  # data field of size `payload_len_bytes`
    cose_encoded = head + cbor_payload_type + cbor_encoded + signature  # absurd da stane

    compressed = zlib.compress(cose_encoded)
    # but for some reason the second byte is "wrong":
    bytelist = list(compressed)
    bytelist[1] = 0xDA  # da.
    compressed_modified = bytes(bytelist)

    base_45_encoded = b45encode(compressed_modified).decode("utf-8")
    return f"HC1:{base_45_encoded}"


def generate_qr_image(text):
    qrcode = segno.make(text, version=16)
    qrcode.save('qr.png')


def generate_custom_json(*,
    first_name_original="ИВАН ДИМИТРОВ",
    first_name_official="IVAN<DIMITROV",
    last_name_original="ГЕОРГИЕВ",
    last_name_official="GEORGIEV",
    date_of_birth_YYYY_MM_DD="1984-04-20",
    issued_timestamp=1622592000,
    expiry_timestamp=1654128000,
):
    return json.loads(json.dumps({
        "1": "BG",
        "4": expiry_timestamp,
        "6": issued_timestamp,
        "-260": {
            "1": {
                "v": [
                    {
                        "ci": "urn:uvci:01:BG:DJFVEZSFMD763P5L#H",
                        "co": "BG",
                        "dn": 2,
                        "dt": "2021-06-02",
                        "is": "Ministry of Health",
                        "ma": "ORG-100001699",
                        "mp": "EU/1/21/1529",
                        "sd": 2,
                        "tg": "840539006",
                        "vp": "J07BX03"
                    }
                ],
                "dob": date_of_birth_YYYY_MM_DD,
                "nam": {
                    "fn": first_name_original,
                    "fnt": first_name_official,
                    "gn": last_name_original,
                    "gnt": last_name_official
                },
                "ver": "1.3.0"
            }
        }
    }))


if __name__ == '__main__':
    testjson = generate_custom_json()
    testqr = encode_to_qr_text(testjson)
    testdecode = decode_from_qr_text(testqr)
    generate_qr_image(testqr)

