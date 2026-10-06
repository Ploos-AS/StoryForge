# OCI qualification

The OCI workflow does more than prove that the image can be assembled. A separate qualification job builds the packaged image and executes StoryForge inside it.

The qualification currently proves:

- the installed CLI starts through the image entrypoint;
- the Lighthouse reference story validates;
- the deterministic solver completes against Lighthouse;
- deterministic analysis completes against Lighthouse;
- the repository is mounted read-only during reference-story checks.

This catches packaging errors that Python unit tests cannot see, including missing package data, broken console entrypoints, dependency omissions, and container-only path problems.

AI-backed network providers are intentionally excluded from OCI qualification. Their nondeterminism, credentials, and external availability should not decide whether the deterministic StoryForge runtime image is healthy.
