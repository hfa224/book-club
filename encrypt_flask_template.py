#!/usr/bin/python3
# Based on PageCrypt
# Original code is
# Copyright (c) 2021 Maximillian Laumeister
# Copyright (c) 2021 Samuel Plumppu

try:
    from Crypto import Random
    from Crypto.Util.py3compat import bchr
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Hash import SHA256
except:
    print('install pycrypto: "pip3 install pycrypto"')
    sys.exit(1)
import os
import sys
from base64 import b64encode
from getpass import getpass
import codecs


def encrypt(tuple_list):

    project_folder = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(project_folder, "templates/decryptTemplate.html")) as f:
        template_HTML = f.read()

    encrypted_doc = template_HTML

    for user_info_tuple in tuple_list:

        print(user_info_tuple[0])

        data = user_info_tuple[1].encode("utf8")

        salt = Random.new().read(32)
        key = PBKDF2(
            user_info_tuple[2].encode("utf-8"),
            salt,
            count=100000,
            dkLen=32,
            hmac_hash_module=SHA256,
        )
        iv = Random.new().read(16)

        cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
        encrypted, tag = cipher.encrypt_and_digest(data)

        encrypted_pl = f'"{b64encode(salt+iv+encrypted+tag).decode("utf-8")}"'
        replace_string = "/*{{" + user_info_tuple[0] + '}}*/""'
        encrypted_doc = encrypted_doc.replace(replace_string, encrypted_pl)
    return encrypted_doc
