"""Opa"""

import segno

def generate_qr_image(text):
    qrcode = segno.make(text, version=20)
    qrcode.save('qr.png')

if __name__ == '__main__':
    pass
