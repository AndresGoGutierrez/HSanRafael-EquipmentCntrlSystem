import pytest
from app.domain.entities.equipment import Equipment, EquipmentType, EquipmentCategory


def test_equipment_creation_valid():
    """
    Test that a valid Equipment instance is created with correct default values.
    """
    # Create a frequent technological equipment instance
    eq = Equipment(
        id=1,
        name="Monitor",
        equipment_type=EquipmentType.FRECUENTE,
        category=EquipmentCategory.TECNOLOGICO,
        serial_number="ABC123"
    )

    # Validate attributes and default states
    assert eq.name == "Monitor"
    assert eq.serial_number == "ABC123"
    assert eq.is_active                       # Equipment should be active by default
    assert eq.is_frequent()                   # FRECUENTE type should be marked as frequent
    assert not eq.requires_photo()            # Frequent equipment should not require a photo


def test_equipment_requires_photo():
    """
    Test that non-frequent biomedical equipment requires a photo.
    """
    eq = Equipment(
        id=2,
        name="ECG",
        equipment_type=EquipmentType.NO_FRECUENTE,
        category=EquipmentCategory.BIOMEDICO
    )

    # Non-frequent biomedical equipment should require a photo
    assert eq.requires_photo()


def test_equipment_activation_deactivation():
    """
    Test the activation and deactivation behavior of Equipment.
    """
    eq = Equipment(
        id=3,
        name="Laptop",
        equipment_type=EquipmentType.FRECUENTE,
        category=EquipmentCategory.TECNOLOGICO
    )

    # Deactivate and check that is_active is False
    eq.deactivate()
    assert not eq.is_active

    # Reactivate and check that is_active is True again
    eq.activate()
    assert eq.is_active


def test_equipment_invalid_type():
    """
    Test that creating Equipment with an invalid type raises a ValueError.
    """
    # Invalid type should raise a ValueError during object creation
    with pytest.raises(ValueError):
        Equipment(
            id=4,
            name="UPS",
            equipment_type="invalid_type",      # Not a valid EquipmentType enum
            category=EquipmentCategory.TECNOLOGICO
        )
