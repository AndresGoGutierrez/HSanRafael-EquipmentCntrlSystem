from app.domain.entities.audit_log import AuditLog, AuditAction

def test_auditlog_creation_to_dict():
    log = AuditLog(
        user_id=1,
        action=AuditAction.USER_LOGIN,
        entity_type="User",
        entity_id=1,
        ip_address="127.0.0.1",
        user_agent="pytest"
    )

    data = log.to_dict()
    assert data["action"] == "user_login"
    assert data["entity_type"] == "User"
    assert data["ip_address"] == "127.0.0.1"
    assert "created_at" in data

def test_auditlog_short_description():
    log = AuditLog(
        user_id=2,
        action=AuditAction.REPORT_GENERATED,
        entity_type="Report",
        entity_id=10,
    )
    desc = log.short_description()
    assert "report_generated" in desc
    assert "Report" in desc

def test_auditlog_repr():
    log = AuditLog(
        user_id=3,
        action=AuditAction.ACCESS_ENTRY,
        entity_type="AccessRecord",
        entity_id=5,
    )
    assert "<AuditLog" in repr(log)
