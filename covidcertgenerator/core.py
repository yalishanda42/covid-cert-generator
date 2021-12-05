"""Opa"""

import segno

import zlib

from base45 import b45decode, b45encode
import cbor2
from cose.messages import CoseMessage


def decode_from_qr_text(text):
    """Return decoded JSON string from QR code"""
    text_without_prefix = text[4:]
    compressed = b45decode(text_without_prefix)
    cwt = zlib.decompress(compressed)
    cose = CoseMessage.decode(cwt)
    original_json = cbor2.loads(cose.payload)
    return original_json


def encode_to_qr_text(json_object):
    """Return QR code text from JSON string"""
    cbor_encoded = cbor2.dumps(json_object)

    # cose_message = Sign1Message(
    #     phdr={Algorithm: Es256},
    #     uhdr={KID: b'&:\xa5\xf6\xb0k\x8cr'},
    #     payload=cbor_encoded
    # )
    # cose_encoded = cose_message.encode()  # not this time, pal:

    head = b'\xd2\x84C\xa1\x01&\xa1\x04H&:\xa5\xf6\xb0k\x8crY\x013'
    signature = b'X@q\xa5X{\x03\xb9\x17\x90@\x8b$\x9e\xb3\xf0\x7f(\xbf\xe7\xd6\xfc<G\xd2\xd0\xe3B?b\xbd\x82\xbd\x8a\xb3~\xd6\x19P\rYS"\x8c+\xbd\xdb3\x1e\xe7#\xef\xcb\xc5}add\x9dfND\t,\xb9\x94'
    cose_encoded = head + cbor_encoded + signature  # absurd da stane

    compressed = zlib.compress(cose_encoded)
    # but for some reason the second byte is "wrong":
    bytelist = list(compressed)
    bytelist[1] = 0xDA  # da.
    compressed_modified = bytes(bytelist)

    base_45_encoded = b45encode(compressed_modified).decode("utf-8")
    return f"HC1:{base_45_encoded}"


def generate_qr_image(text):
    qrcode = segno.make(text, version=20)
    qrcode.save('qr.png')


if __name__ == '__main__':
    # for test purposes
    jsonobj = decode_from_qr_text("HC1:NCFOXN*TS0BI$ZDYSH$PJ6RQPM3 RF:D4M+H-36HD7-TM9W4OFW5DOP-IW/T3QGNO4*J8OX4W$C2VLWLI3K5YO9OUUMK9WLIK*L5R1G$JA-LI*NVPO8UK00SR%BF:PYI0I*FCZ7:PIWEGLS47%S7Y48YIZ73423ZQT+EJKD3XW4UZ2 NVV5TN%2UP20J5/5LEBFD-48YI+T4D-4HRVUMNMD3*20EJK-+K.IA.C8KRDL4O54O6KKUJK6HI0JAXD15IAXMFU*GSHGRKMXGG6DBYCBMQN:HG5PAHGG8KES/F-1JF.KAU0VWNVGISKE MCAOI8%MYYN7L6QV9P86QQOUK1A-5+TN795-Z73G88GPC%F7TT$BB9Z2*DB3:5GLNNUTMB0PR17T0B3V1FDUZ464K/:FHD4DGC9NTXW49:H 4M5LO$.FC:HC%6S+C+8AFT5D75W9AAABG64IIK%DD- 64:9N618/RRXUA6G-CRCGW*PR4O38M9: 3GKRV0U2UR /MH7U+SCV3E3DM:8I 7S.3P-AQ7CSW*77UJVLIK27PAQLOAQ9TX40*VBL5")
    ascii = encode_to_qr_text(jsonobj)
    generate_qr_image(ascii)
