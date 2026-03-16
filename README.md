# Interview Agent Prototype

An interview assistant prototype built around LM Studio, lightweight project scaffolding, and a modular `app/` package layout.

## What this project includes

- LM Studio client integration through the OpenAI-compatible API
- A modular package structure for interview flow, RAG, and scoring layers
- A simple local entry point for manual smoke testing
- Basic test coverage for configuration and compatibility imports

## Project structure

```text
.
|-- app/
|   |-- agents/
|   |-- llm/
|   |-- rag/
|   `-- scoring/
|-- knowledge_base/
|-- docs/
|-- tests/
|-- config.py
`-- main.py
```

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Make sure LM Studio is running locally with an OpenAI-compatible server.
4. Update `config.py` if you want to change the base URL or model.
5. Run `python main.py`.

## Development workflow

- `main`: stable branch
- `dev`: integration branch
- `feature/*`: feature-focused work

## Notes

- `lmstudio_client.py` is kept as a compatibility layer.
- New code should prefer imports from `app/...`.
