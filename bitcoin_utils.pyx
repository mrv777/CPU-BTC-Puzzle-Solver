import coincurve
import hashlib
import base58

def generate_bitcoin_address(private_key_hex: str) -> str:
    cdef bytes private_key_bytes = bytes.fromhex(private_key_hex)
    cdef object public_key = coincurve.PublicKey.from_valid_secret(private_key_bytes)
    cdef bytes public_key_bytes = public_key.format(compressed=True)
    
    cdef bytes sha256_hash = hashlib.sha256(public_key_bytes).digest()
    cdef bytes ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    
    cdef bytes version_byte = b'\x00'
    cdef bytes extended_ripemd160 = version_byte + ripemd160_hash
    
    cdef bytes checksum = hashlib.sha256(hashlib.sha256(extended_ripemd160).digest()).digest()[:4]
    cdef bytes binary_address = extended_ripemd160 + checksum
    
    return base58.b58encode(binary_address).decode('utf-8')