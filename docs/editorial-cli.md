# Editorial CLI

M2.15 exposes the persisted editorial review boundary without coupling the CLI to any AI provider.

Inspect a run artifact:

```
storyforge run-status run.json
```

The command validates and restores the run before printing halted state and completed stage/gate status.

Create an approval artifact for one completed stage:

```
storyforge review run.json draft approve --reviewer editor -o approval.json
```

Reject it with an optional note:

```
storyforge review run.json draft reject --reviewer editor --note "Revise tone" -o rejection.json
```

Review artifacts use the proposal fingerprint from the restored run, so approval is bound to exactly the proposal shown in that artifact. Ambiguous or missing stage names fail.

Provider execution and automatic resume are intentionally not exposed yet. Provider configuration needs a stable, provider-neutral serialization contract before CLI commands should invoke models.
