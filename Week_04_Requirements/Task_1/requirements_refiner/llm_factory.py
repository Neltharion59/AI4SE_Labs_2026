"""Construction of role-specific structured-output chat clients."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .schemas import ConsolidationResult, ExtractionResult, ReviewReport


ChatModelFactory = Callable[..., Any]


@dataclass(frozen=True)
class LLMClients:
    """Injectable structured-output runners used by the graph nodes."""

    extractor: Any
    consolidator: Any
    reviewer: Any
    reviser: Any
    extractor_model: str
    consolidator_model: str
    reviewer_model: str


def _base_model(
    *,
    model: str,
    settings: Any,
    chat_model_factory: ChatModelFactory,
    api_key: str | None,
) -> Any:
    kwargs: dict[str, Any] = {
        "model": model,
        "timeout": settings.llm_timeout_seconds,
        "max_retries": settings.max_retries,
    }
    # GPT-6 models currently accept only their default temperature value.
    # Omitting the parameter is different from explicitly sending 0.0, which
    # the API rejects with ``unsupported_value``.
    if not model.casefold().startswith("gpt-6-"):
        kwargs["temperature"] = 0
    if api_key:
        kwargs["api_key"] = api_key
    if getattr(settings, "openai_base_url", None):
        kwargs["base_url"] = settings.openai_base_url
    return chat_model_factory(**kwargs)


def _structured(model: Any, schema: type[Any]) -> Any:
    """Bind JSON-schema output while keeping the runner injectable in tests."""

    return model.with_structured_output(schema, method="json_schema")


def create_llm_clients(
    settings: Any,
    *,
    chat_model_factory: ChatModelFactory | None = None,
) -> LLMClients:
    """Create three model clients and four role-specific structured runners.

    Consolidation and revision intentionally share the consolidator model, while
    extraction and independent review use different models.
    """

    api_key: str | None = None
    if chat_model_factory is None:
        # Keep imports and unit tests usable before optional runtime dependencies
        # are installed. A real execution still uses langchain_openai.ChatOpenAI.
        from langchain_openai import ChatOpenAI

        chat_model_factory = ChatOpenAI
        api_key = settings.require_api_key()

    extractor_base = _base_model(
        model=settings.extractor_model,
        settings=settings,
        chat_model_factory=chat_model_factory,
        api_key=api_key,
    )
    consolidator_base = _base_model(
        model=settings.consolidator_model,
        settings=settings,
        chat_model_factory=chat_model_factory,
        api_key=api_key,
    )
    reviewer_base = _base_model(
        model=settings.reviewer_model,
        settings=settings,
        chat_model_factory=chat_model_factory,
        api_key=api_key,
    )
    return LLMClients(
        extractor=_structured(extractor_base, ExtractionResult),
        consolidator=_structured(consolidator_base, ConsolidationResult),
        reviewer=_structured(reviewer_base, ReviewReport),
        reviser=_structured(consolidator_base, ConsolidationResult),
        extractor_model=settings.extractor_model,
        consolidator_model=settings.consolidator_model,
        reviewer_model=settings.reviewer_model,
    )
