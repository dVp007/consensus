from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All configuration comes from environment variables (or backend/.env)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # SQLite works out of the box; switch to Postgres via docker-compose later:
    # postgresql+psycopg://consensus:consensus@localhost:5432/consensus
    database_url: str = "sqlite:///./consensus.db"

    # OpenRouter (OpenAI-compatible API)
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    # Pick a model that supports tool calling from https://openrouter.ai/models
    # (filter by "Tools"). Free variants end in ":free" and are rate-limited.
    llm_model: str = "CHANGE_ME/your-model-id"

    # Guardrails for agent loops
    agent_max_steps: int = 6
    agent_max_tokens: int = 1200

    frontend_origin: str = "http://localhost:5173"
    app_name: str = "Consensus"


@lru_cache
def get_settings() -> Settings:
    return Settings()
