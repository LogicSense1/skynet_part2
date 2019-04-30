import os
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from Crypto.PublicKey import RSA
from lib.files import verify_file


# check if the received file includes signature. If so, remove it.
def remove_signature(f):
    if verify_file(f):
        lines = f.split(bytes("\n\n", "ascii"), 1)
        message = lines[-1]
        return message
    else:
        return f


def decrypt_valuables(f):
    # TODO: For Part 2, you'll need to decrypt the contents of this file
    # first import the private key for RSA decryption
    key = RSA.importKey(open('private.pem').read())
    # determine the size of hash included in the message
    dsize = SHA.digest_size
    # define the object of PKCS1_v1_5 as cipher
    cipher = PKCS1_v1_5.new(key)
    # as the api doc said, a random number will be used for decryption
    sentinel = Random.new()
    message = cipher.decrypt(f, sentinel)
    # split the hash value from the message based on the dsize
    digest = SHA.new(message[:-dsize]).digest()
    decrypt_data = message[:-dsize]
    # split each line of the massage
    lines = decrypt_data.split(bytes("\n", "ascii"))
    # use the hash matching to check if the decryption is successful
    if digest == message[-dsize:]:
        for i in lines:
            print(i.decode('ascii'))
    else:
        print("Decryption failed")


if __name__ == "__main__":
    fn = input("Which file in pastebot.net does the botnet master want to view? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os._exit(0)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    f = remove_signature(f)
    decrypt_valuables(f)
