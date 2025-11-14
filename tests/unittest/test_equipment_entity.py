"""
Unit tests for the Equipment domain entity.

This module contains a comprehensive suite of unit tests designed to validate
the behavior and integrity of the `Equipment` entity and its related enumerations
(`EquipmentType` and `EquipmentCategory`).

The tests ensure that:
- Enumeration values are correctly defined.
- Equipment instances are properly created with expected attributes.
- Business rules (e.g., requiring photos for biomedical equipment) are respected.
- Default timestamps (`created_at`, `updated_at`) are automatically set.

Test framework: unittest (Python Standard Library)
"""
import unittest
from datetime import datetime
from app.domain.entities.equipment import (
    Equipment,
    EquipmentType,
    EquipmentCategory,
)



def _create_equipment(**kwargs) -> Equipment:
    """
    Factory helper function to create `Equipment` entities with default values.

    This utility allows the creation of `Equipment` objects without repeating
    boilerplate code in each test case. It provides reasonable defaults that
    can be overridden by passing keyword arguments.

    Args:
        **kwargs: Custom values to override default attributes of the equipment.

    Returns:
        Equipment: A fully initialized `Equipment` entity ready for testing.
    """
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

    """
    Unit tests for `EquipmentType` and `EquipmentCategory` enumerations.

    This test suite validates that enumeration values are correctly assigned
    and remain consistent with domain definitions.
    """

    def test_equipment_type_enum(self):
        """
        Verify that `EquipmentType` enum values are correct.
        """
        self.assertEqual(EquipmentType.FRECUENTE.value, "frecuente")
        self.assertEqual(EquipmentType.NO_FRECUENTE.value, "no_frecuente")

    def test_equipment_category_enum(self):
        """
        Verify that `EquipmentCategory` enum values are correct.
        """
        self.assertEqual(EquipmentCategory.TECNOLOGICO.value, "tecnologico")
        self.assertEqual(EquipmentCategory.BIOMEDICO.value, "biomedico")


class TestEquipmentEntity(unittest.TestCase):
    """
    Unit tests for the `Equipment` domain entity.

    These tests validate the entity's creation, default behaviors,
    and specific domain logic (e.g., frequent/non-frequent classification,
    photo requirements, and timestamp assignment).
    """

    def test_create_frequent_equipment(self):
        """
        Test creating a frequent equipment instance.

        Ensures that all attributes are correctly initialized and that
        the `is_frequent()` method correctly identifies frequent equipment.
        """
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
        """
        Test creating a non-frequent equipment instance.

        Ensures that the `is_frequent()` method returns False and that
        attributes like `serial_number` are correctly set.
        """
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
        """
        Test that biomedical equipment requires a photo.

        Validates that `requires_photo()` returns True for biomedical category.
        """
        biomedical = _create_equipment(
            id=3,
            name="Defibrillator",
            category=EquipmentCategory.BIOMEDICO,
            qr_code="QR789012"
        )

        self.assertTrue(biomedical.requires_photo())

    def test_technological_equipment_no_photo_required(self):
        """
        Test that technological equipment does not require a photo.

        Validates that `requires_photo()` returns False for technological category.
        """
        tech = _create_equipment(
            id=4,
            name="Printer",
            category=EquipmentCategory.TECNOLOGICO,
            qr_code="QR345678"
        )

        self.assertFalse(tech.requires_photo())

    def test_equipment_with_image_url(self):
        """
        Test that an equipment instance correctly stores an image URL.

        Ensures that the `image_url` attribute is assigned and that
        `requires_photo()` behavior remains consistent with the equipment category.
        """
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
        """
        Test that timestamps are automatically assigned upon creation.

        Verifies that both `created_at` and `updated_at` are instances of `datetime`.
        """
        equipment = _create_equipment(id=6)

        self.assertIsInstance(equipment.created_at, datetime)
        self.assertIsInstance(equipment.updated_at, datetime)


if __name__ == "__main__":
    unittest.main()
