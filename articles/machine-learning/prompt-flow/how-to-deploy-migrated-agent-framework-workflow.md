---
title: Deploy and operate your migrated Agent Framework workflow
titleSuffix: Azure Machine Learning
description: Set up OpenTelemetry tracing, deploy your Microsoft Agent Framework workflow to Azure Container Apps, add a CI/CD quality gate, and cut over production traffic from Prompt Flow.
author: scottpolly
ms.author: scottpolly
ms.service: azure-machine-learning
ms.subservice: prompt-flow
ms.topic: how-to
ms.date: 04/15/2026
ai-usage: ai-assisted
#CustomerIntent: As a developer who rebuilt my Prompt Flow workflow in Microsoft Agent Framework, I want to deploy it and switch production traffic so that I can complete the migration.
---

# Deploy and operate your migrated Agent Framework workflow

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

This article covers the operations and cutover steps of the Prompt Flow to Microsoft Agent Framework migration: setting up tracing, deploying to Azure Container Apps, adding a CI/CD quality gate, and cutting over production traffic. For the audit, rebuild, and validation steps, see [Rebuild and validate your Prompt Flow workflow in Microsoft Agent Framework](how-to-migrate-prompt-flow-to-agent-framework.md).

## Prerequisites

- Completed the audit, rebuild, and validation steps with a mean parity score ≥ 3.5 in `parity_results.csv`.
- An Application Insights instance.
- An Azure Container Registry and Container Apps environment.
- A GitHub repository with secrets configured for CI/CD.
- Install additional packages:

    ```bash
    pip install azure-monitor-opentelemetry fastapi uvicorn
    ```

## Migrate operations

This step replaces the operational infrastructure that Prompt Flow managed automatically.

| Sub-phase | Replaces | Details |
|---|---|---|
| 4a — Tracing | Prompt Flow built-in run viewer | OpenTelemetry + Application Insights |
| 4b — Deployment | Prompt Flow Managed Online Endpoint | FastAPI + Azure Container Apps |
| 4c — CI/CD | Manual evaluation runs in the Prompt Flow UI | GitHub Actions quality gate |

### Set up tracing with OpenTelemetry

Agent Framework automatically emits OpenTelemetry spans for every executor invocation, agent call, and LLM request. Connect these to Application Insights by calling `configure_azure_monitor()` once at application startup.

1. Add the Application Insights connection string to your `.env` file:

    ```text
    APPLICATIONINSIGHTS_CONNECTION_STRING=<your-connection-string>
    ```

1. Call `configure_azure_monitor()` before any `workflow.run()` call:

    ```python
    import os

    from dotenv import load_dotenv
    from azure.monitor.opentelemetry import configure_azure_monitor

    load_dotenv()

    configure_azure_monitor(
        connection_string=os.environ[
            "APPLICATIONINSIGHTS_CONNECTION_STRING"
        ]
    )

    # All workflow.run() calls after this point emit traces.
    ```

1. View traces in the Azure portal: go to your Application Insights resource and select **Transaction Search**.

> [!IMPORTANT]
> Call `configure_azure_monitor()` at application startup, not inside a handler or after `workflow.run()`. Traces emitted before the call are lost.

### Deploy to Azure Container Apps

Wrap your Agent Framework workflow in a FastAPI service and deploy it as a container.

#### Create the FastAPI wrapper

Create an `app.py` file that exposes a `/ask` endpoint:

```python
"""Wraps an Agent Framework workflow in a FastAPI service."""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from azure.monitor.opentelemetry import configure_azure_monitor

load_dotenv()

# Import your rebuilt workflow
from your_workflow_module import workflow

# Configure tracing if connection string is present.
appinsights_conn = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if appinsights_conn:
    configure_azure_monitor(connection_string=appinsights_conn)


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Agent Framework Workflow Service", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
async def ask(payload: QuestionRequest):
    if not payload.question.strip():
        raise HTTPException(
            status_code=400, detail="Question must not be empty."
        )

    result = await workflow.run(payload.question.strip())
    outputs = result.get_outputs()

    if not outputs:
        raise HTTPException(
            status_code=500,
            detail="Workflow produced no output.",
        )

    return AnswerResponse(answer=outputs[0])
```

Test locally with:

```bash
uvicorn app:app --reload
```

#### Create the Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Deploy with Azure CLI

1. Build and push the container image:

    ```azurecli
    az acr build \
      --registry <your-acr> \
      --image maf-app:latest \
      .
    ```

1. Create the Container App:

    ```azurecli
    az containerapp create \
      --name maf-app \
      --resource-group <your-rg> \
      --environment <your-env> \
      --image <your-acr>.azurecr.io/maf-app:latest \
      --target-port 8000 \
      --ingress external \
      --registry-server <your-acr>.azurecr.io \
      --secrets openai-key="$AZURE_OPENAI_API_KEY" \
      --env-vars \
        AZURE_OPENAI_API_KEY=secretref:openai-key \
        AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/" \
        AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="<deployment>"
    ```

1. Verify the deployment:

    ```azurecli
    APP_URL=$(az containerapp show \
      --name maf-app \
      --resource-group <your-rg> \
      --query "properties.configuration.ingress.fqdn" -o tsv)

    curl "https://${APP_URL}/health"
    ```

> [!TIP]
> For production deployments, use managed identity instead of API keys. Pass `credential=ManagedIdentityCredential()` to `AzureOpenAIChatClient()` and remove `AZURE_OPENAI_API_KEY` from your environment variables. Use Key Vault secret references (`secretref:kv-*`) for any remaining secrets.

### Add a CI/CD quality gate

Create a GitHub Actions workflow that runs the parity check on every push and fails the pipeline if the mean similarity drops below the threshold.

```yaml
name: Evaluate on Deploy
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run parity evaluation
        run: python parity_check.py
        env:
          AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
          AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
          AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: ${{ secrets.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME }}

      - name: Enforce quality gate
        run: |
          python -c "
          import pandas as pd, sys
          df = pd.read_csv('parity_results.csv')
          score = df['similarity'].mean()
          print(f'Mean similarity: {score:.2f} / 5.0')
          sys.exit(0 if score >= 3.5 else 1)
          "
```

Required repository secrets:

- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME`

## Cut over

Switch production traffic to Agent Framework and decommission Prompt Flow resources.

### Pre-cutover checklist

Verify all of the following before proceeding:

- Mean parity score ≥ 3.5 across the full test suite.
- Agent Framework Container App is healthy (`az containerapp show`).
- Tracing is confirmed in Application Insights.
- CI/CD quality gate is passing on the main branch.
- API gateway or client configuration is updated to point at the Agent Framework endpoint.

### Run the cutover

1. Archive your existing Prompt Flow YAML:

    ```bash
    cp -r <your-flow-directory> ./archived-flow/
    ```

1. Delete the Prompt Flow managed online endpoint:

    ```azurecli
    az ml online-endpoint delete \
      --name <your-pf-endpoint> \
      --resource-group <your-rg> \
      --workspace-name <your-ws> \
      --yes
    ```

1. Delete the Prompt Flow connection:

    ```azurecli
    az ml connection delete \
      --name <your-pf-connection> \
      --resource-group <your-rg> \
      --workspace-name <your-ws>
    ```

> [!WARNING]
> Run the cutover commands only after confirming that traffic is routed to the Agent Framework endpoint. Use `--dry-run` flags in your scripts to preview commands before executing them.

### After cutover

- Monitor Application Insights for error spikes in the first 24 hours.
- Keep the archived flow YAML for at least 30 days before deleting.

## Troubleshooting

### No traces appearing in Application Insights

Make sure `configure_azure_monitor()` is called before any `workflow.run()` call — not after, and not inside a handler. Also verify the connection string: Azure portal > your Application Insights resource > **Overview** > **Connection String**.

### `uvicorn` starts but `/ask` returns 500

The most common cause is that `app.py` loaded the wrong workflow file, or the target file doesn't define a module-level `workflow` object. Check the Application Insights trace for the full exception.

### `az containerapp create` fails with an image pull error

Check:

1. `--registry-server` matches your ACR login server exactly (`<name>.azurecr.io`).
1. The Container App's managed identity (or admin credentials) has the `AcrPull` role on the registry.
1. The image tag pushed by `az acr build` matches the tag in `--image`.

### Workflow hangs and never completes

The most common cause is a circular edge definition. Agent Framework uses a superstep execution model and iterates until it reaches the `max_iterations` limit (default: 100). Check your `add_edge()` calls for cycles:

```python
WorkflowBuilder(name="MyWorkflow", max_iterations=10)
```

## Related content

- [Migrate from Prompt Flow to Microsoft Agent Framework](migrate-prompt-flow-to-agent-framework.md)
- [Rebuild and validate your Prompt Flow workflow in Microsoft Agent Framework](how-to-migrate-prompt-flow-to-agent-framework.md)
- [Azure Container Apps documentation](/azure/container-apps/)
- [Azure Monitor OpenTelemetry](/azure/azure-monitor/app/opentelemetry-enable)
- [PromptFlow-to-MAF migration samples](https://github.com/microsoft/agent-framework/tree/main/migration-guide/PromptFlow-to-MAF)
