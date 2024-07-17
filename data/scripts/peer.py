from typing import Optional
from sqlalchemy.orm import Session
from toaster.database import script
from data import Peer, PeerMark


@script(auto_commit=False)
def get_peer_mark(session: Session, bpid: int) -> Optional[str]:
    peer = session.get(Peer, {"id": bpid})
    return peer.mark.value if peer else None


@script(auto_commit=False)
def set_peer_mark(session: Session, mark: str, bpid: int, name: str) -> None:
    new_mark = Peer(
        id=bpid,
        name=name,
        mark=PeerMark(mark),
    )
    session.add(new_mark)
    session.commit()


@script(auto_commit=False)
def update_peer_data(session: Session, bpid: int, name: str) -> None:
    peer = session.get(Peer, {"id": bpid})
    peer.name = name
    session.commit()


@script(auto_commit=False)
def drop_peer_mark(session: Session, bpid: int) -> None:
    peer = session.get(Peer, {"id": bpid})
    session.delete(peer)
    session.commit()
