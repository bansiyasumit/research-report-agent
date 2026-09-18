"""
Builds a CrewAI LLM configured for Google Gemini, using the user's own
free API key passed in at call time. Nothing here is stored, logged, or
read from os.environ.
"""

from crewai import LLM
from google.genai import types

# Model choices offered in the sidebar. Google has fully retired the
# 2.x/2.5.x Gemini generations for new API keys (both "gemini-2.5-flash"
# and "gemini-2.5-flash-lite" 404'd with a message pointing at their 3.x
# replacements) -- only 3.x models work now. Within 3.x, "gemini-3.6-flash"
# is the newest frontier model and its free tier is capped at ~20
# requests/DAY, far too low for a multi-agent run (3 agents x multiple
# reasoning/tool steps each). "-lite" models are the cheaper tier and,
# consistent with every past Gemini generation, carry much higher
# free-tier request quotas, so gemini-3.5-flash-lite is the default.
MODEL_OPTIONS = {
    "Gemini 3.5 Flash-Lite (recommended — highest free quota)": "gemini/gemini-3.5-flash-lite",
    "Gemini 3.1 Flash-Lite": "gemini/gemini-3.1-flash-lite",
    "Gemini 3.6 Flash (newest — ~20 free requests/day)": "gemini/gemini-3.6-flash",
}
DEFAULT_MODEL = MODEL_OPTIONS["Gemini 3.5 Flash-Lite (recommended — highest free quota)"]

# The Gemini free tier returns 503 UNAVAILABLE under high demand fairly
# often. crewai's native Gemini provider passes client_params straight
# into google-genai's Client, which has its own retry/backoff support --
# so retries happen inside the SDK instead of surfacing as a failed run.
_RETRY_OPTIONS = types.HttpRetryOptions(
    attempts=5,
    initial_delay=1.0,
    max_delay=20.0,
    http_status_codes=[429, 500, 502, 503, 504],
)


def build_llm(api_key: str, model: str | None = None) -> LLM:
    if not api_key:
        raise ValueError("A Gemini API key is required")

    return LLM(
        model=model or DEFAULT_MODEL,
        api_key=api_key,
        client_params={"http_options": types.HttpOptions(retry_options=_RETRY_OPTIONS)},
    )
