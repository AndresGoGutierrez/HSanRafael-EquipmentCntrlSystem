from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from app.domain.entities.access_record import AccessRecord


class AccessRecordRepository(ABC):
    """Port for access record repository"""

    # ------------- CREATE --------------
    @abstractmethod
    def create(self, access_record: AccessRecord) -> AccessRecord:
        """Persist a new AccessRecord entity."""
        raise NotImplementedError

    # ------------- READ --------------
    @abstractmethod
    def get_by_id(self, record_id: int) -> Optional[AccessRecord]:
        """Retrieve an access record by its unique identifier."""
        raise NotImplementedError

    @abstractmethod
    def get_active_by_equipment(self, equipment_id: int) -> Optional[AccessRecord]:
        """Retrieve the currently active access record for a specific equipment."""
        raise NotImplementedError

    @abstractmethod
    def get_by_equipment(
        self, equipment_id: int, skip: int = 0, limit: int = 100
    ) -> List[AccessRecord]:
        """Retrieve all access records for a given equipment."""
        raise NotImplementedError

    @abstractmethod
    def get_by_user(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AccessRecord]:
        """Retrieve all access records created by a specific user."""
        raise NotImplementedError

    @abstractmethod
    def get_active_records(self) -> List[AccessRecord]:
        """Retrieve all currently active access records."""
        raise NotImplementedError

    @abstractmethod
    def get_expired_records(self) -> List[AccessRecord]:
        """Retrieve all access records that have expired."""
        raise NotImplementedError

    @abstractmethod
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AccessRecord]:
        """Retrieve all access records created within a specific date range."""
        raise NotImplementedError
    
    # ------------- UPDATE --------------

    @abstractmethod
    def update(self, access_record: AccessRecord) -> AccessRecord:
        """Update an existing access record."""
        raise NotImplementedError
    
    # ------------- DELETE --------------
    @abstractmethod
    def delete(self, record_id: int) -> bool:
        """Delete an access record by its ID."""
        raise NotImplementedError
