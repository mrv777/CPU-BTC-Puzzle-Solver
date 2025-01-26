import coincurve
import hashlib
import base58

def generate_bitcoin_address(private_key_hex: str) -> str:
    # Pre-allocate the version byte
    cdef bytes version_byte = b'\x00'
    cdef bytes private_key_bytes = bytes.fromhex(private_key_hex)
    
    # Get compressed public key directly
    cdef bytes public_key_bytes = coincurve.PublicKey.from_valid_secret(private_key_bytes).format(compressed=True)
    
    # Chain the hash operations without intermediate variables
    cdef bytes ripemd160_hash = hashlib.new('ripemd160', hashlib.sha256(public_key_bytes).digest()).digest()
    cdef bytes extended_ripemd160 = version_byte + ripemd160_hash
    
    # Compute double SHA256 checksum in one step
    cdef bytes checksum = hashlib.sha256(hashlib.sha256(extended_ripemd160).digest()).digest()[:4]
    
    # Encode final result directly
    return base58.b58encode(extended_ripemd160 + checksum).decode('utf-8')