# Command parser

M1.9 adds a deterministic parser in front of the text runtime. It accepts one-based choice numbers, `choose N`, exact choice text, unambiguous choice prefixes, and meta commands for `look`, `inventory`, and `help`. Norwegian aliases are included for the meta commands.

The parser returns a structured `Command`; it never mutates game state. Only `Session` executes a selected choice. This is the contract future natural-language and LLM parsers must follow: interpretation may be probabilistic, but authoritative world state remains deterministic.

World verbs such as arbitrary `take X` or `use X on Y` are intentionally not inferred yet. Those need explicit IR affordances so a parser cannot invent actions that the authored world does not permit.
