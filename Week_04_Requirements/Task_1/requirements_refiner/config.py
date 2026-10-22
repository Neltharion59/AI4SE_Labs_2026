"""Configuration for the requirements pipeline."""

from __future__ import annotations

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Assignment settings are kept directly in code. Only the API credentials
# belong in the untracked .env file.
EXTRACTOR_MODEL = "gpt-4o-mini"
CONSOLIDATOR_MODEL = "gpt-5-mini"
REVIEWER_MODEL = "gpt-6-luna"
LLM_TIMEOUT_SECONDS = 300.0
MAX_RETRIES = 2
CHUNK_CHAR_LIMIT = 8000
CHUNK_OVERLAP_PARAGRAPHS = 1
MAX_REVIEW_ITERATIONS = 10
EXTRACTION_BATCH_SIZE = 8


class Settings(BaseSettings):
    """Runtime settings.

    The API key is optional while constructing settings so all deterministic
    code and tests can run offline. A live LLM entry point must explicitly call
    :meth:`require_api_key` before creating clients.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    openai_api_key: SecretStr | None = None
    openai_base_url: str | None = None

    extractor_model: str = EXTRACTOR_MODEL
    consolidator_model: str = CONSOLIDATOR_MODEL
    reviewer_model: str = REVIEWER_MODEL

    llm_timeout_seconds: float = Field(default=LLM_TIMEOUT_SECONDS, gt=0)
    max_retries: int = Field(default=MAX_RETRIES, ge=0, le=10)
    chunk_char_limit: int = Field(default=CHUNK_CHAR_LIMIT, ge=500)
    chunk_overlap_paragraphs: int = Field(default=CHUNK_OVERLAP_PARAGRAPHS, ge=0, le=10)
    max_review_iterations: int = Field(default=MAX_REVIEW_ITERATIONS, ge=0, le=20)
    extraction_batch_size: int = Field(default=EXTRACTION_BATCH_SIZE, ge=1, le=100)

    @model_validator(mode="after")
    def validate_models_are_distinct(self) -> "Settings":
        models = [
            self.extractor_model.strip(),
            self.consolidator_model.strip(),
            self.reviewer_model.strip(),
        ]
        if any(not model for model in models):
            raise ValueError("Model names must not be empty")
        if len({model.casefold() for model in models}) != 3:
            raise ValueError(
                "Extractor, consolidator and reviewer must use three distinct models"
            )
        self.extractor_model, self.consolidator_model, self.reviewer_model = models

        if self.openai_base_url is not None:
            self.openai_base_url = self.openai_base_url.strip() or None
        return self

    def require_api_key(self) -> str:
        """Return the configured API key or raise a safe, actionable error."""

        if self.openai_api_key is None:
            raise ValueError(
                "OPENAI_API_KEY is required for a live LLM run. "
                "Set it in the environment or in an untracked .env file."
            )
        key = self.openai_api_key.get_secret_value().strip()
        if not key:
            raise ValueError(
                "OPENAI_API_KEY is empty. Set it before starting a live LLM run."
            )
        return key

