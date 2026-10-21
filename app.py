
import logging
import time

from fastapi import FastAPI
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger("mock-ai")

app = FastAPI(
    title="MLOps Practice Lab",
    description="A mock AI API for learning deployment and monitoring.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    question: str
    answer: str
    mode: str
    latency_ms: float


def generate_mock_answer(question: str) -> str:
    """Return a predefined answer without calling a real LLM."""
    text = question.lower()

    if "mlops" in text:
        return (
            "MLOps helps teams build, deploy, monitor, "
            "and maintain machine learning systems."
        )

    if "llmops" in text:
        return (
            "LLMOps helps teams operate LLM applications, "
            "including prompt management, evaluation, "
            "monitoring, and cost control."
        )

    if "monitor" in text:
        return (
            "Monitor response times, errors, application "
            "availability, and AI response quality."
        )

    if "docker" in text:
        return (
            "Docker packages an application and its dependencies "
            "into a container for consistent execution."
        )

    return (
        "This is a mock AI response. The application received "
        "your question successfully, but no real LLM was called."
    )


@app.get("/")
def home():
    return {
        "message": "Welcome to the MLOps Practice Lab!",
        "documentation": "/docs",
        "health_check": "/health",
        "chat_endpoint": "POST /chat",
        "mode": "mock",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    start = time.perf_counter()

    answer = generate_mock_answer(request.question)

    latency_ms = round(
        (time.perf_counter() - start) * 1000, 2
    )

    logger.info(
        "chat_request question_length=%d latency_ms=%.2f mode=mock",
        len(request.question),
        latency_ms,
    )

    return ChatResponse(
        question=request.question,
        answer=answer,
        mode="mock",
        latency_ms=latency_ms,
    )
