from importlib.metadata import PackageNotFoundError, version


def storyforge_version() -> str:
    try:
        return version("storyforge")
    except PackageNotFoundError:
        return "0+unknown"
