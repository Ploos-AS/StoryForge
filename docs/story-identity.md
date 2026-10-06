# Story identity

M1.14 introduces stable story identity metadata:

```yaml
metadata:
  id: lighthouse
  version: 0.1.0
  title: The Lighthouse
```

`id` is a machine identifier independent of display title. `version` is a semantic-version-shaped content version. Both remain optional in IR v0 for compatibility, but new projects created by `storyforge init` receive an ID and version automatically. The ID can be supplied with `--id`; otherwise it is derived from the title. The initial version defaults to `0.1.0`.

When both fields are present, M1.13 save files are bound to that exact story ID and version. Loading a bound save into another story or version is rejected. Older/unbound saves remain loadable.

Explicit save migration between story versions is a future feature; StoryForge does not silently assume that state from one content version is compatible with another.
