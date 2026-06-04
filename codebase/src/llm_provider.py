from dataclasses import dataclass

from langchain_openai import ChatOpenAI

from config import get_env


SUPPORTED_PROVIDERS = {"openai", "openai-compatible", "compatible", "custom"}


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    model_name: str
    api_key: str
    base_url: str


def get_llm_settings():
    return LLMSettings(
        provider=get_env("LLM_PROVIDER", "openai").lower(),
        model_name=get_env("LLM_MODEL_NAME", "gpt-4o-mini"),
        api_key=get_env("LLM_API_KEY"),
        base_url=get_env("LLM_BASE_URL"),
    )


def get_llm_api_key():
    return get_llm_settings().api_key


def get_llm_display_name():
    settings = get_llm_settings()
    return f"{settings.provider} / {settings.model_name}"


def create_chat_model(api_key=None):
    settings = get_llm_settings()
    final_api_key = api_key or settings.api_key

    llm_kwargs = {
        "model": settings.model_name,
        "api_key": final_api_key,
        "temperature": 0,
    }

    if settings.base_url:
        llm_kwargs["base_url"] = settings.base_url

    # ChatOpenAI supports OpenAI-compatible providers when base_url is set.
    if settings.provider not in SUPPORTED_PROVIDERS:
        print(f"Unsupported LLM_PROVIDER={settings.provider}; using ChatOpenAI-compatible settings.")

    return ChatOpenAI(**llm_kwargs)
