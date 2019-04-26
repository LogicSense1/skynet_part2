import os
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from Crypto.PublicKey import RSA


def decrypt_valuables(f):
    # TODO: For Part 2, you'll need to decrypt the contents of this file
    # The existing scheme uploads in plaintext
    # As such, we just convert it back to ASCII and print it out
    key = RSA.importKey(open('private.pem').read())
    dsize = SHA.digest_size
    sentinel = Random.new()
    cipher = PKCS1_v1_5.new(key)
    message = cipher.decrypt(f, sentinel)
    digest = SHA.new(message[:-dsize]).digest()
    decrypt_data = message[:-dsize]
    if digest == message[-dsize:]:
        print(decrypt_data)
    else:
        print("Decryption failed")


if __name__ == "__main__":
    fn = input("Which file in pastebot.net does the botnet master want to view? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    decrypt_valuables(f)
