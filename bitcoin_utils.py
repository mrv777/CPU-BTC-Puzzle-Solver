import hashlib
from coincurve import PrivateKey
import base58

def generate_bitcoin_address(private_key):
    # Generate public key using coincurve
    pk = PrivateKey(bytes.fromhex(private_key))
    public_key = pk.public_key.format(compressed=True)
    
    # Perform SHA-256 and RIPEMD-160 hashing
    hash160 = hashlib.new('ripemd160', hashlib.sha256(public_key).digest()).digest()
    
    # Add version byte and calculate checksum
    versioned_hash = b'\x00' + hash160
    checksum = hashlib.sha256(hashlib.sha256(versioned_hash).digest()).digest()[:4]
    
    # Combine and encode to base58
    return base58.b58encode(versioned_hash + checksum).decode('utf-8')
