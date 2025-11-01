import os
import io
import uuid
from datetime import datetime
from typing import Optional
from PIL import Image


class StorageService:
    """
    Local storage service for handling image files.
    Simulates Azure Blob Storage for local development.
    """

    DEFAULT_STORAGE_DIR = "./storage/equipment-images"
    DEFAULT_IMAGE_EXT = ".jpg"

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = storage_path or self.DEFAULT_STORAGE_DIR
        self._ensure_storage_directory()

    # --- Internal Utilities ---
    def _ensure_storage_directory(self) -> None:
        """Ensure the storage directory exists."""
        os.makedirs(self.storage_path, exist_ok=True)

    def _generate_filename(self, original_filename: Optional[str] = None) -> str:
        """Generate a unique filename using timestamp and UUID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex[:8]
        ext = os.path.splitext(original_filename or "")[1] or self.DEFAULT_IMAGE_EXT
        return f"{timestamp}_{unique_id}{ext}"

    # --- Core Operations ---
    def save_image(self, image_data: bytes, filename: Optional[str] = None) -> str:
        """
        Save an image to local storage.

        Args:
            image_data: Raw image bytes.
            filename: Optional original filename.

        Returns:
            str: Relative path or URL to the saved image.
        """
        if not image_data:
            raise ValueError("Image data cannot be empty.")

        try:
            # Validate image integrity
            with Image.open(io.BytesIO(image_data)) as img:
                new_filename = self._generate_filename(filename)
                file_path = os.path.join(self.storage_path, new_filename)
                img.save(file_path)

            # Return a relative URL
            return f"/storage/equipment-images/{new_filename}"

        except Exception as e:
            raise ValueError(f"Failed to save image: {e}") from e

    def delete_image(self, image_url: str) -> bool:
        """
        Delete an image from local storage.

        Args:
            image_url: Relative URL/path to the image.

        Returns:
            bool: True if the file was deleted successfully.
        """
        try:
            filename = os.path.basename(image_url)
            file_path = os.path.join(self.storage_path, filename)

            if os.path.isfile(file_path):
                os.remove(file_path)
                return True
            return False

        except OSError as e:
            # Loggable error context could be added here
            print(f"[StorageService] Failed to delete {image_url}: {e}")
            return False

    def get_image_url(self, filename: str) -> str:
        """Return the relative URL for an image filename."""
        return f"/storage/equipment-images/{filename}"


# --- Production Azure Blob Storage Placeholder ---
class AzureBlobStorageService:
    """
    Placeholder for Azure Blob Storage service.
    To be used in production with azure-storage-blob package.
    """

    def __init__(self, connection_string: str, container_name: str):
        """
        Initialize Azure Blob Storage service.

        Args:
            connection_string: Azure Blob Storage connection string.
            container_name: Name of the Azure Blob container.
        """
        self.connection_string = connection_string
        self.container_name = container_name
        # Example for production:
        # from azure.storage.blob import BlobServiceClient
        # self.client = BlobServiceClient.from_connection_string(connection_string)

    def save_image(self, image_data: bytes, filename: Optional[str] = None) -> str:
        """Upload image to Azure Blob Storage."""
        raise NotImplementedError("Azure Blob Storage not configured for local environment.")

    def delete_image(self, image_url: str) -> bool:
        """Delete image from Azure Blob Storage."""
        raise NotImplementedError("Azure Blob Storage not configured for local environment.")
