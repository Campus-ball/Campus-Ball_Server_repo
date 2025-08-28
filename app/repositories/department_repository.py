from typing import List

from sqlalchemy.orm import Session

from app.models import Department


class DepartmentRepository:
    def list_all(self, db: Session) -> List[Department]:
        return db.query(Department).order_by(Department.department_id.asc()).all()
