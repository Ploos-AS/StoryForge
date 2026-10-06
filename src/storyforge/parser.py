from dataclasses import dataclass
import re
import unicodedata


@dataclass(frozen=True)
class Command:
    kind: str
    choice: int | None = None


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold().strip()
    return " ".join(text.split())


def parse_command(text: str, choices: tuple[str, ...], commands: tuple[tuple[str, ...], ...] | None = None) -> Command:
    value = _normalize(text)
    if value in {"look", "l", "se", "se deg rundt"}:
        return Command("look")
    if value in {"inventory", "inv", "i", "inventar"}:
        return Command("inventory")
    if value in {"help", "h", "?", "hjelp"}:
        return Command("help")

    match = re.fullmatch(r"(?:choose|choice|velg)?\s*(\d+)", value)
    if match:
        index = int(match.group(1)) - 1
        if 0 <= index < len(choices):
            return Command("choose", index)
        return Command("unknown")

    if commands is not None:
        matches = []
        for index, aliases in enumerate(commands):
            if value in {_normalize(alias) for alias in aliases}:
                matches.append(index)
        if len(matches) == 1:
            return Command("choose", matches[0])
        if len(matches) > 1:
            return Command("unknown")

    exact = [_normalize(choice) for choice in choices]
    if value in exact:
        return Command("choose", exact.index(value))

    prefixed = [i for i, choice in enumerate(exact) if choice.startswith(value) and value]
    if len(prefixed) == 1:
        return Command("choose", prefixed[0])

    return Command("unknown")
