from typing import Dict
from sqlalchemy.orm import Session
from toaster.database import script
from data import Setting, SettingDestination, SettingStatus


@script(auto_commit=False, debug=True)
def get_destinated_settings(
    session: Session, destination: SettingDestination, bpid: int
) -> Dict[str, SettingStatus]:
    settings = (
        session.query(Setting)
        .filter(
            Setting.bpid == bpid,
            Setting.destination == destination,
        )
        .all()
    )
    result = {setting.name: setting.status for setting in settings}
    return result


@script(auto_commit=False, debug=True)
def update_setting_status(
    session: Session, status: SettingStatus, bpid: int, name: str
) -> None:
    setting = session.get(Setting, {"bpid": bpid, "name": name})
    setting.status = status
    session.commit()
