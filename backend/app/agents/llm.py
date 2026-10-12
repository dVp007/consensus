"""Thin OpenRouter client. OpenRouter speaks the OpenAI Chat Completions API, so we use
the official `openai` SDK with a different base_url. Swapping models = changing LLM_MODEL.

This file is complete. Everything above it (interviewer, planner) is yours to build.
"""

import logging
import time

from openai import AsyncOpenAI

from app.config import get_settings

log = logging.getLogger("consensus.llm")
settings = get_settings()

client = AsyncOpenAI(
    base_url=settings.openrouter_base_url,
    api_key=settings.openrouter_api_key or "missing-key",
    default_headers={
        # Optional OpenRouter attribution headers
        "HTTP-Referer": settings.frontend_origin,
        "X-Title": settings.app_name,
    },
)


async def complete(messages: list[dict], tools: list[dict] | None = None, **kwargs):
    """One model call. Returns the first choice's message (may contain tool_calls).

    Logs latency and token usage for every call. TODO (Week 5): persist these to an
    `agent_runs` table so you can show cost per plan in a trace viewer.
    """
    if not settings.openrouter_api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set (backend/.env)")

    started = time.perf_counter()
    response = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        tools=tools or None,
        max_tokens=settings.agent_max_tokens,
        **kwargs,
    )
    usage = response.usage
    log.info(
        "llm model=%s ms=%d in=%s out=%s",
        settings.llm_model,
        (time.perf_counter() - started) * 1000,
        getattr(usage, "prompt_tokens", "?"),
        getattr(usage, "completion_tokens", "?"),
    )
    return response.choices[0].message
