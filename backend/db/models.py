#####
# Declare db with sqlalchemy ORM
#####

from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, Boolean, CHAR, Text, Float, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .database import Base

# lazy="raise_on_sql" is a scrict setting to cause errors when referencing reltioinships attributes
# that have not been loaded by the ORM
# this is prevent 1 + n queries (i've been hurt before)


class Physician(Base):
    __tablename__ = "physicians"

    physician_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    npi: Mapped[str] = mapped_column(CHAR(10))
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    specialty: Mapped[str] = mapped_column(Text)
    state: Mapped[str] = mapped_column(CHAR(2))
    consent_opt_in: Mapped[bool] = mapped_column(Boolean)
    preferred_channel: Mapped[str] = mapped_column(Text)

    messages: Mapped[List["Message"]] = relationship(
        back_populates="physician", lazy="raise_on_sql"
    )


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    physician_id: Mapped[int] = mapped_column(ForeignKey("physicians.physician_id"))
    channel: Mapped[str] = mapped_column(Text)
    is_outbound: Mapped[bool] = mapped_column(Boolean)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP)
    message_text: Mapped[str] = mapped_column(Text)
    campaign_id: Mapped[str] = mapped_column(Text)
    topic: Mapped[str] = mapped_column(Text)
    compliance_tag: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[str] = mapped_column(Text)
    delivery_status: Mapped[str] = mapped_column(Text)
    response_latency_sec: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    physician: Mapped["Physician"] = relationship(
        back_populates="messages", lazy="raise_on_sql"
    )


class ComplianceVersion(Base):
    __tablename__ = "compliance_versions"

    version: Mapped[str] = mapped_column(Text, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)

    rules: Mapped[List["Rule"]] = relationship(
        back_populates="compliance_version_ref", lazy="raise_on_sql"
    )


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    compliance_version: Mapped[str] = mapped_column(
        ForeignKey("compliance_versions.version"), primary_key=True
    )
    name: Mapped[str] = mapped_column(Text)
    result_type: Mapped[str] = mapped_column(Text)
    result_text: Mapped[str] = mapped_column(Text)

    compliance_version_ref: Mapped["ComplianceVersion"] = relationship(
        back_populates="rules", lazy="raise_on_sql"
    )
    keywords: Mapped[List["AnyKeyword"]] = relationship(
        back_populates="rule", lazy="raise_on_sql"
    )


class AnyKeyword(Base):
    __tablename__ = "anykeywords"

    rule_id: Mapped[str] = mapped_column(ForeignKey("rules.id"), primary_key=True)
    keyword: Mapped[str] = mapped_column(Text, primary_key=True)

    rule: Mapped["Rule"] = relationship(back_populates="keywords", lazy="raise_on_sql")
