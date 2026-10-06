import pytest

from storyforge.provider_config import ProviderConfigError, load_provider_config


def config():
    return {
        "format": "storyforge-providers",
        "version": 1,
        "providers": {
            "writer-local": {
                "kind": "ollama-compatible",
                "model": "writer-model",
                "endpoint": "http://localhost:11434",
            },
            "review-cloud": {
                "kind": "openai-compatible",
                "model": "review-model",
                "api_key_env": "REVIEW_API_KEY",
            },
        },
        "roles": {
            "writer": "writer-local",
            "playtester": "review-cloud",
        },
    }


def test_loads_provider_registry_and_role_mapping():
    registry = load_provider_config(config())
    assert registry.roles["writer"] == "writer-local"
    assert registry.providers["writer-local"].model == "writer-model"
    assert registry.providers["review-cloud"].api_key_env == "REVIEW_API_KEY"


@pytest.mark.parametrize("field", ["api_key", "token", "secret", "password"])
def test_inline_secrets_are_rejected(field):
    data = config()
    data["providers"]["review-cloud"][field] = "do-not-store-this"
    with pytest.raises(ProviderConfigError, match="inline secret"):
        load_provider_config(data)


def test_unknown_role_provider_is_rejected():
    data = config()
    data["roles"]["writer"] = "missing"
    with pytest.raises(ProviderConfigError, match="unknown provider"):
        load_provider_config(data)
