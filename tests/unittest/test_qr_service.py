"""
Unit tests for the QRCodeService component.

These tests validate the core functionality of the QR code generation service,
including code uniqueness, image generation, format verification, and custom
sizing options. The tests ensure that QR codes can be generated correctly for
equipment records within the system.
"""

import unittest
from io import BytesIO
from PIL import Image
from app.infrastructure.services.qr_service import QRCodeService


class TestQRCodeService(unittest.TestCase):
    """
    Unit tests for the QRCodeService.

    This class verifies that the service correctly generates unique codes and
    valid QR images in PNG format, handles custom size configurations, and
    integrates properly with higher-level utility methods for equipment QR
    generation.
    """

    def setUp(self):
        """
        Initialize the test environment before each test case.

        Creates an instance of the `QRCodeService` to be used across all tests.
        """
        self.qr_service = QRCodeService()

    # ----------------------------------------------------------
    def test_generate_unique_code_creates_different_values(self):
        """
        Test that `generate_unique_code` returns unique and non-empty values.

        Verifies:
        - Each generated code is not None.
        - Codes from multiple calls are distinct.
        - Generated strings have non-zero length.
        """
        code1 = self.qr_service.generate_unique_code()
        code2 = self.qr_service.generate_unique_code()

        self.assertIsNotNone(code1)
        self.assertIsNotNone(code2)
        self.assertNotEqual(code1, code2)
        self.assertGreater(len(code1), 0)
        self.assertGreater(len(code2), 0)

    # ----------------------------------------------------------
    def test_generate_qr_image_returns_valid_png_bytes(self):
        """
        Test that `generate_qr_image` returns valid PNG image bytes.

        Verifies:
        - The returned object is of type `bytes`.
        - The byte sequence is not empty.
        - The resulting image format is correctly recognized as PNG.
        """
        data = "TEST-QR-12345"

        qr_bytes = self.qr_service.generate_qr_image(data)

        self.assertIsInstance(qr_bytes, bytes)
        self.assertGreater(len(qr_bytes), 0)

        # Validate PNG format
        image = Image.open(BytesIO(qr_bytes))
        self.assertEqual(image.format, "PNG")

    # ----------------------------------------------------------
    def test_generate_qr_image_with_custom_size_affects_dimensions(self):
        """
        Test that `generate_qr_image` responds to custom size and border parameters.

        Verifies that changing size and border values alters the resulting image
        dimensions as expected.
        """
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
        Test simulated workflow of QR generation for an equipment entity.

        This test performs the equivalent of a `generate_qr_for_equipment` operation:
        1. Generate a unique code.
        2. Build the equipment QR data string using `create_equipment_qr_data()`.
        3. Generate the corresponding QR image in PNG format.

        Verifies that:
        - The generated code and data are valid.
        - The data string contains the equipment ID.
        - The QR image is valid and decodable as a PNG.
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
        """
        Test that multiple invocations of `generate_unique_code` yield unique results.

        Generates 100 unique codes and ensures no collisions occur.
        """
        codes = {self.qr_service.generate_unique_code() for _ in range(100)}
        self.assertEqual(len(codes), 100)


if __name__ == "__main__":
    unittest.main()
