import hashlib
import ecdsa
import base58

def generate_bitcoin_address(private_key):
    # Generate public key
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    
    # Get compressed public key
    public_key = vk.to_string("compressed")
    
    # Perform SHA-256 hashing on the compressed public key
    sha256_hash = hashlib.sha256(public_key).digest()
    
    # Perform RIPEMD-160 hashing on the result of SHA-256
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    hash160 = ripemd160.digest()
    
    # Add version byte in front of RIPEMD-160 hash (0x00 for Main Network)
    versioned_hash = b'\x00' + hash160
    
    # Perform double SHA-256 hash on the extended RIPEMD-160 result
    sha256_1 = hashlib.sha256(versioned_hash).digest()
    sha256_2 = hashlib.sha256(sha256_1).digest()
    
    # Take the first 4 bytes of the second SHA-256 hash for checksum
    checksum = sha256_2[:4]
    
    # Add the 4 checksum bytes from stage 7 at the end of extended RIPEMD-160 hash from stage 4
    binary_address = versioned_hash + checksum
    
    # Convert the result from a byte string into base58
    bitcoin_address = base58.b58encode(binary_address).decode('utf-8')
    
    return bitcoin_address