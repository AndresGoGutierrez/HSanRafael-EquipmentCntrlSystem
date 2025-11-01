from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from app.domain.entities.audit_log import AuditLog, AuditAction


class AuditLogRepository(ABC):
    """Port interface for the Audit Log repository.
    
    Defines the contract for storing and retrieving audit logs from the data source.
    Concrete implementations (e.g., SQLAlchemy, MongoDB, etc.) must implement these methods.
    """

    # ───────────────────────────────────────────────
    # CREATE
    # ───────────────────────────────────────────────
    
    @abstractmethod
    def create(self, audit_log: AuditLog) -> AuditLog:
        """Create a new audit log entry.
        
        Args:
            audit_log: The audit log entity to persist.
        
        Returns:
            AuditLog: The created audit log entry.
        """
        raise NotImplementedError("AuditLogRepository.create() must be implemented by subclass.")
    
    # ───────────────────────────────────────────────
    # RETRIEVAL
    # ───────────────────────────────────────────────
    
    @abstractmethod
    def get_by_id(self, log_id: int) -> Optional[AuditLog]:
        """Retrieve an audit log entry by its unique ID.
        
        Args:
            log_id: The ID of the audit log.
        
        Returns:
            Optional[AuditLog]: The matching audit log, or None if not found.
        """
        raise NotImplementedError("AuditLogRepository.get_by_id() must be implemented by subclass.")
    
    @abstractmethod
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Retrieve audit logs associated with a specific user.
        
        Args:
            user_id: The ID of the user.
            skip: Number of records to skip (for pagination).
            limit: Maximum number of records to return.
        
        Returns:
            List[AuditLog]: A list of audit logs for the specified user.
        """
        raise NotImplementedError("AuditLogRepository.get_by_user() must be implemented by subclass.")
    
    @abstractmethod
    def get_by_action(self, action: AuditAction, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Retrieve audit logs filtered by a specific action type.
        
        Args:
            action: The type of action (e.g., CREATE, UPDATE, DELETE).
            skip: Number of records to skip.
            limit: Maximum number of records to return.
        
        Returns:
            List[AuditLog]: Audit logs that match the specified action.
        """
        raise NotImplementedError("AuditLogRepository.get_by_action() must be implemented by subclass.")
    
    @abstractmethod
    def get_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[AuditLog]:
        """Retrieve audit logs within a specific date range.
        
        Args:
            start_date: Start of the time range.
            end_date: End of the time range.
            skip: Number of records to skip.
            limit: Maximum number of records to return.
        
        Returns:
            List[AuditLog]: Audit logs created between the specified dates.
        """
        raise NotImplementedError("AuditLogRepository.get_by_date_range() must be implemented by subclass.")
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Retrieve all audit logs with pagination support.
        
        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.
        
        Returns:
            List[AuditLog]: List of all audit logs.
        """
        raise NotImplementedError("AuditLogRepository.get_all() must be implemented by subclass.")
