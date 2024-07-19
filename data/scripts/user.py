from sqlalchemy.orm import Session
from toaster.database import script
from data import Permission, Staff, StaffRole, UserPermission


@script(auto_commit=False, debug=True)
def get_user_permission(
    session: Session, uuid: int, bpid: int, ignore_staff: bool = False
) -> int:
    if not ignore_staff:
        staff = session.get(Staff, {"uuid": uuid})
        if (staff is not None) and (StaffRole.TECH == staff.role):
            return 2

    permission = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    return permission.permission.value if permission else 0


@script(auto_commit=False, debug=True)
def set_user_permission(session: Session, uuid: int, bpid: int, lvl: int) -> int:
    new_permission = Permission(
        bpid=bpid,
        uuid=uuid,
        permission=UserPermission(lvl),
    )
    session.add(new_permission)
    session.commit()


@script(auto_commit=False, debug=True)
def update_user_permission(session: Session, uuid: int, bpid: int, lvl: int) -> int:
    permission = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    permission.permission(lvl)
    session.commit()


@script(auto_commit=False, debug=True)
def drop_user_permission(session: Session, uuid: int, bpid: int) -> int:
    permission = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    session.delete(permission)
    session.commit()
