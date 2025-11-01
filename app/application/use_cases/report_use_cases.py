from typing import List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.infrastructure.models.access_record_model import AccessRecordModel
from app.infrastructure.models.equipment_model import EquipmentModel
from app.infrastructure.models.user_model import UserModel
from app.domain.entities.access_record import AccessStatus


class ReportUseCases:
    """Use cases for generating reports related to access records, users, and equipment."""

    def __init__(self, db: Session):
        """
        Initialize the report use cases with a SQLAlchemy session.
        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    # Summary Report

    def generate_summary_report(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """
        Generate a summary report for the given date range.

        Returns:
            dict: Statistics about equipment access, users, and current statuses.
        """
        # Ensure timezone awareness for consistency
        start_date = start_date.replace(tzinfo=timezone.utc)
        end_date = end_date.replace(tzinfo=timezone.utc)

        def _count(query):
            """Helper to safely count records."""
            return query.scalar() or 0

        total_entries = _count(
            self.db.query(func.count(AccessRecordModel.id)).filter(
                and_(
                    AccessRecordModel.entry_time >= start_date,
                    AccessRecordModel.entry_time <= end_date,
                )
            )
        )

        total_exits = _count(
            self.db.query(func.count(AccessRecordModel.id)).filter(
                and_(
                    AccessRecordModel.exit_time >= start_date,
                    AccessRecordModel.exit_time <= end_date,
                    AccessRecordModel.status == AccessStatus.COMPLETADO,
                )
            )
        )

        currently_inside = _count(
            self.db.query(func.count(AccessRecordModel.id)).filter(
                AccessRecordModel.status == AccessStatus.ACTIVO
            )
        )

        expired_equipment = _count(
            self.db.query(func.count(AccessRecordModel.id)).filter(
                and_(
                    AccessRecordModel.status == AccessStatus.VENCIDO,
                    AccessRecordModel.entry_time >= start_date,
                    AccessRecordModel.entry_time <= end_date,
                )
            )
        )

        total_equipment = _count(self.db.query(func.count(EquipmentModel.id)))
        total_users = _count(self.db.query(func.count(UserModel.id)))

        return {
            "total_entries": total_entries,
            "total_exits": total_exits,
            "currently_inside": currently_inside,
            "expired_equipment": expired_equipment,
            "total_equipment": total_equipment,
            "total_users": total_users,
            "period_start": start_date,
            "period_end": end_date,
        }

    # Equipment Report

    def generate_equipment_report(
        self, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Generate a detailed report of equipment access records.

        Returns:
            list[dict]: List of access records with equipment and user details.
        """
        start_date = start_date.replace(tzinfo=timezone.utc)
        end_date = end_date.replace(tzinfo=timezone.utc)

        records = (
            self.db.query(AccessRecordModel, EquipmentModel, UserModel)
            .join(EquipmentModel, AccessRecordModel.equipment_id == EquipmentModel.id)
            .join(UserModel, AccessRecordModel.user_id == UserModel.id)
            .filter(
                and_(
                    AccessRecordModel.entry_time >= start_date,
                    AccessRecordModel.entry_time <= end_date,
                )
            )
            .all()
        )

        result = []
        now = datetime.now(timezone.utc)

        for record, equipment, user in records:
            entry_time = record.entry_time or now
            exit_time = record.exit_time
            expected_exit = record.expected_exit_time

            days_inside = (
                (exit_time - entry_time).days if exit_time else (now - entry_time).days
            )

            is_expired = (
                bool(expected_exit)
                and record.status == AccessStatus.ACTIVO
                and now > expected_exit
            )

            result.append(
                {
                    "record_id": record.id,
                    "equipment_name": equipment.name,
                    "equipment_qr_code": equipment.qr_code,
                    "equipment_serial_number": equipment.serial_number,
                    "user_full_name": user.full_name,
                    "entry_time": entry_time,
                    "exit_time": exit_time,
                    "expected_exit_time": expected_exit,
                    "status": record.status.value,
                    "days_inside": days_inside,
                    "is_expired": is_expired,
                }
            )

        return result

    # User Activity Report

    def generate_user_activity_report(
        self, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Generate a report of user activity during the given period.

        Returns:
            list[dict]: List of users with the number of actions performed.
        """
        start_date = start_date.replace(tzinfo=timezone.utc)
        end_date = end_date.replace(tzinfo=timezone.utc)

        user_stats = (
            self.db.query(
                UserModel.id,
                UserModel.username,
                UserModel.full_name,
                UserModel.role,
                func.count(AccessRecordModel.id).label("total_actions"),
            )
            .join(AccessRecordModel, UserModel.id == AccessRecordModel.user_id)
            .filter(
                and_(
                    AccessRecordModel.created_at >= start_date,
                    AccessRecordModel.created_at <= end_date,
                )
            )
            .group_by(
                UserModel.id,
                UserModel.username,
                UserModel.full_name,
                UserModel.role,
            )
            .all()
        )

        return [
            {
                "user_id": uid,
                "username": username,
                "full_name": fullname,
                "role": role.value if hasattr(role, "value") else role,
                "total_actions": actions,
            }
            for uid, username, fullname, role, actions in user_stats
        ]
