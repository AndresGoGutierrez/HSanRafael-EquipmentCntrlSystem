import pytest
from app.domain.entities.equipment import Equipment, EquipmentType, EquipmentCategory

def test_equipment_creation_valid():
    eq = Equipment(
        id=1,
        name="Monitor",
        equipment_type=EquipmentType.FRECUENTE,
        category=EquipmentCategory.TECNOLOGICO,
        serial_number="ABC123"
    )

    assert eq.name == "Monitor"
    assert eq.serial_number == "ABC123"
    assert eq.is_active
    assert eq.is_frequent()
    assert not eq.requires_photo()

def test_equipment_requires_photo():
    eq = Equipment(
        id=2,
        name="ECG",
        equipment_type=EquipmentType.NO_FRECUENTE,
        category=EquipmentCategory.BIOMEDICO
    )
    assert eq.requires_photo()

def test_equipment_activation_deactivation():
    eq = Equipment(
        id=3,
        name="Laptop",
        equipment_type=EquipmentType.FRECUENTE,
        category=EquipmentCategory.TECNOLOGICO
    )

    eq.deactivate()
    assert not eq.is_active
    eq.activate()
    assert eq.is_active

def test_equipment_invalid_type():
    with pytest.raises(ValueError):
        Equipment(
            id=4,
            name="UPS",
            equipment_type="invalid_type",
            category=EquipmentCategory.TECNOLOGICO
        )
