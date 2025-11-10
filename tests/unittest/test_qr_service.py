"""
Unit tests for QR code generation service adapted to project implementation.
"""

import unittest
from io import BytesIO
from PIL import Image
from app.infrastructure.services.qr_service import QRCodeService


class TestQRCodeService(unittest.TestCase):
    """Unit tests for QRCodeService."""

    def setUp(self):
        """Initialize a QRCodeService instance before each test."""
        self.qr_service = QRCodeService()

    # ----------------------------------------------------------
    def test_generate_unique_code_creates_different_values(self):
        """generate_unique_code should return unique non-empty values."""
        code1 = self.qr_service.generate_unique_code()
        code2 = self.qr_service.generate_unique_code()

        self.assertIsNotNone(code1)
        self.assertIsNotNone(code2)
        self.assertNotEqual(code1, code2)
        self.assertGreater(len(code1), 0)
        self.assertGreater(len(code2), 0)

    # ----------------------------------------------------------
    def test_generate_qr_image_returns_valid_png_bytes(self):
        """generate_qr_image must return PNG bytes."""
        data = "TEST-QR-12345"

        qr_bytes = self.qr_service.generate_qr_image(data)

        self.assertIsInstance(qr_bytes, bytes)
        self.assertGreater(len(qr_bytes), 0)

        # Validate PNG format
        image = Image.open(BytesIO(qr_bytes))
        self.assertEqual(image.format, "PNG")

    # ----------------------------------------------------------
    def test_generate_qr_image_with_custom_size_affects_dimensions(self):
        """generate_qr_image must allow custom sizing configuration."""
        small_qr = self.qr_service.generate_qr_image("DATA", size=5, border=2)
        large_qr = self.qr_service.generate_qr_image("DATA", size=15, border=6)

        small_img = Image.open(BytesIO(small_qr))
        large_img = Image.open(BytesIO(large_qr))

        # Larger settings should produce larger image
        self.assertLess(small_img.size[0], large_img.size[0])
        self.assertLess(small_img.size[1], large_img.size[1])

    # ----------------------------------------------------------
    def test_generate_qr_for_equipment_using_available_methods(self):
        """
        Simulate generate_qr_for_equipment by:
        1. Generating a unique code
        2. Building QR data using create_equipment_qr_data()
        3. Generating QR image
        """
        equipment_id = 42

        qr_code = self.qr_service.generate_unique_code()
        qr_data = self.qr_service.create_equipment_qr_data(equipment_id, qr_code)
        qr_image = self.qr_service.generate_qr_image(qr_data)

        self.assertIsNotNone(qr_code)
        self.assertIn(str(equipment_id), qr_data)
        self.assertIsInstance(qr_image, bytes)

        image = Image.open(BytesIO(qr_image))
        self.assertEqual(image.format, "PNG")

    # ----------------------------------------------------------
    def test_generate_unique_code_multiple_calls(self):
        """Multiple calls should return unique codes."""
        codes = {self.qr_service.generate_unique_code() for _ in range(100)}
        self.assertEqual(len(codes), 100)


if __name__ == "__main__":
    unittest.main()
