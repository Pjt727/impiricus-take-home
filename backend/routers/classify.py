from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func, literal
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from itertools import groupby
from operator import attrgetter

from db.database import get_db
from db.models import Message, Rule, AnyKeyword

router = APIRouter(prefix="/classify", tags=["classify"])


class RuleResponse(BaseModel):
    id: str
    name: str
    result_type: str
    result_text: str
    matched_keywords: list[str] = []


class ClassifyMessageResponse(BaseModel):
    message_id: int
    message_text: str
    compliance_version: str
    matched_rules: list[RuleResponse] = []


@router.post("/{message_id}", response_model=ClassifyMessageResponse)
def classify_message(
    message_id: int,
    compliance_version: str = "v1",  # assumed that users would only be interested in a single compliance version at a time
    db: Session = Depends(get_db),
):
    message_stmt = select(Message.message_text).where(Message.message_id == message_id)
    message_text = db.execute(message_stmt).scalar_one_or_none()
    if message_text is None:
        raise HTTPException(status_code=404, detail="Message not found")

    keyword_stmt = (
        select(AnyKeyword)
        .distinct()
        .join(Rule)
        .where(
            Rule.compliance_version == compliance_version,
            func.lower(literal(message_text)).contains(func.lower(AnyKeyword.keyword)),
        )
        .order_by(
            Rule.id
        )  # order by is important for the linear group by Rule.id later
        .options(joinedload(AnyKeyword.rule))
    )

    matching_keywords = db.execute(keyword_stmt).scalars()

    # it could be dangerous to expose the reason why a message triggers a certain
    # rule, for this exercise i've chosen to expose the keyword(s) that match and
    # not any other keywords (mainly because that was the most fun to implement)

    matched_rules_response: list[RuleResponse] = []

    # group the keywords by their rule id, since we do not want to expose all trigger keywords
    # this has to be done here instead of just joinedloading the keywords from rule
    for _, group in groupby(matching_keywords, key=attrgetter("rule.id")):
        keywords_for_rule = list(group)

        # each object has the same rule
        first_keyword_in_group = keywords_for_rule[0]
        associated_rule = first_keyword_in_group.rule

        rule_response = RuleResponse(
            id=associated_rule.id,
            name=associated_rule.name,
            result_type=associated_rule.result_type,
            result_text=associated_rule.result_text,
            matched_keywords=[k.keyword for k in keywords_for_rule],
        )
        matched_rules_response.append(rule_response)

    return ClassifyMessageResponse(
        message_id=message_id,
        message_text=message_text,
        compliance_version=compliance_version,
        matched_rules=matched_rules_response,
    )
