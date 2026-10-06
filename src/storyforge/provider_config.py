from dataclasses import dataclass


PROVIDER_CONFIG_FORMAT = "storyforge-providers"
PROVIDER_CONFIG_VERSION = 1


class ProviderConfigError(ValueError):
    pass


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    kind: str
    model: str
    endpoint: str | None = None
    api_key_env: str | None = None


@dataclass(frozen=True)
class ProviderRegistry:
    providers: dict[str, ProviderConfig]
    roles: dict[str, str]


def load_provider_config(data: dict) -> ProviderRegistry:
    if data.get("format") != PROVIDER_CONFIG_FORMAT:
        raise ProviderConfigError("unsupported provider config format")
    if data.get("version") != PROVIDER_CONFIG_VERSION:
        raise ProviderConfigError("unsupported provider config version")

    raw_providers = data.get("providers")
    raw_roles = data.get("roles")
    if not isinstance(raw_providers, dict) or not isinstance(raw_roles, dict):
        raise ProviderConfigError("providers and roles must be objects")

    providers = {}
    for name, raw in raw_providers.items():
        if not isinstance(name, str) or not name:
            raise ProviderConfigError("provider name must be non-empty")
        if not isinstance(raw, dict):
            raise ProviderConfigError(f"provider {name!r} must be an object")
        kind = raw.get("kind")
        model = raw.get("model")
        if not isinstance(kind, str) or not kind:
            raise ProviderConfigError(f"provider {name!r} kind must be non-empty")
        if not isinstance(model, str) or not model:
            raise ProviderConfigError(f"provider {name!r} model must be non-empty")
        endpoint = raw.get("endpoint")
        api_key_env = raw.get("api_key_env")
        if endpoint is not None and not isinstance(endpoint, str):
            raise ProviderConfigError(f"provider {name!r} endpoint must be a string")
        if api_key_env is not None and not isinstance(api_key_env, str):
            raise ProviderConfigError(f"provider {name!r} api_key_env must be a string")
        if any(key in raw for key in ("api_key", "token", "secret", "password")):
            raise ProviderConfigError(f"provider {name!r} contains an inline secret")
        providers[name] = ProviderConfig(name, kind, model, endpoint, api_key_env)

    roles = {}
    for role, provider_name in raw_roles.items():
        if not isinstance(role, str) or not isinstance(provider_name, str):
            raise ProviderConfigError("role mappings must be strings")
        if provider_name not in providers:
            raise ProviderConfigError(
                f"role {role!r} references unknown provider {provider_name!r}"
            )
        roles[role] = provider_name

    return ProviderRegistry(providers, roles)
