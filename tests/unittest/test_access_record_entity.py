"""
Unit tests for AccessRecord domain entity (adaptados a implementación actual)
"""
import unittest
from datetime import datetime, timezone, timedelta
from app.domain.entities.access_record import AccessRecord, AccessType, AccessStatus


class TestAccessRecordEntity(unittest.TestCase):
    """Unit tests for the AccessRecord entity"""

    def setUp(self):
        """Common setup for test cases"""
        self.default_entry_time = datetime.now(timezone.utc) - timedelta(hours=1)

    def test_create_entry_record(self):
        """Test creating an entry access record"""
        record = AccessRecord(
            id=1,
            equipment_id=10,
            user_id=5,
            access_type=AccessType.INGRESO,
            notes="Equipment entering for maintenance"
        )

        self.assertEqual(record.id, 1)
        self.assertEqual(record.equipment_id, 10)
        self.assertEqual(record.user_id, 5)
        self.assertEqual(record.access_type, AccessType.INGRESO)
        self.assertIsNone(record.exit_time)
        self.assertIsInstance(record.entry_time, datetime)
        self.assertEqual(record.status, AccessStatus.ACTIVO)

    def test_create_exit_record(self):
        """Test creating an exit access record"""
        exit_time = datetime.now(timezone.utc)

        record = AccessRecord(
            id=2,
            equipment_id=10,
            user_id=5,
            access_type=AccessType.EGRESO,
            entry_time=self.default_entry_time,
            exit_time=exit_time
        )

        self.assertEqual(record.access_type, AccessType.EGRESO)
        self.assertEqual(record.exit_time, exit_time)
        self.assertGreater(record.exit_time, record.entry_time)

    def test_is_expired_not_expired(self):
        """Record should not be expired when status is ACTIVE and still within allowed days"""
        record = AccessRecord(
            id=7,
            equipment_id=10,
            user_id=5,
            access_type=AccessType.INGRESO,
            entry_time=datetime.now(timezone.utc) - timedelta(days=1)
        )

        self.assertFalse(record.is_expired())



    def test_is_expired_with_exit(self):
        """Record should not be expired if exit_time is already set"""
        record = AccessRecord(
            id=9,
            equipment_id=10,
            user_id=5,
            access_type=AccessType.EGRESO,
            entry_time=datetime.now(timezone.utc) - timedelta(days=10),
            exit_time=datetime.now(timezone.utc) - timedelta(days=9)
        )

        # Tu entidad nunca marca vencido si ya está completado
        self.assertFalse(record.is_expired())

    def test_notes_is_optional(self):
        """Notes field should be optional"""
        record = AccessRecord(
            id=10,
            equipment_id=10,
            user_id=5,
            access_type=AccessType.INGRESO
        )
        self.assertIsNone(record.notes)


class TestAccessTypeEnum(unittest.TestCase):
    """Test AccessType enumeration"""

    def test_enum_values(self):
        """Should match exact expected values"""
        self.assertEqual(AccessType.INGRESO.value, "ingreso")
        self.assertEqual(AccessType.EGRESO.value, "egreso")


if __name__ == "__main__":
    unittest.main()
