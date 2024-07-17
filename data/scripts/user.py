from sqlalchemy.orm import Session
from toaster.database import script
from data import Permission, Staff, StaffRole


@script(auto_commit=False)
def get_user_permission(session: Session, uuid: int, bpid: int) -> int:
    staff = session.get(Staff, {"uuid": uuid})
    if (staff is not None) and (StaffRole.TECH == staff.role):
        return 2

    permission = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    return permission.permission.value if permission else 0
