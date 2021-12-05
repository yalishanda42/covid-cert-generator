"""Unit tests"""

import unittest
from covidcertgenerator import *
from covidcertgenerator.core import generate_custom_json

class Tests(unittest.TestCase):
    """Unit tests"""

    def __init__(self, *args, **kwargs):
        super(Tests, self).__init__(*args, **kwargs)
        self.maxDiff = None

    def test_decode_encode_real_cert_is_reversible(self):
        """Test that the decode and encode functions are reversible for the scraped certificate."""
        text = "HC1:NCFOXN*TS0BI$ZDYSH$PJ6RQPM3 RF:D4M+H-36HD7-TM9W4OFW5DOP-IW/T3QGNO4*J8OX4W$C2VLWLI3K5YO9OUUMK9WLIK*L5R1G$JA-LI*NVPO8UK00SR%BF:PYI0I*FCZ7:PIWEGLS47%S7Y48YIZ73423ZQT+EJKD3XW4UZ2 NVV5TN%2UP20J5/5LEBFD-48YI+T4D-4HRVUMNMD3*20EJK-+K.IA.C8KRDL4O54O6KKUJK6HI0JAXD15IAXMFU*GSHGRKMXGG6DBYCBMQN:HG5PAHGG8KES/F-1JF.KAU0VWNVGISKE MCAOI8%MYYN7L6QV9P86QQOUK1A-5+TN795-Z73G88GPC%F7TT$BB9Z2*DB3:5GLNNUTMB0PR17T0B3V1FDUZ464K/:FHD4DGC9NTXW49:H 4M5LO$.FC:HC%6S+C+8AFT5D75W9AAABG64IIK%DD- 64:9N618/RRXUA6G-CRCGW*PR4O38M9: 3GKRV0U2UR /MH7U+SCV3E3DM:8I 7S.3P-AQ7CSW*77UJVLIK27PAQLOAQ9TX40*VBL5"

        decoded = decode_from_qr_text(text)
        encoded = encode_to_qr_text(decoded)

        self.assertEqual(text, encoded)

    def test_encode_decode_fake_objects_are_reversible(self):
        """Test that the decode and encode functions are reversible for fake objects."""
        fake_cert = generate_custom_json()

        encoded = encode_to_qr_text(fake_cert)
        decoded = decode_from_qr_text(encoded)

        self.assertEqual(fake_cert, decoded)


if __name__ == '__main__':
    unittest.main()