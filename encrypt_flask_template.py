"""Contains encryption logic for generating wrapped pages with login"""
#!/usr/bin/python3
# Based on PageCrypt
# Original code is
# Copyright (c) 2021 Maximillian Laumeister
# Copyright (c) 2021 Samuel Plumppu


import os
import sys
from base64 import b64encode
try:
    from Crypto import Random
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Hash import SHA256
except ImportError:
    print('install pycrypto: "pip3 install pycrypto"')
    sys.exit(1)


def encrypt(members_list):
    """Encrypt the page generated for each member and insert it in the decrypt template HTML
        based on the key given for each member"""

    project_folder = os.path.dirname(os.path.abspath(__file__))
    with open(file=os.path.join(project_folder, "templates/decryptTemplate.html"),
              encoding="utf8") as f:
        template_html = f.read()

    encrypted_doc = template_html

    for member_info_tuple in members_list:

        print(member_info_tuple[0])

        data = member_info_tuple[1].encode("utf8")

        salt = Random.new().read(32)
        key = PBKDF2(
            member_info_tuple[2].encode("utf-8"),
            salt,
            count=100000,
            dkLen=32,
            hmac_hash_module=SHA256,
        )
        iv = Random.new().read(16)

        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        encrypted, tag = cipher.encrypt_and_digest(data)

        encrypted_pl = f'"{b64encode(salt+iv+encrypted+tag).decode("utf-8")}"'
        replace_string = "/*{{" + member_info_tuple[0] + '}}*/""'
        encrypted_doc = encrypted_doc.replace(replace_string, encrypted_pl)
    return encrypted_doc
