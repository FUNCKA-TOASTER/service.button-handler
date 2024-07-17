from sqlalchemy.orm import Session
from toaster.database import script
from data import Permission


@script(auto_commit=False)
def get_user_permission(session: Session, uuid: int, bpid: int) -> int:
    permission = session.get(Permission, {"uuid": uuid, "bpid": bpid})
    return permission.permission if permission else 0
