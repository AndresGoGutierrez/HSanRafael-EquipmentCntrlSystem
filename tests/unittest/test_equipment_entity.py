"""
Unit tests for Equipment domain entity
"""
import unittest
from datetime import datetime
from app.domain.entities.equipment import (
    Equipment,
    EquipmentType,
    EquipmentCategory,
)


def _create_equipment(**kwargs) -> Equipment:
    """Factory helper for creating equipment entities with defaults."""
    defaults = {
        "id": kwargs.get("id", 1),
        "name": kwargs.get("name", "Generic Equipment"),
        "equipment_type": kwargs.get("equipment_type", EquipmentType.FRECUENTE),
        "category": kwargs.get("category", EquipmentCategory.TECNOLOGICO),
        "qr_code": kwargs.get("qr_code", "QR-DEFAULT"),
        "serial_number": kwargs.get("serial_number"),
        "image_url": kwargs.get("image_url"),
        "description": kwargs.get("description", None),
    }
    return Equipment(**defaults)


class TestEquipmentEnums(unittest.TestCase):
    """Test Equipment enumeration values"""

    def test_equipment_type_enum(self):
        self.assertEqual(EquipmentType.FRECUENTE.value, "frecuente")
        self.assertEqual(EquipmentType.NO_FRECUENTE.value, "no_frecuente")

    def test_equipment_category_enum(self):
        self.assertEqual(EquipmentCategory.TECNOLOGICO.value, "tecnologico")
        self.assertEqual(EquipmentCategory.BIOMEDICO.value, "biomedico")


class TestEquipmentEntity(unittest.TestCase):
    """Test Equipment domain behavior"""

    def test_create_frequent_equipment(self):
        equipment = _create_equipment(
            id=1,
            name="Laptop Dell",
            equipment_type=EquipmentType.FRECUENTE,
            category=EquipmentCategory.TECNOLOGICO,
            qr_code="QR123456",
            description="Laptop for testing"
        )

        self.assertEqual(equipment.id, 1)
        self.assertEqual(equipment.name, "Laptop Dell")
        self.assertEqual(equipment.qr_code, "QR123456")
        self.assertTrue(equipment.is_active)
        self.assertTrue(equipment.is_frequent())

    def test_create_non_frequent_equipment(self):
        equipment = _create_equipment(
            id=2,
            name="External Monitor",
            equipment_type=EquipmentType.NO_FRECUENTE,
            category=EquipmentCategory.TECNOLOGICO,
            serial_number="SN987654"
        )

        self.assertFalse(equipment.is_frequent())
        self.assertEqual(equipment.serial_number, "SN987654")

    def test_biomedical_equipment_requires_photo(self):
        biomedical = _create_equipment(
            id=3,
            name="Defibrillator",
            category=EquipmentCategory.BIOMEDICO,
            qr_code="QR789012"
        )

        self.assertTrue(biomedical.requires_photo())

    def test_technological_equipment_no_photo_required(self):
        tech = _create_equipment(
            id=4,
            name="Printer",
            category=EquipmentCategory.TECNOLOGICO,
            qr_code="QR345678"
        )

        self.assertFalse(tech.requires_photo())

    def test_equipment_with_image_url(self):
        equipment = _create_equipment(
            id=5,
            name="X-Ray Machine",
            equipment_type=EquipmentType.NO_FRECUENTE,
            category=EquipmentCategory.BIOMEDICO,
            serial_number="XR123",
            image_url="https://storage.example.com/images/xray123.jpg"
        )

        self.assertEqual(equipment.image_url, "https://storage.example.com/images/xray123.jpg")
        self.assertTrue(equipment.requires_photo())

    def test_equipment_timestamps_auto_set(self):
        equipment = _create_equipment(id=6)

        self.assertIsInstance(equipment.created_at, datetime)
        self.assertIsInstance(equipment.updated_at, datetime)

    # OPCIONAL: Activa si tu dominio lanza excepción cuando falta un dato obligatorio
    # def test_biomedical_equipment_without_photo_raises_error(self):
    #     with self.assertRaises(ValueError):
    #         _create_equipment(
    #             category=EquipmentCategory.BIOMEDICO,
    #             qr_code=None,
    #             image_url=None
    #         )


if __name__ == "__main__":
    unittest.main()
