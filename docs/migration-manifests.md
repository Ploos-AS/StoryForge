# Migration manifests

Story projects may keep declarative save migrations in a `migrations/` directory. Each YAML file contains one version edge:

```yaml
from: 1.0.0
to: 1.1.0
operations:
  - rename_scene:
      from: old_room
      to: new_room
```

Files are loaded in deterministic filename order. The manifest validator rejects duplicate source versions, self edges, missing version endpoints, and malformed operation entries. Runtime migration remains handled by the M1.15 migration engine.
