import os
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto import Random


def generate_rsa_key():
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)
    private_pem = rsa.exportKey()
    with open('private.pem', 'wb') as private_key_file:
        private_key_file.write(private_pem)
    public_pem = rsa.publickey().exportKey()
    with open('public.pem', 'wb') as public_key_file:
        public_key_file.write(public_pem)


def sign_file(f):
    # TODO: For Part 2, you'll use public key crypto here
    # The existing scheme just ensures the updates start with the line 'Caesar'
    # This is naive -- replace it with something better!
    key = RSA.importKey(open('private.pem').read())
    h = SHA.new(f)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(h)
    return bytes(signature) + f


if __name__ == "__main__":
    fn = input("Which file in pastebot.net should be signed? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    generate_rsa_key()
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    signed_f = sign_file(f)
    signed_fn = os.path.join("pastebot.net", fn + ".signed")
    out = open(signed_fn, "wb")
    out.write(signed_f)
    out.close()
    print("Signed file written to", signed_fn)
