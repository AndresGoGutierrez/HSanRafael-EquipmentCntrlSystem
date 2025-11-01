import io
import uuid
import base64
import qrcode
from typing import Optional


class QRCodeService:
    """Service for generating and encoding QR codes."""

    # --- Configuration constants ---
    DEFAULT_BOX_SIZE = 10
    DEFAULT_BORDER = 2
    DEFAULT_FORMAT = "PNG"

    # --- Unique Code Generation ---
    @staticmethod
    def generate_unique_code(prefix: str = "HSR") -> str:
        """
        Generate a unique QR code identifier.

        Args:
            prefix: Optional prefix for code identification (default "HSR")

        Returns:
            str: A unique formatted QR code string
        """
        unique_part = uuid.uuid4().hex[:12].upper()
        return f"{prefix}-{unique_part}"

    # --- QR Code Image Generation ---
    @staticmethod
    def generate_qr_image(
        data: str,
        size: int = DEFAULT_BOX_SIZE,
        border: int = DEFAULT_BORDER,
        fill_color: str = "black",
        back_color: str = "white",
    ) -> bytes:
        """
        Generate a QR code image as bytes.

        Args:
            data: Data to encode in QR code
            size: Size of QR code (box_size parameter)
            border: Border size in boxes
            fill_color: Foreground color
            back_color: Background color

        Returns:
            bytes: QR code image as bytes (PNG)
        """
        if not data:
            raise ValueError("QR data cannot be empty.")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Convert image to byte array
        with io.BytesIO() as buffer:
            img.save(buffer, format=QRCodeService.DEFAULT_FORMAT)
            return buffer.getvalue()

    # --- Base64 Encoded QR ---
    @staticmethod
    def generate_qr_base64(
        data: str,
        size: int = DEFAULT_BOX_SIZE,
        border: int = DEFAULT_BORDER,
    ) -> str:
        """
        Generate a QR code as base64-encoded string.

        Args:
            data: Data to encode
            size: QR code size
            border: Border size

        Returns:
            str: Base64 encoded QR code image
        """
        qr_bytes = QRCodeService.generate_qr_image(data, size, border)
        return base64.b64encode(qr_bytes).decode("utf-8")

    # --- Equipment-specific QR Data ---
    @staticmethod
    def create_equipment_qr_data(equipment_id: int, qr_code: str) -> str:
        """
        Create formatted data string for equipment QR code.

        Args:
            equipment_id: Equipment database ID
            qr_code: Unique QR code identifier

        Returns:
            str: Formatted QR code data string
        """
        if not equipment_id or not qr_code:
            raise ValueError("Both equipment_id and qr_code are required.")

        return f"EQUIPMENT|ID:{equipment_id}|CODE:{qr_code}"
