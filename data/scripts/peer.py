from typing import Optional
from sqlalchemy.orm import Session
from toaster.database import script
from data import Peer


@script(auto_commit=False)
def get_peer_mark(session: Session, bpid: int) -> Optional[str]:
    peer = session.get(Peer, {"id": bpid})
    return peer.mark if peer else None
