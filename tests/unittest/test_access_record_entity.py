"""
Unit tests for AccessRecord domain entity.

These tests validate the correct behavior, initialization, and business logic
of the `AccessRecord` entity, as well as the associated `AccessType` and
`AccessStatus` enumerations.
"""
import unittest
from datetime import datetime, timezone, timedelta
from app.domain.entities.access_record import AccessRecord, AccessType, AccessStatus


class TestAccessRecordEntity(unittest.TestCase):
    """
    Unit tests for the AccessRecord entity.

    This class contains tests that verify the creation, validation, and 
    behavior of access records representing equipment ingress and egress
    operations within the domain model.
    """

    def setUp(self):
        """
        Common setup executed before each test case.

        Creates a default entry time (one hour ago) used in multiple test cases.
        """
        self.default_entry_time = datetime.now(timezone.utc) - timedelta(hours=1)

    def test_create_entry_record(self):
        """
        Test creating an entry (INGRESO) access record.

        Verifies that:
        - The record initializes with the expected attributes.
        - Entry time is automatically assigned.
        - Exit time is None.
        - Status defaults to ACTIVE.
        """
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
        """
        Test creating an exit (EGRESO) access record.

        Verifies that:
        - The record correctly stores both entry and exit times.
        - The exit time is greater than the entry time.
        """
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
        """
        Test that an active record within allowed time is not expired.

        Verifies that a record with status ACTIVE and entry time within the 
        allowed duration does not mark as expired.
        """
        record = AccessRecord(
            id=7,
            equipment_id=10,
            user_id=5,
            access_type=AccessType.INGRESO,
            entry_time=datetime.now(timezone.utc) - timedelta(days=1)
        )

        self.assertFalse(record.is_expired())



    def test_is_expired_with_exit(self):
        """
        Test that a record with an exit time is never considered expired.

        Even if a long time has passed since the entry, having an `exit_time`
        means the record is complete and should not expire.
        """
        record = AccessRecord(
            id=9,
            equipment_id=10,
            user_id=5,
            access_type=AccessType.EGRESO,
            entry_time=datetime.now(timezone.utc) - timedelta(days=10),
            exit_time=datetime.now(timezone.utc) - timedelta(days=9)
        )

        self.assertFalse(record.is_expired())

    def test_notes_is_optional(self):
        """
        Test that the `notes` field is optional.

        Verifies that an AccessRecord can be created without notes.
        """
        record = AccessRecord(
            id=10,
            equipment_id=10,
            user_id=5,
            access_type=AccessType.INGRESO
        )
        self.assertIsNone(record.notes)


class TestAccessTypeEnum(unittest.TestCase):
    """
    Unit tests for the AccessType enumeration.

    Ensures that the enumeration values correspond to the expected string
    representations used throughout the system.
    """

    def test_enum_values(self):
        """
        Verify that enumeration values match expected strings.
        """
        self.assertEqual(AccessType.INGRESO.value, "ingreso")
        self.assertEqual(AccessType.EGRESO.value, "egreso")


if __name__ == "__main__":
    unittest.main()
