# Stable choice IDs and action API

M1.11 adds optional globally unique IDs to choices. Human-facing text and parser aliases can now change without changing the machine identity of an authored transition.

`Session.actions()` exposes currently available actions as structured records containing `id`, display `text`, and parser `commands`. `Session.choose_id()` executes an available transition by stable ID using the same deterministic path as indexed selection.

This interface is intended for web/PWA clients, automated playtesters, accessibility layers, and future AI interpreters. New stories should assign IDs to choices; the schema keeps them optional for compatibility with existing StoryForge sources.
