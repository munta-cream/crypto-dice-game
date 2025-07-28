import hashlib
import hmac

def verify_hmac(key, value, expected_hmac):
    try:
        key_bytes = bytes.fromhex(key)
        calculated_hmac = hmac.new(key_bytes, str(value).encode(), hashlib.sha3_256).hexdigest().upper()
        is_valid = calculated_hmac == expected_hmac.upper() 
        print(f"Key: {key}")
        print(f"Value: {value}")
        print(f"Expected HMAC: {expected_hmac}")
        print(f"Calculated HMAC: {calculated_hmac}")
        print(f"Valid: {is_valid}")  
        return is_valid 
    except Exception as e:
        print(f"Error: {e}")
        return False
def main():
    print("HMAC Verification Tool")
    print("Enter the values from the game to verify the computer didn't cheat:")
    print()
    key = input("Enter the KEY (hex): ").strip()
    value = input("Enter the value: ").strip()
    expected_hmac = input("Enter the HMAC: ").strip() 
    print("\nVerifying...")
    verify_hmac(key, value, expected_hmac)
if __name__ == "__main__":
    main()