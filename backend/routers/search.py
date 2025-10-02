from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from db.database import get_db
from db.models import Physician, Message


router = APIRouter(prefix="", tags=["search"])


# in this simple cases the response type maps 1:1 with database type, however
# decoupling them allows us to change the shema without accidentally breaking contracts with the frontend
class PhysicianResponse(BaseModel):
    physician_id: int
    npi: str
    first_name: str
    last_name: str
    specialty: str
    state: str
    consent_opt_in: bool
    preferred_channel: str

    @staticmethod
    def from_db(physician: Physician) -> "PhysicianResponse":
        return PhysicianResponse(
            physician_id=physician.physician_id,
            npi=physician.npi,
            first_name=physician.first_name,
            last_name=physician.last_name,
            specialty=physician.specialty,
            state=physician.state,
            consent_opt_in=physician.consent_opt_in,
            preferred_channel=physician.preferred_channel,
        )


class MessageResponse(BaseModel):
    message_id: int
    physician_id: int
    channel: str
    direction: str
    timestamp: str
    message_text: str
    campaign_id: Optional[str] = None
    topic: Optional[str] = None
    compliance_tag: Optional[str] = None
    sentiment: Optional[str] = None
    delivery_status: Optional[str] = None
    response_latency_sec: Optional[float] = None

    @staticmethod
    def from_db(message: Message) -> "MessageResponse":
        return MessageResponse(
            message_id=message.message_id,
            physician_id=message.physician_id,
            channel=message.channel,
            direction="outbound" if message.is_outbound else "inbound",
            timestamp=message.timestamp.strftime(
                "%Y-%m-%dT%H:%M:%S"
            ),  # same format as sample data
            message_text=message.message_text,
            campaign_id=message.campaign_id,
            topic=message.topic,
            compliance_tag=message.compliance_tag,
            sentiment=message.sentiment,
            delivery_status=message.delivery_status,
            response_latency_sec=message.response_latency_sec,
        )


@router.get("/physicians", response_model=list[PhysicianResponse])
def get_physicians(
    state: str | None = None,
    specialty: str | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(Physician)
    if state is not None:
        stmt = stmt.filter(Physician.state.ilike(state))
    if specialty is not None:
        stmt = stmt.filter(Physician.specialty.like(specialty))

    physicians = db.execute(stmt).scalars()

    return list(map(PhysicianResponse.from_db, physicians))


@router.get("/messages", response_model=list[MessageResponse])
def get_messages(
    physician_id: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(get_db),
):
    # ensure start_date comes after end_date
    is_full_range_set = (start_date is not None) and (end_date is not None)
    if is_full_range_set and start_date > end_date:  # pyright: ignore (lsp not smart enough to realize both types arent't None)
        raise HTTPException(
            status_code=400, detail="Start date must come before end date"
        )

    stmt = select(Message).order_by(Message.timestamp)
    if physician_id is not None:
        stmt = stmt.filter(Message.physician_id == physician_id)

    if start_date is not None:
        stmt = stmt.filter(Message.timestamp >= start_date)
    if end_date is not None:
        stmt = stmt.filter(Message.timestamp <= end_date)

    messages = db.execute(stmt).scalars()

    return list(map(MessageResponse.from_db, messages))
