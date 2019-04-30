from Crypto.Hash import SHA256
from Crypto.Random import random
from lib.helpers import read_hex
from Crypto.PublicKey import RSA
from Crypto import Random

# Project TODO: Is this the best choice of prime? Why? Why not? Feel free to replacasddsae!

# 1536 bit safe prime for Diffie-Hellman key exchange
# obtained from RFC 3526
raw_prime = """FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF"""
# Convert from the value supplied in the RFC to an integer
prime = read_hex(raw_prime)


# Project TODO: write the appropriate code to perform DH key exchange


def create_dh_key():
    # Creates a Diffie-Hellman key
    # Returns (public, private)
    a = random.randint(0, prime)  # Generate a random number in range of RFC3526
    b = pow(2, a, prime)  # calculate the g^a or g^b used to exchange each other's secret
    return b, a


def calculate_dh_secret(their_public, my_private):
    # Calculate the shared secret
    shared_secret = pow(their_public, my_private, prime)
    # Hash the value so that:
    # (a) There's no bias in the bits of the output
    #     (there may be bias if the shared secret is used raw)
    # (b) We can convert to raw bytes easily
    # (c) We could add additional information if we wanted
    # Feel free to change SHA256 to a different value if more appropriate
    shared_hash = SHA256.new(bytes(str(shared_secret), "ascii")).hexdigest()
    return shared_hash


def calculate_iv(their_public, my_private):
    shared_secret = pow(their_public, my_private, prime)
    return shared_secret


# this function will be used once to create the public and private key pair
# for the master used to sign or asymmetric encryption
def generate_rsa_key():
    random_generator = Random.new().read
    # use the public tools from pycrypto to create the key pair with the random seed
    rsa = RSA.generate(2048, random_generator)
    private_pem = rsa.exportKey()
    # write private and public key to the .pem file
    with open('private.pem', 'wb') as private_key_file:
        private_key_file.write(private_pem)
    public_pem = rsa.publickey().exportKey()
    with open('public.pem', 'wb') as public_key_file:
        public_key_file.write(public_pem)
