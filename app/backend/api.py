from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.core.agent import get_response_from_agents
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger = get_logger(__name__)

app = FastAPI(title="Multi AI Agent")


# validating incoming data
class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

# generate responses from the LLM


@app.post("/chat")
def chat_endpoint(request: RequestState):
    logger.info(f'Received request for model: {request.model_name}')

    if request.model_name not in settings.ALLOWED_MODELS:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400, detail="Invalid model name")

    try:
        response = get_response_from_agents(
            request.model_name,
            request.system_prompt,
            request.messages,
            request.allow_search
        )

        logger.info(f"Successful received response from Agent"
                    f"{request.model_name}")

        return {"response": response}

    except Exception as e:
        logger.error("Error occurred during message generation")
        raise HTTPException(
            status_code=500,
            detail=str(CustomException("Failed to get response",
                                       error_detail=e)))
