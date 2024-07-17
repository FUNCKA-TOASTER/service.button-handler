from typing import Optional
from sqlalchemy.orm import Session
from toaster.broker.events import Event
from toaster.database import script
from data import Peer, PeerMark


@script(auto_commit=False)
def get_peer_mark(session: Session, event: Event) -> Optional[str]:
    peer = session.get(Peer, {"id": event.peer.bpid})
    return peer.mark.value if peer else None


@script(auto_commit=False)
def set_peer_mark(session: Session, mark: str, event: Event) -> None:
    new_mark = Peer(
        id=event.peer.bpid,
        name=event.peer.name,
        mark=PeerMark(mark),
    )
    session.add(new_mark)
    session.commit()


@script(auto_commit=False)
def update_peer_data(session: Session, event: Event) -> None:
    peer = session.get(Peer, {"id": event.peer.bpid})
    peer.name = event.peer.name
    session.commit()


@script(auto_commit=False)
def drop_peer_mark(session: Session, event: Event) -> None:
    peer = session.get(Peer, {"id": event.peer.bpid})
    session.delete(peer)
    session.commit()
