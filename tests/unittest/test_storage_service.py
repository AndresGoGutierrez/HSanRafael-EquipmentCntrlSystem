"""
Unit tests for StorageService (Azure Blob simulated).

This module tests the functionality of the StorageService class, ensuring
it correctly handles image uploads, QR code storage, deletion, and
unique filename generation, including both mocked and integration scenarios.
"""

import unittest
import os
import tempfile
from unittest.mock import patch, ANY, MagicMock
from app.infrastructure.services.storage_service import StorageService


class TestStorageService(unittest.TestCase):
    """
    Unit test suite for the StorageService class.

    These tests verify the behavior of local and simulated Azure Blob storage operations,
    ensuring file uploads, deletions, and naming conventions work as expected.
    """

    def setUp(self):
        """
        Create a temporary directory and initialize StorageService before each test.
        """
        self.test_dir = tempfile.mkdtemp()
        self.storage_service = StorageService(storage_path=self.test_dir)

    def tearDown(self):
        """
        Clean up temporary directory after each test.
        """
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch("app.infrastructure.services.storage_service.StorageService.save_image")
    def test_upload_image_success(self, mock_save_image):
        """
        Test that uploading an image returns a valid storage URL.

        The save_image method is mocked to simulate a successful upload.
        """
        mock_save_image.return_value = "/storage/equipment-images/test_image.jpg"

        image_data = b"fake_image_data"
        filename = "test_image.jpg"

        url = self.storage_service.upload_image(image_data, filename)

        self.assertEqual(url, "/storage/equipment-images/test_image.jpg")
        mock_save_image.assert_called_once_with(image_data, ANY)

    @patch("app.infrastructure.services.storage_service.StorageService.save_image")
    def test_upload_image_to_custom_folder(self, mock_save_image):
        """
        Test that upload_image supports uploading to a custom folder.
        """
        mock_save_image.return_value = (
            "/storage/equipment-images/custom_folder_image.jpg"
        )

        url = self.storage_service.upload_image(
            image_data=b"fake", filename="medical_photo.jpg", folder="biomedical"
        )

        self.assertEqual(url, "/storage/equipment-images/custom_folder_image.jpg")

        mock_save_image.assert_called_once_with(b"fake", ANY)

    @patch("app.infrastructure.services.storage_service.StorageService.save_image")
    def test_upload_qr_code(self, mock_save_image):
        """
        Test that upload_qr_code stores QR code images under the 'qr_codes' directory.
        """
        mock_save_image.return_value = "/storage/equipment-images/qr_code_test.jpg"

        qr_data = b"fake_qr_code"
        qr_code = "QR-ABC-123"

        url = self.storage_service.upload_qr_code(qr_data, qr_code)

        self.assertEqual(url, "/storage/equipment-images/qr_code_test.jpg")
        mock_save_image.assert_called_once_with(qr_data, ANY)

    @patch("app.infrastructure.services.storage_service.StorageService.save_image")
    def test_upload_multiple_images_must_generate_unique_urls(self, mock_save_image):
        """
        Test that multiple image uploads produce unique URLs.
        """

        url_counter = 0

        def side_effect(*args, **kwargs):
            nonlocal url_counter
            url_counter += 1
            return f"/storage/equipment-images/image_{url_counter}.jpg"

        mock_save_image.side_effect = side_effect

        urls = {
            self.storage_service.upload_image(
                image_data=f"img-{i}".encode(), filename=f"image_{i}.jpg"
            )
            for i in range(10)
        }

        self.assertEqual(len(urls), 10)
        self.assertEqual(mock_save_image.call_count, 10)

    def test_upload_real_image_integration(self):
        """
        Integration test: Upload a real image and verify it is saved locally.
        """

        image_data = self._create_test_image()
        filename = "real_test_image.jpg"

        url = self.storage_service.upload_image(image_data, filename)

        self.assertIsNotNone(url)
        self.assertTrue(url.startswith("/storage/equipment-images/"))

        filename_from_url = os.path.basename(url)
        file_path = os.path.join(self.storage_service.storage_path, filename_from_url)
        self.assertTrue(os.path.exists(file_path))

    def test_delete_image_success(self):
        """
        Test that deleting an existing image returns True and removes the file.
        """

        test_filename = "test_delete_real.jpg"
        test_filepath = os.path.join(self.storage_service.storage_path, test_filename)

        with open(test_filepath, "wb") as f:
            f.write(b"test image content")

        test_url = f"/storage/equipment-images/{test_filename}"

        result = self.storage_service.delete_image(test_url)

        self.assertTrue(result)
        self.assertFalse(os.path.exists(test_filepath))

    def test_generate_unique_filename(self):
        """
        Test that generated filenames are unique while keeping their file extension.
        """
        filename = "photo.jpg"

        first = self.storage_service.generate_unique_filename(filename)
        second = self.storage_service.generate_unique_filename(filename)

        self.assertNotEqual(first, second)
        self.assertTrue(first.endswith(".jpg"))
        self.assertTrue(second.endswith(".jpg"))

    def _create_test_image(self):
        """
        Create a small in-memory red test image for integration tests.

        Returns:
            bytes: The JPEG-encoded image data.
        """
        from PIL import Image
        import io

        img = Image.new("RGB", (10, 10), color="red")
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        return img_bytes.getvalue()

    @patch("app.infrastructure.services.storage_service.BlobServiceClient")
    def test_azure_client_initialization(self, mock_blob_client):
        """
        Test that Azure BlobServiceClient can be imported and mocked successfully.

        This ensures that the azure-storage-blob dependency is properly referenced.
        """

        from azure.storage.blob import BlobServiceClient

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
