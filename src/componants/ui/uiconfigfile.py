"""
Central config for everything the sidebar renders.
Keeping this separate means adding a new LLM provider, model,
or usecase never touches UI logic — just this dict.
"""

APP_TITLE = "LangGraph: Build Stateful Agentic AI graph"
APP_ICON = "🕸️"

LLM_OPTIONS = ["Groq", "OpenAI"]

MODEL_OPTIONS = {
    "Groq": [
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b",
        "qwen/qwen3.6-27b",
        "groq/compound",
        "whisper-large-v3",
    ],
    "OpenAI": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4.1",
    ],
}

USECASE_OPTIONS = [
    "Basic Chatbot",
    "Chatbot with Web Search",
    "AI News Summarizer",
]

# Which sidebar controls each usecase needs beyond the LLM block
USECASE_REQUIRES_API_KEY = {
    "Basic Chatbot": [],
    "Chatbot with Web Search": ["TAVILY_API_KEY"],
    "AI News Summarizer": [],
}


class Config:
    """Small wrapper kept for parity with the original tutorial-style API."""

    def get_llm_options(self):
        return LLM_OPTIONS

    def get_model_options(self, llm: str):
        return MODEL_OPTIONS.get(llm, [])

    def get_usecase_options(self):
        return USECASE_OPTIONS

    def get_extra_keys_for_usecase(self, usecase: str):
        return USECASE_REQUIRES_API_KEY.get(usecase, [])
