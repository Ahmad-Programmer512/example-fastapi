from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize the modern hasher
ph = PasswordHasher()

def hash(password: str) -> str:
    return ph.hash(password)

def verify(plain_password: str, hashed_password: str) -> bool:
    try:
        # argon2-cffi handles both checking and legacy passlib formats smoothly
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
    except Exception:
        # Catches edge cases if old hashes are completely malformed
        return False