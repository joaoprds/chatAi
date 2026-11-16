from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.ai.agent import run_agent
from app.schemas.assistant import (
    AssistantRequest,
    AssistantResponse,
)

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
        answer = run_agent(
            db=db,
            company_id=company_id,
            user_message=request.message,
        )

        return AssistantResponse(answer=answer)

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="The AI assistant could not process the request.",
        )