"""
Unit tests for the security module:
- Password hashing (bcrypt)
- JWT generation and validation
"""

import unittest
from datetime import timedelta
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)


class TestPasswordHashing(unittest.TestCase):
    """Unit tests for password hashing and verification."""

    def setUp(self):
        """Common password for tests."""
        self.password = "SecurePassword123!"

    def test_hash_password_generates_valid_bcrypt(self):
        """Password hashing should produce a non-reversible bcrypt hash."""
        hashed = get_password_hash(self.password)

        self.assertIsNotNone(hashed)
        self.assertNotEqual(self.password, hashed)
        self.assertTrue(hashed.startswith("$2b$"))  # bcrypt indicator

    def test_verify_correct_password(self):
        """verify_password should confirm correct credentials."""
        hashed = get_password_hash(self.password)

        self.assertTrue(verify_password(self.password, hashed))

    def test_verify_incorrect_password(self):
        """verify_password should reject incorrect password."""
        hashed = get_password_hash(self.password)

        self.assertFalse(verify_password("WrongPassword456!", hashed))

    def test_hashing_same_password_generates_different_salts(self):
        """Hashing the same password should produce different values (salt)."""
        hash1 = get_password_hash(self.password)
        hash2 = get_password_hash(self.password)

        self.assertNotEqual(hash1, hash2)
        self.assertTrue(verify_password(self.password, hash1))
        self.assertTrue(verify_password(self.password, hash2))


class TestJWTTokens(unittest.TestCase):
    """Unit tests for JWT token creation and decoding."""

    def test_create_access_token_returns_valid_string(self):
        """Token creation should return a non-empty string."""
        token = create_access_token({"sub": "testuser", "user_id": 1})

        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 10)  # basic check to avoid trivial strings

    def test_token_with_expiration_is_decodable(self):
        """Token should include expiration when a custom timedelta is passed."""
        expires_delta = timedelta(minutes=15)
        token = create_access_token({"sub": "testuser"}, expires_delta)

        payload = decode_access_token(token)

        self.assertIsNotNone(payload)
        self.assertEqual(payload["sub"], "testuser")
        self.assertIn("exp", payload)

    def test_decode_valid_token_returns_payload(self):
        """decode_access_token should correctly decode valid tokens."""
        token = create_access_token({"sub": "testuser", "user_id": 1, "role": "ti"})

        payload = decode_access_token(token)

        self.assertIsNotNone(payload)
        self.assertEqual(payload["sub"], "testuser")
        self.assertEqual(payload["user_id"], 1)
        self.assertEqual(payload["role"], "ti")

    def test_decode_invalid_token_returns_none(self):
        """Invalid or unreadable tokens should return None."""
        payload = decode_access_token("invalid.token.here")

        self.assertIsNone(payload)

    def test_decode_tampered_token_returns_none(self):
        """Tampering with the token should cause decoding failure."""
        token = create_access_token({"sub": "testuser"})

        tampered_token = token[:-5] + "XXXXX"  # alter the signature

        payload = decode_access_token(tampered_token)

        self.assertIsNone(payload)


if __name__ == "__main__":
    unittest.main()
