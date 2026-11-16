
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.ai.agent import run_agent
from app.schemas.assistant import (
    AssistantRequest,
    AssistantResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/companies/{company_id}/assistant",
    response_model=AssistantResponse,
)
def ask_assistant(
    company_id: int,
    request: AssistantRequest,
    db: Session = Depends(get_db),
):
    try:
        result = run_agent(
            db=db,
            company_id=company_id,
            user_message=request.message,
            conversation_id=request.conversation_id,
        )

        return AssistantResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception:
        db.rollback()

        logger.exception(
            "Error while executing AI assistant"
        )

        raise HTTPException(
            status_code=502,
            detail="The AI assistant could not process the request.",
        )
