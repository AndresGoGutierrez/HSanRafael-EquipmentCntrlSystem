from app.domain.entities.access_record import AccessRecord, AccessType, AccessStatus
from datetime import datetime, timedelta, timezone

class DummySettings:
    EQUIPMENT_MAX_STAY_DAYS = 2

def test_access_record_creation(monkeypatch):
    # Simular settings globales
    monkeypatch.setattr("app.domain.entities.access_record.settings", DummySettings())

    record = AccessRecord(
        id=1,
        equipment_id=10,
        user_id=20,
        access_type=AccessType.INGRESO
    )

    assert record.status == AccessStatus.ACTIVO
    assert record.equipment_id == 10
    assert record.user_id == 20
    assert isinstance(record.expected_exit_time, datetime)

def test_mark_as_completed(monkeypatch):
    monkeypatch.setattr("app.domain.entities.access_record.settings", DummySettings())
    record = AccessRecord(
        equipment_id=1,
        user_id=1,
        access_type=AccessType.INGRESO
    )

    record.mark_as_completed()
    assert record.status == AccessStatus.COMPLETADO
    assert record.exit_time is not None

def test_is_expired(monkeypatch):
    monkeypatch.setattr("app.domain.entities.access_record.settings", DummySettings())
    past_time = datetime.now(timezone.utc) - timedelta(days=3)
    record = AccessRecord(
        equipment_id=1,
        user_id=1,
        access_type=AccessType.INGRESO,
        expected_exit_time=past_time
    )
    assert record.is_expired()

def test_to_dict(monkeypatch):
    monkeypatch.setattr("app.domain.entities.access_record.settings", DummySettings())
    record = AccessRecord(
        equipment_id=5,
        user_id=6,
        access_type=AccessType.EGRESO
    )
    data = record.to_dict()
    assert data["access_type"] == "egreso"
    assert "equipment_id" in data
