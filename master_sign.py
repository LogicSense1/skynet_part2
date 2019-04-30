import os
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def sign_file(f):
    # TODO: For Part 2, you'll use public key crypto here
    # first read the private key from the file to sign the file
    key = RSA.importKey(open('private.pem').read())
    # Calculate the SHA256 value for original file for signing
    h = SHA256.new(f)
    # define the object of PKCS1_v1_5 for signing
    signer = PKCS1_v1_5.new(key)
    # use the private key to encrypt the hash for signing
    signature = signer.sign(h)
    # return the signature followed by the data stream of original file
    # use string '\n\n' for the program to identify the position to split the signed file into two parts
    return bytes(signature) + '\n\n'.encode('ascii') + f


if __name__ == "__main__":
    fn = input("Which file in pastebot.net should be signed? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    signed_f = sign_file(f)
    signed_fn = os.path.join("pastebot.net", fn + ".signed")
    out = open(signed_fn, "wb")
    out.write(signed_f)
    out.close()
    print("Signed file written to", signed_fn)
