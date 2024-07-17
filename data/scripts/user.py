from sqlalchemy.orm import Session
from toaster.database import script
from toaster.broker.events import Event
from data import Permission, Staff, StaffRole


@script(auto_commit=False)
def get_user_permission(session: Session, event: Event) -> int:
    staff = session.get(Staff, {"uuid": event.user.uuid})
    if (staff is not None) and (StaffRole.TECH == staff.role):
        return 2

    permission = session.get(
        Permission, {"uuid": event.user.uuid, "bpid": event.peer.bpid}
    )

    return permission.permission.value if permission else 0
