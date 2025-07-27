"""
Cryptographic utilities for secure random number generation and HMAC calculation.
"""

import secrets
import hashlib
import hmac


class CryptoUtils:
    """Utilities for cryptographically secure operations."""
    
    def __init__(self):
        """Initialize crypto utilities."""
        self.key_length = 32  # 256 bits
    
    def generate_secure_key(self):
        """
        Generate a cryptographically secure 256-bit random key.
        
        Returns:
            str: Hexadecimal representation of the secure key
        """
        key_bytes = secrets.token_bytes(self.key_length)
        return key_bytes.hex().upper()
    
    def generate_secure_random(self, max_value):
        """
        Generate a cryptographically secure random integer in range [0, max_value).
        
        Args:
            max_value: Upper bound (exclusive) for random number
            
        Returns:
            int: Secure random integer in range [0, max_value)
        """
        return secrets.randbelow(max_value)
    
    def calculate_hmac(self, key_hex, message):
        """
        Calculate HMAC-SHA3-256 for the given key and message.
        
        Args:
            key_hex: Hexadecimal string representation of the key
            message: Message to authenticate (will be converted to string)
            
        Returns:
            str: Hexadecimal representation of the HMAC
        """
        try:
            # Convert hex key to bytes
            key_bytes = bytes.fromhex(key_hex)
            
            # Convert message to bytes
            message_bytes = str(message).encode('utf-8')
            
            # Calculate HMAC using SHA3-256
            hmac_obj = hmac.new(key_bytes, message_bytes, hashlib.sha3_256)
            
            return hmac_obj.hexdigest().upper()
            
        except Exception as e:
            raise ValueError(f"HMAC calculation failed: {e}")
    
    def verify_hmac(self, key_hex, message, expected_hmac):
        """
        Verify HMAC against expected value.
        
        Args:
            key_hex: Hexadecimal string representation of the key
            message: Original message
            expected_hmac: Expected HMAC value
            
        Returns:
            bool: True if HMAC matches, False otherwise
        """
        try:
            calculated_hmac = self.calculate_hmac(key_hex, message)
            return hmac.compare_digest(calculated_hmac, expected_hmac.upper())
        except Exception:
            return False
