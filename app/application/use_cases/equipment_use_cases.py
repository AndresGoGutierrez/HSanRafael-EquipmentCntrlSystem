from typing import List, Optional
from fastapi import HTTPException, status, UploadFile
from app.domain.entities.equipment import Equipment, EquipmentType, EquipmentCategory
from app.domain.ports.equipment_repository import EquipmentRepository
from app.infrastructure.services.qr_service import QRCodeService
from app.infrastructure.services.storage_service import StorageService


class EquipmentUseCases:
    """Use cases for managing equipment lifecycle and related operations."""

    def __init__(
        self,
        equipment_repository: EquipmentRepository,
        qr_service: QRCodeService,
        storage_service: StorageService,
    ):
        self.equipment_repository = equipment_repository
        self.qr_service = qr_service
        self.storage_service = storage_service

    # Create Equipment

    def create_equipment(
        self,
        name: str,
        equipment_type: EquipmentType,
        category: EquipmentCategory,
        description: Optional[str] = None,
        serial_number: Optional[str] = None,
        image_file: Optional[UploadFile] = None,
    ) -> Equipment:
        """Create a new equipment entry."""

        # Validate serial number uniqueness
        if serial_number and self.equipment_repository.get_by_serial_number(
            serial_number
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Serial number already exists.",
            )

        # Generate QR code for frequent-use equipment
        qr_code = (
            self.qr_service.generate_unique_code()
            if equipment_type == EquipmentType.FRECUENTE
            else None
        )

        # Handle biomedical equipment image upload
        image_url = None
        if category == EquipmentCategory.BIOMEDICO:
            if not image_file:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Biomedical equipment requires an image.",
                )

            image_data = image_file.file.read()
            image_url = self.storage_service.save_image(image_data, image_file.filename)

        # Build equipment entity
        equipment = Equipment(
            id=None,
            name=name.strip(),
            equipment_type=equipment_type,
            category=category,
            serial_number=serial_number,
            qr_code=qr_code,
            image_url=image_url,
            description=description.strip() if description else None,
            is_active=True,
        )

        return self.equipment_repository.create(equipment)

    # Retrieval Methods

    def get_equipment_by_id(self, equipment_id: int) -> Equipment:
        """Retrieve an equipment item by its ID."""
        equipment = self.equipment_repository.get_by_id(equipment_id)
        if not equipment:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="Equipment not found."
            )
        return equipment

    def get_equipment_by_qr(self, qr_code: str) -> Equipment:
        """Retrieve equipment by its QR code."""
        equipment = self.equipment_repository.get_by_qr_code(qr_code)
        if not equipment:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="No equipment found for this QR code."
            )
        return equipment

    def get_equipment_by_serial(self, serial_number: str) -> Equipment:
        """Retrieve equipment by its serial number."""
        equipment = self.equipment_repository.get_by_serial_number(serial_number)
        if not equipment:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="No equipment found for this serial number.",
            )
        return equipment

    # List Equipment

    def get_all_equipment(
        self,
        skip: int = 0,
        limit: int = 100,
        equipment_type: Optional[EquipmentType] = None,
        category: Optional[EquipmentCategory] = None,
        is_active: Optional[bool] = None,
    ) -> List[Equipment]:
        """Retrieve all equipment, optionally filtered by attributes."""
        all_equipment = self.equipment_repository.get_all(skip=skip, limit=limit)

        # Apply filters safely and clearly
        filtered = [
            eq
            for eq in all_equipment
            if (equipment_type is None or eq.equipment_type == equipment_type)
            and (category is None or eq.category == category)
            and (is_active is None or eq.is_active == is_active)
        ]

        return filtered

    # Update Equipment

    def update_equipment(
        self,
        equipment_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
        image_file: Optional[UploadFile] = None,
    ) -> Equipment:
        """Update equipment information."""
        equipment = self.get_equipment_by_id(equipment_id)

        if name:
            equipment.name = name.strip()

        if description is not None:
            equipment.description = description.strip() if description else None

        if is_active is not None:
            equipment.is_active = is_active

        # Handle image replacement
        if image_file:
            if equipment.image_url:
                try:
                    self.storage_service.delete_image(equipment.image_url)
                except Exception:
                    # Log internally but don't break the update if deletion fails
                    pass

            image_data = image_file.file.read()
            equipment.image_url = self.storage_service.save_image(
                image_data, image_file.filename
            )

        return self.equipment_repository.update(equipment)

    # Delete Equipment

    def delete_equipment(self, equipment_id: int) -> bool:
        """Delete an equipment item and its image (if any)."""
        equipment = self.get_equipment_by_id(equipment_id)

        if equipment.image_url:
            try:
                self.storage_service.delete_image(equipment.image_url)
            except Exception:
                # Log and continue (don’t block deletion)
                pass

        return self.equipment_repository.delete(equipment_id)

    # QR Code Management

    def generate_qr_code_image(self, equipment_id: int) -> str:
        """Generate a base64-encoded QR code image for a given equipment."""
        equipment = self.get_equipment_by_id(equipment_id)

        if not equipment.qr_code:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="This equipment does not have a QR code assigned.",
            )

        qr_data = self.qr_service.create_equipment_qr_data(
            equipment.id, equipment.qr_code
        )
        return self.qr_service.generate_qr_base64(qr_data)
