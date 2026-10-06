from storyforge.parser import Command, parse_command


CHOICES = ("Take the rusty key", "Walk to lighthouse", "Wait")


def test_number_and_choose_number():
    assert parse_command("2", CHOICES) == Command("choose", 1)
    assert parse_command("choose 1", CHOICES) == Command("choose", 0)


def test_exact_and_unique_prefix_matching():
    assert parse_command("WAIT", CHOICES) == Command("choose", 2)
    assert parse_command("walk", CHOICES) == Command("choose", 1)


def test_ambiguous_or_invalid_is_unknown():
    choices = ("Take key", "Take coin")
    assert parse_command("take", choices) == Command("unknown")
    assert parse_command("99", choices) == Command("unknown")


def test_meta_commands():
    assert parse_command("look", CHOICES) == Command("look")
    assert parse_command("i", CHOICES) == Command("inventory")
    assert parse_command("help", CHOICES) == Command("help")


def test_norwegian_meta_commands():
    assert parse_command("se", CHOICES) == Command("look")
    assert parse_command("inventar", CHOICES) == Command("inventory")
    assert parse_command("hjelp", CHOICES) == Command("help")
