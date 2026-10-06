# Command affordances

M1.10 lets an authored choice declare explicit parser phrases with `commands`. For example, a choice may expose `take key`, `take rusty key`, and `pick up key` while retaining a more narrative menu label.

Affordances are aliases for choices, not a second gameplay system. Requirements are evaluated first, so commands for unavailable choices are not exposed to the parser. Selecting an affordance executes the exact same deterministic transition as selecting the corresponding menu choice.

This also defines a safe input surface for future natural-language/LLM parsing: a model may map free text onto currently available affordances, but it cannot invent a transition that is absent from the authored IR.
