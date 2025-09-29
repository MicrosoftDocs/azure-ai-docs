# Stage 1 Prototype Sample (Idea → Prototype)

This folder contains the scaffold referenced in the tutorial **Stage 1 (Idea → Prototype) - Build and evaluate a code-first enterprise agent**.

## Contents

```
stage1-prototype-sample/
  requirements.txt
  Dockerfile
  README.md
  .gitignore
  .env.example
  src/agent_app/
    __init__.py
    config.py
    build_agent.py
    mcp_client.py
    run_batch_eval.py
    multi_agent.py
  assets/
    eval_questions.jsonl
  tests/
    test_agent_smoke.py
```

## Quick start (local)

1. Copy `.env.example` to `.env` and fill values.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create the initial agent:
   ```bash
   python -m agent_app.build_agent
   ```
4. Run a (placeholder) batch evaluation:
   ```bash
   python -m agent_app.run_batch_eval
   ```

## Placeholders / Verification

Strings marked `[TO VERIFY]` depend on the latest Azure AI Foundry SDK surface. Replace them with confirmed class names, method signatures, and package identifiers before publishing.

## Security / Secrets

Never commit a real `.env`. Use managed identity where possible instead of static credentials.

## Next Steps

- Replace MCP placeholder with real MCP tool registration once docs confirm usage.
- Add official evaluator integration for groundedness/relevance/coherence.
- Introduce tracing & logging (Application Insights) in Stage 2.
