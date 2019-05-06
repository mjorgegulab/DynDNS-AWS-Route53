#!/usr/bin/env python3

import sys
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

banner = '''   ___               _                                
  / __|_ _ _  _ _ __| |_ ___ _ _                      
 | (__| '_| || | '_ \  _/ _ \ '_|                     
  \___|_|  \_, | .__/\__\___/_|__      ___      _____ 
 |   \ _  _|__/|_|_|   \| \| / __|___ /_\ \    / / __|
 | |) | || | ' \___| |) | .` \__ \___/ _ \ \/\/ /\__ \\
 |___/ \_, |_||_|  |___/|_|\_|___/  /_/ \_\_/\_/ |___/
       |__/                                           
'''

class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


def check():
    if len(sys.argv) != 4:
        print("[!] Error on arguments.")
        print("Example: {} password AWS_KEY AWS_ACCESS".format(sys.argv[0]))
        sys.exit(1)


if __name__ == "__main__":
    check()
    try:
        crypto = AESCipher(str(sys.argv[1]))
    except Exception as e:
        print("[!] Error creating AESCipher object")
        print("[!] {}".format(str(e)))
        sys.exit(1)

    print(banner)

    try:
        print("\nEncrypyed AWS_KEY: " + str(crypto.encrypt(str(sys.argv[2]))))
        print("Encrypted AWS_ACCESS: " + str(crypto.encrypt(str(sys.argv[3]))))
        print("\n[*] Keep secret the password used, and put this ciphered text into main.py script.")
        sys.exit(0)
    except Exception as e:
        print("[!] Error encrypting data")
        print("[!] {}".format(str(e)))
        sys.exit(1)


