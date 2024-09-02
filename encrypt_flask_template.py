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
	print("install pycrypto: \"pip3 install pycrypto\"")
	exit(1)
import os, sys
from base64 import b64encode
from getpass import getpass
import codecs


def encrypt(tupleList):
	# sanitize input

	projectFolder = os.path.dirname(os.path.abspath(__file__))
	with open(os.path.join(projectFolder, "templates/decryptTemplate.html")) as f:
		templateHTML = f.read()

	encryptedDocument = templateHTML

	for tuple in tupleList:

		print(tuple[0])

		data = tuple[1].encode("utf8")

		salt = Random.new().read(32)
		key = PBKDF2(
			tuple[2].encode('utf-8'), 
			salt, 
			count=100000,
			dkLen=32, 
			hmac_hash_module=SHA256
		)
		iv = Random.new().read(16)

		cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
		encrypted, tag = cipher.encrypt_and_digest(data)
	
		encryptedPl = f'"{b64encode(salt+iv+encrypted+tag).decode("utf-8")}"'
		replaceString = "/*{{" + tuple[0] + "}}*/\"\""
		print(replaceString)
		encryptedDocument = encryptedDocument.replace(replaceString, encryptedPl)

	#filename, extension = os.path.splitext(inputfile)
	#outputfile = filename + "-protected" + extension
	#with codecs.open(outputfile, 'w','utf-8-sig') as f:
	#	f.write(encryptedDocument)
	#print("File saved to %s"%outputfile)
	return encryptedDocument