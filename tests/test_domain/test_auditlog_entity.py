from app.domain.entities.audit_log import AuditLog, AuditAction


def test_auditlog_creation_to_dict():
    """
    Test that AuditLog instances are correctly converted to a dictionary using to_dict().
    """
    # Create a sample audit log for a user login event
    log = AuditLog(
        user_id=1,
        action=AuditAction.USER_LOGIN,
        entity_type="User",
        entity_id=1,
        ip_address="127.0.0.1",
        user_agent="pytest"
    )

    # Convert the log to a dictionary and verify the expected fields
    data = log.to_dict()
    assert data["action"] == "user_login"      # Enum value should be serialized correctly
    assert data["entity_type"] == "User"
    assert data["ip_address"] == "127.0.0.1"
    assert "created_at" in data                # The creation timestamp should be included


def test_auditlog_short_description():
    """
    Test that short_description() returns a clear and concise string representation.
    """
    # Create a sample audit log for a report generation action
    log = AuditLog(
        user_id=2,
        action=AuditAction.REPORT_GENERATED,
        entity_type="Report",
        entity_id=10,
    )

    # Generate a short description and validate expected content
    desc = log.short_description()
    assert "report_generated" in desc          # Action should appear in the description
    assert "Report" in desc                    # Entity type should also be included


def test_auditlog_repr():
    """
    Test that the __repr__ method returns a properly formatted string.
    """
    # Create a sample audit log and verify that its representation includes identifying details
    log = AuditLog(
        user_id=3,
        action=AuditAction.ACCESS_ENTRY,
        entity_type="AccessRecord",
        entity_id=5,
    )

    # Ensure the repr contains the class name and basic structure
    assert "<AuditLog" in repr(log)
