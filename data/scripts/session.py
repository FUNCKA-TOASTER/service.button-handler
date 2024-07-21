from sqlalchemy.orm import Session
from toaster.database import script
from data import Session as MenuSession, Delay
from datetime import datetime, timedelta


@script(auto_commit=False, debug=True)
def open_menu_session(session: Session, bpid: int, cmid: int) -> None:
    setting = session.get(Delay, {"bpid": bpid, "setting": "menu_session"})
    delay = setting.delay if setting else 0
    expired = datetime.now() + timedelta(minutes=delay)
    new_menu_session = MenuSession(bpid=bpid, cmid=cmid, expired=expired)
    session.add(new_menu_session)
    session.commit()


@script(auto_commit=False, debug=True)
def close_menu_session(session: Session, bpid: int, cmid: int) -> None:
    menu_session = session.get(MenuSession, {"bpid": bpid, "cmid": cmid})
    session.delete(menu_session)
    session.commit()
