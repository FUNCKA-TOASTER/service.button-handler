from typing import Optional
from sqlalchemy.orm import Session
from toaster.broker.events import Event
from toaster.database import script
from data import Peer, PeerMark


@script(auto_commit=False)
def get_peer_mark(session: Session, bpid: int) -> Optional[str]:
    peer = session.get(Peer, {"id": bpid})
    return peer.mark.value if peer else None


@script(auto_commit=False)
def set_peer_mark(session: Session, mark: str, event: Event) -> Optional[str]:
    new_mark = Peer(
        id=event.peer.bpid,
        name=event.peer.name,
        mark=PeerMark(mark),
    )
    session.add(new_mark)
