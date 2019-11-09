import os
import hashlib
import hmac

SALT = os.environ["HASH_SECRET"]


def hash_new_password(password: str) -> bytes:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    pw_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000)
    return pw_hash


def is_correct_password(pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000)
    )
