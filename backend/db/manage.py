#####
# Manage db
#    - migrations
#    - move sample data to database
#####
import argparse
import csv
import json
from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import date, datetime

from db.database import SessionLocal, create_tables
from db.models import (
    Physician as PhysicianDB,
    Message as MessageDB,
    ComplianceVersion as ComplianceVersionDB,
    Rule as RuleDB,
    AnyKeyword as AnyKeywordDB,
)

##
# Declare the shape of the input datat to parse it declaratively with pydantic
##


class Rule(BaseModel):
    id: str
    name: str
    keywords_any: List[str]
    action: Optional[str] = None
    requires_append: Optional[str] = None


class Compliance(BaseModel):
    version: str
    updated: date
    rules: List[Rule]


class Message(BaseModel):
    message_id: int
    physician_id: int
    channel: str
    direction: str
    timestamp: datetime
    message_text: str
    campaign_id: Optional[str] = None
    topic: Optional[str] = None
    compliance_tag: Optional[str] = None
    sentiment: Optional[str] = None
    delivery_status: Optional[str] = None
    response_latency_sec: Optional[float] = None

    @field_validator("response_latency_sec", mode="before")
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v


class Physician(BaseModel):
    physician_id: int
    npi: str
    first_name: str
    last_name: str
    specialty: str
    state: str
    consent_opt_in: bool
    preferred_channel: str


##
# Read in the data and convert it to the db types
##


def load_data():
    db = SessionLocal()
    try:
        # Load physicians
        with open("sample_data/physicians.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row: dict
                physician = Physician(**row)
                db_physician = PhysicianDB(**physician.model_dump())
                db.add(db_physician)
        db.commit()

        # Load messages
        with open("sample_data/messages.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row: dict
                message = Message(**row)
                db_message = MessageDB(
                    message_id=message.message_id,
                    physician_id=message.physician_id,
                    channel=message.channel,
                    is_outbound=message.direction == "outbound",
                    timestamp=message.timestamp,
                    message_text=message.message_text,
                    topic=message.topic,
                    campaign_id=message.campaign_id,
                    compliance_tag=message.compliance_tag,
                    sentiment=message.sentiment,
                    delivery_status=message.delivery_status,
                    response_latency_sec=message.response_latency_sec,
                )
                db.add(db_message)
        db.commit()

        # Load compliance policies
        with open("sample_data/compliance_policies.json", "r") as f:
            data = json.load(f)
            compliance = Compliance(**data)
            db_compliance_version = ComplianceVersionDB(
                version=compliance.version, first_name=compliance.updated.isoformat()
            )
            db.add(db_compliance_version)
            db.commit()

            for rule in compliance.rules:
                # rules are assumption to have a single result type e.i. action, requires_append etc
                # result type stores this value along with the text

                # a rule must have either it is likely more cases would need to be added, but then the parsing will also change
                assert rule.action or rule.requires_append
                result_type = "action" if rule.action else "requires_append"
                result_text = rule.action if rule.action else rule.requires_append

                db_rule = RuleDB(
                    id=rule.id,
                    compliance_version=compliance.version,
                    name=rule.name,
                    result_type=result_type,
                    result_text=result_text,
                )
                db.add(db_rule)
                db.commit()

                for keyword in rule.keywords_any:
                    db_keyword = AnyKeywordDB(rule_id=rule.id, keyword=keyword)
                    db.add(db_keyword)
                db.commit()

    finally:
        db.close()
    print("Data loaded successfully")


# more sophiscated migration scripts or tooling would need to be used for reflect changes, deletetions, etc to the schema
def run_migrations():
    create_tables()
    print("Migrations ran successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the database.")
    parser.add_argument("action", choices=["load", "migrate"], help="Action to perform")
    args = parser.parse_args()

    if args.action == "load":
        load_data()
    elif args.action == "migrate":
        run_migrations()
