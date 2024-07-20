from sqlalchemy.orm import Session
from toaster.database import script
from data import Permission, Staff, StaffRole, UserPermission


@script(auto_commit=False, debug=True)
def get_user_permission(
    session: Session, uuid: int, bpid: int, ignore_staff: bool = False
) -> UserPermission:
    if not ignore_staff:
        staff = session.get(Staff, {"uuid": uuid})
        if (staff is not None) and (StaffRole.TECH == staff.role):
            return UserPermission.administrator

    user = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    return user.permission if user else UserPermission.user


@script(auto_commit=False, debug=True)
def set_user_permission(
    session: Session, lvl: UserPermission, uuid: int, bpid: int
) -> None:
    new_user = Permission(
        bpid=bpid,
        uuid=uuid,
        permission=lvl,
    )
    session.add(new_user)
    session.commit()


@script(auto_commit=False, debug=True)
def update_user_permission(
    session: Session, lvl: UserPermission, uuid: int, bpid: int
) -> None:
    user = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    user.permission = lvl
    session.commit()


@script(auto_commit=False, debug=True)
def drop_user_permission(session: Session, uuid: int, bpid: int) -> None:
    user = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    session.delete(user)
    session.commit()
