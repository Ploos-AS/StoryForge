# Declarative gate policy

Pipeline stages may declare a gate by stable policy name:

```yaml
gate: puzzle-solver
```

or compose gates in order:

```yaml
gate:
  - puzzle-solver
  - human-approval
```

Version 1 recognizes only `puzzle-solver` and `human-approval`. Unknown names fail closed.

`puzzle-solver` invokes StoryForge's deterministic puzzle qualification.

`human-approval` deliberately rejects the first run with `human approval required`. This preserves the generated proposal in the editorial run artifact instead of applying it. A later resume layer can replace that pending policy with an approval gate bound to the exact proposal fingerprint.

Gate lists use ordered AND semantics. Evaluation stops at the first rejected gate.

No arbitrary Python import, expression, shell command, or plugin name is accepted from pipeline configuration.
