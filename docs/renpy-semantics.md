# Ren'Py semantic parity

M1.7 exports StoryForge's deterministic state model instead of only scene flow. Semantic adventure actions are lowered with the same compiler used by solving and analysis. Requirements become Ren'Py menu conditions, and effects mutate generated StoryForge runtime state.

Exported state covers global variables, player inventory, NPC item ownership, and generic character attributes. This closes the previous gap where a story could validate and solve correctly in StoryForge while the generated Ren'Py game ignored puzzle state.

The generated script remains a build artifact: edit the StoryForge source, not the exported `.rpy` file.
