from app.domain.entities.access_record import AccessRecord, AccessType, AccessStatus
from datetime import datetime, timedelta, timezone


class DummySettings:
    """
    Dummy configuration class used to simulate global application settings
    for testing purposes.
    """
    EQUIPMENT_MAX_STAY_DAYS = 2


def test_access_record_creation(monkeypatch):
    """
    Test that AccessRecord instances are created correctly with default values.
    """
    # Mock global settings used in AccessRecord
    monkeypatch.setattr("app.domain.entities.access_record.settings", DummySettings())

    # Create a new access record for equipment entry
    record = AccessRecord(
        id=1,
        equipment_id=10,
        user_id=20,
        access_type=AccessType.INGRESO
    )

    # Verify default attributes after creation
    assert record.status == AccessStatus.ACTIVO             # Should be active upon creation
    assert record.equipment_id == 10
    assert record.user_id == 20
    assert isinstance(record.expected_exit_time, datetime)  # Expected exit time must be set


def test_mark_as_completed(monkeypatch):
    """
    Test that mark_as_completed() updates the status and sets the exit time.
    """
    # Patch settings dependency
    monkeypatch.setattr("app.domain.entities.access_record.settings", DummySettings())

    # Create an active record
    record = AccessRecord(
        equipment_id=1,
        user_id=1,
        access_type=AccessType.INGRESO
    )

    # Complete the record and check the new state
    record.mark_as_completed()
    assert record.status == AccessStatus.COMPLETADO          # Status must change to completed
    assert record.exit_time is not None                      # Exit time should be recorded


def test_is_expired(monkeypatch):
    """
    Test that is_expired() returns True when expected_exit_time is in the past.
    """
    # Override global settings
    monkeypatch.setattr("app.domain.entities.access_record.settings", DummySettings())

    # Simulate a record whose expected exit time has already passed
    past_time = datetime.now(timezone.utc) - timedelta(days=3)
    record = AccessRecord(
        equipment_id=1,
        user_id=1,
        access_type=AccessType.INGRESO,
        expected_exit_time=past_time
    )

    # Check expiration logic
    assert record.is_expired()                               # Should be expired


def test_to_dict(monkeypatch):
    """
    Test that to_dict() serializes AccessRecord correctly.
    """
    # Patch settings dependency
    monkeypatch.setattr("app.domain.entities.access_record.settings", DummySettings())

    # Create an access record for an equipment exit
    record = AccessRecord(
        equipment_id=5,
        user_id=6,
        access_type=AccessType.EGRESO
    )

    # Convert the record to a dictionary and verify key data
    data = record.to_dict()
    assert data["access_type"] == "egreso"                   # Enum must serialize properly
    assert "equipment_id" in data                            # Field must be included in output
