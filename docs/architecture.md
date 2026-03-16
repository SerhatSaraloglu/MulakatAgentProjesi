# Architecture

This repository is organized around a small interview assistant prototype that talks to LM Studio through the OpenAI-compatible API.

## Current layout

- `main.py`: simple local entry point for a manual smoke run.
- `config.py`: root runtime configuration for LM Studio connectivity.
- `app/agents/`: interview flow orchestration placeholders.
- `app/llm/`: provider client, schemas, and service boundaries.
- `app/rag/`: retrieval pipeline placeholders.
- `app/scoring/`: scoring pipeline placeholders.
- `knowledge_base/`: role-specific prompt and knowledge data.
- `tests/`: lightweight smoke tests for import paths and configuration wiring.

## Compatibility notes

Some root-level modules remain as compatibility shims while the codebase moves toward the package structure under `app/`.
New code should prefer package imports such as `app.llm.providers.lm_studio.client`.
