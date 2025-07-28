import secrets
import hashlib
import hmac


class CryptoUtils:
    
    def __init__(self):
        self.key_length = 32  # 256 bits
    
    def generate_secure_key(self):
        key_bytes = secrets.token_bytes(self.key_length)
        return key_bytes.hex().upper()
    
    def generate_secure_random(self, max_value):
        return secrets.randbelow(max_value)
    
    def calculate_hmac(self, key_hex, message):
        try:
            key_bytes = bytes.fromhex(key_hex)
            message_bytes = str(message).encode('utf-8')
            hmac_obj = hmac.new(key_bytes, message_bytes, hashlib.sha3_256)   
            return hmac_obj.hexdigest().upper()   
        except Exception as e:
            raise ValueError(f"HMAC calculation failed: {e}")
    
    def verify_hmac(self, key_hex, message, expected_hmac):
        try:
            calculated_hmac = self.calculate_hmac(key_hex, message)
            return hmac.compare_digest(calculated_hmac, expected_hmac.upper())
        except Exception:
            return False
