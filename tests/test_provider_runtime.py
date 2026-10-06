import pytest

from storyforge.provider_config import ProviderConfigError, load_provider_config
from storyforge.provider_runtime import build_providers, resolve_role_providers


def registry(kind="openai-compatible", key_env="AI_KEY"):
    return load_provider_config(
        {
            "format": "storyforge-providers",
            "version": 1,
            "providers": {
                "main": {
                    "kind": kind,
                    "model": "model-a",
                    "endpoint": "http://localhost/v1/chat/completions",
                    **({"api_key_env": key_env} if key_env else {}),
                }
            },
            "roles": {"writer": "main", "playtester": "main"},
        }
    )


def transport(endpoint, payload, headers):
    return {}


def test_build_resolves_secret_from_supplied_environment():
    providers = build_providers(registry(), transport, {"AI_KEY": "runtime-secret"})
    provider = providers["main"]
    assert provider.api_key == "runtime-secret"
    assert provider.model == "model-a"


def test_role_mapping_reuses_named_provider_instance():
    roles = resolve_role_providers(registry(key_env=None), transport, {})
    assert roles["writer"] is roles["playtester"]


def test_missing_required_secret_fails_before_use():
    with pytest.raises(ProviderConfigError, match="environment variable"):
        build_providers(registry(), transport, {})


def test_unsupported_kind_fails():
    with pytest.raises(ProviderConfigError, match="unsupported provider kind"):
        build_providers(registry(kind="other", key_env=None), transport, {})


def test_ollama_compatible_uses_same_runtime_contract():
    providers = build_providers(
        registry(kind="ollama-compatible", key_env=None), transport, {}
    )
    assert providers["main"].model == "model-a"
