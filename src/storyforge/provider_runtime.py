import os
from typing import Mapping

from .provider_config import ProviderConfigError, ProviderRegistry
from .providers.openai_compatible import OpenAICompatibleProvider, Transport


def build_providers(
    registry: ProviderRegistry,
    transport: Transport,
    environ: Mapping[str, str] | None = None,
) -> dict[str, OpenAICompatibleProvider]:
    env = os.environ if environ is None else environ
    instances = {}

    for name, config in registry.providers.items():
        if config.kind not in {"openai-compatible", "ollama-compatible"}:
            raise ProviderConfigError(f"unsupported provider kind {config.kind!r}")
        if not config.endpoint:
            raise ProviderConfigError(f"provider {name!r} requires endpoint")

        api_key = None
        if config.api_key_env:
            api_key = env.get(config.api_key_env)
            if not api_key:
                raise ProviderConfigError(
                    f"provider {name!r} requires environment variable "
                    f"{config.api_key_env!r}"
                )

        instances[name] = OpenAICompatibleProvider(
            config.endpoint, config.model, transport, api_key
        )

    return instances


def resolve_role_providers(
    registry: ProviderRegistry,
    transport: Transport,
    environ: Mapping[str, str] | None = None,
) -> dict[str, OpenAICompatibleProvider]:
    instances = build_providers(registry, transport, environ)
    return {
        role: instances[provider_name]
        for role, provider_name in registry.roles.items()
    }
