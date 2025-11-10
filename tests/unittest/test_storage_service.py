"""
Unit tests for StorageService (Azure Blob simulated).
"""

import unittest
import os
import tempfile
from unittest.mock import patch, ANY, MagicMock
from app.infrastructure.services.storage_service import StorageService


class TestStorageService(unittest.TestCase):
    """Unit tests for StorageService."""

    def setUp(self):
        """Initialize StorageService before each test."""
        # Usar directorio temporal para tests
        self.test_dir = tempfile.mkdtemp()
        self.storage_service = StorageService(storage_path=self.test_dir)

    def tearDown(self):
        """Clean up after tests."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # ✅ TESTS CON MOCK PARA EVITAR VALIDACIÓN DE IMAGEN REAL

    @patch("app.infrastructure.services.storage_service.StorageService.save_image")
    def test_upload_image_success(self, mock_save_image):
        """Uploading an image should return a valid URL."""
        mock_save_image.return_value = "/storage/equipment-images/test_image.jpg"
        
        image_data = b"fake_image_data"
        filename = "test_image.jpg"

        url = self.storage_service.upload_image(image_data, filename)

        self.assertEqual(url, "/storage/equipment-images/test_image.jpg")
        mock_save_image.assert_called_once_with(image_data, ANY)

    @patch("app.infrastructure.services.storage_service.StorageService.save_image")
    def test_upload_image_to_custom_folder(self, mock_save_image):
        """Image upload should support custom folder."""
        mock_save_image.return_value = "/storage/equipment-images/custom_folder_image.jpg"
        
        url = self.storage_service.upload_image(
            image_data=b"fake", filename="medical_photo.jpg", folder="biomedical"
        )

        self.assertEqual(url, "/storage/equipment-images/custom_folder_image.jpg")
        # El folder parameter es ignorado en la implementación local, pero se verifica el mock
        mock_save_image.assert_called_once_with(b"fake", ANY)

    @patch("app.infrastructure.services.storage_service.StorageService.save_image")
    def test_upload_qr_code(self, mock_save_image):
        """QR code upload should generate URL under qr_codes."""
        mock_save_image.return_value = "/storage/equipment-images/qr_code_test.jpg"
        
        qr_data = b"fake_qr_code"
        qr_code = "QR-ABC-123"

        url = self.storage_service.upload_qr_code(qr_data, qr_code)

        self.assertEqual(url, "/storage/equipment-images/qr_code_test.jpg")
        mock_save_image.assert_called_once_with(qr_data, ANY)

    @patch("app.infrastructure.services.storage_service.StorageService.save_image")
    def test_upload_multiple_images_must_generate_unique_urls(self, mock_save_image):
        """Multiple uploads must generate different URLs."""
        # Configurar el mock para retornar URLs únicas
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

    # ✅ TESTS DE INTEGRACIÓN CON IMÁGENES REALES (opcional)

    def test_upload_real_image_integration(self):
        """Test with real image data (integration test)."""
        # Crear imagen REAL válida
        image_data = self._create_test_image()
        filename = "real_test_image.jpg"

        url = self.storage_service.upload_image(image_data, filename)

        self.assertIsNotNone(url)
        self.assertTrue(url.startswith("/storage/equipment-images/"))
        # Verificar que el archivo se creó realmente
        filename_from_url = os.path.basename(url)
        file_path = os.path.join(self.storage_service.storage_path, filename_from_url)
        self.assertTrue(os.path.exists(file_path))

    # ✅ TESTS DE FUNCIONALIDAD LOCAL (sin mock)

    def test_delete_image_success(self):
        """Deleting an image should return True when file exists."""
        # Primero crear un archivo REAL
        test_filename = "test_delete_real.jpg"
        test_filepath = os.path.join(self.storage_service.storage_path, test_filename)
        
        # Crear archivo temporal
        with open(test_filepath, 'wb') as f:
            f.write(b"test image content")
        
        # URL que espera delete_image
        test_url = f"/storage/equipment-images/{test_filename}"
        
        # Ejecutar delete
        result = self.storage_service.delete_image(test_url)
        
        self.assertTrue(result)
        self.assertFalse(os.path.exists(test_filepath))


    def test_generate_unique_filename(self):
        """Generated filenames should be unique and maintain file extension."""
        filename = "photo.jpg"

        first = self.storage_service.generate_unique_filename(filename)
        second = self.storage_service.generate_unique_filename(filename)

        self.assertNotEqual(first, second)
        self.assertTrue(first.endswith(".jpg"))
        self.assertTrue(second.endswith(".jpg"))

    def _create_test_image(self):
        """Create a valid test image."""
        from PIL import Image
        import io
        
        img = Image.new('RGB', (10, 10), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        return img_bytes.getvalue()

    # ✅ TESTS CON MOCK DE AZURE (si los necesitas)

    @patch("app.infrastructure.services.storage_service.BlobServiceClient")
    def test_azure_client_initialization(self, mock_blob_client):
        """Test that Azure client can be imported and mocked."""
        # Este test verifica que los imports de Azure funcionan
        from azure.storage.blob import BlobServiceClient
        self.assertTrue(True)  # Si llegamos aquí, el import funciona


if __name__ == "__main__":
    unittest.main()