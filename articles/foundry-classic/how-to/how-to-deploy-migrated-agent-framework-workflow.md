---
title: Deploy and operate your migrated Agent Framework workflow for Foundry (classic)
titleSuffix: Microsoft Foundry
description: Set up tracing, deploy your Microsoft Agent Framework workflow to Azure Container Apps, add a CI/CD quality gate, and cut over production traffic from Prompt Flow.
author: scottpolly
ms.author: scottpolly
ms.service: microsoft-foundry
ms.topic: how-to
ms.date: 04/15/2026
ai-usage: ai-assisted
#CustomerIntent: As a developer who rebuilt my Prompt Flow workflow in Microsoft Agent Framework, I want to deploy it and switch production traffic so that I can complete the migration.
---

# Deploy and operate your migrated Agent Framework workflow for Foundry (classic)

[!INCLUDE [prompt-flow-retirement](../includes/prompt-flow-retirement.md)]

This article covers the operations and cutover steps of the Prompt Flow to Microsoft Agent Framework migration: setting up tracing, deploying to Azure Container Apps, adding a CI/CD quality gate, and cutting over production traffic. For the audit, rebuild, and validation steps, see [Audit, rebuild, and validate your Prompt Flow workflow in Microsoft Agent Framework](how-to-migrate-prompt-flow-to-agent-framework.md). For the migration overview and concept mapping, see [Migrate from Prompt Flow to Microsoft Agent Framework](prompt-flow-migration-overview.md).

## Prerequisites

- Completed the audit, rebuild, and validation steps with a mean parity score ≥ 3.5 in `parity_results.csv`. For details, see [Audit, rebuild, and validate your Prompt Flow workflow](how-to-migrate-prompt-flow-to-agent-framework.md).
- An Application Insights instance.
- An Azure Container Registry and Container Apps environment.
- A GitHub repository with secrets configured for CI/CD.
- Install additional packages:

    ```bash
    pip install fastapi uvicorn azure-monitor-opentelemetry
    ```

## Migrate operations

This step replaces the operational infrastructure that Prompt Flow managed automatically.

| Sub-phase | Replaces | Details |
|---|---|---|
| 4a — Tracing | Prompt Flow built-in run viewer | OpenTelemetry + Application Insights |
| 4b — Deployment | Prompt Flow Managed Online Endpoint | FastAPI + Azure Container Apps |
| 4c — CI/CD | Manual evaluation runs in the Prompt Flow UI | GitHub Actions quality gate |

### Set up tracing

Foundry has native tracing integration with Agent Framework. Agents built with Agent Framework automatically emit traces when tracing is enabled for your Foundry project. For detailed setup instructions, see [Configure tracing for AI agent frameworks](../../foundry/observability/how-to/trace-agent-framework.md).

For standalone deployments outside Foundry (for example, Azure Container Apps), use `configure_azure_monitor()`:

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

#### Create the requirements file

Create a `requirements.txt` file with your project dependencies:

```text
agent-framework>=1.0.0
agent-framework-foundry
fastapi
uvicorn
python-dotenv
azure-identity
azure-monitor-opentelemetry
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

If you don't have an Azure Container Registry and Container Apps environment, create them:

```azurecli
az acr create --name <your-acr> --resource-group <your-rg> --sku Basic
az containerapp env create \
  --name <your-env> \
  --resource-group <your-rg> \
  --location <your-location>
```

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
      --env-vars \
        FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com" \
        FOUNDRY_MODEL="<deployment>"
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
> For production deployments, use managed identity. `DefaultAzureCredential` is already configured in the `FoundryChatClient` examples, so managed identity works automatically in Azure-hosted environments. Remove any API key environment variables.

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
          FOUNDRY_PROJECT_ENDPOINT: ${{ secrets.FOUNDRY_PROJECT_ENDPOINT }}
          FOUNDRY_MODEL: ${{ secrets.FOUNDRY_MODEL }}

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

## Cut over

Switch production traffic to Agent Framework and decommission Prompt Flow resources.

### Pre-cutover checklist

Verify all of the following items before proceeding:

- [ ] Mean parity score is 3.5 or higher across the full test suite.
- [ ] Agent Framework Container App (or Agent Service deployment) is healthy.
- [ ] Tracing is confirmed in Application Insights or the Foundry portal.
- [ ] CI/CD quality gate is passing on the main branch.
- [ ] API gateway or client configuration is updated to point at the Agent Framework endpoint.

### Run the cutover

1. Archive your existing Prompt Flow YAML.

    ```bash
    cp -r <your-flow-directory> ./archived-flow/
    ```

1. Delete the Prompt Flow managed online endpoint.

    ```azurecli
    az ml online-endpoint delete \
      --name <your-pf-endpoint> \
      --resource-group <your-rg> \
      --workspace-name <your-ws> \
      --yes
    ```

1. Delete the Prompt Flow connection.

    ```azurecli
    az ml connection delete \
      --name <your-pf-connection> \
      --resource-group <your-rg> \
      --workspace-name <your-ws>
    ```

> [!WARNING]
> Run the cutover commands only after you confirm that traffic is routed to the Agent Framework endpoint. Use `--dry-run` flags in your scripts to preview commands before executing them.

### After cutover

- Monitor Application Insights (or the Foundry portal tracing view) for error spikes in the first 24 hours.
- Keep the archived flow YAML for at least 30 days before deleting.

## Troubleshooting

### No traces appearing in Application Insights

Make sure you call `configure_azure_monitor()` before any `workflow.run()` call. Also verify the connection string: Azure portal > your Application Insights resource > **Overview** > **Connection String**.

For Foundry-hosted deployments, verify tracing is enabled for your project in the Foundry portal.

### `uvicorn` starts but `/ask` returns 500

The most common cause is that `app.py` loaded the wrong workflow file, or the target file doesn't define a module-level `workflow` object. Check the Application Insights trace for the full exception.

### `az containerapp create` fails with an image pull error

Check:

1. `--registry-server` matches your ACR login server exactly (`<name>.azurecr.io`).
1. The Container App's managed identity (or admin credentials) has the `AcrPull` role on the registry.
1. The image tag pushed by `az acr build` matches the tag in `--image`.

### `CredentialUnavailableError` or `ClientAuthenticationError`

`DefaultAzureCredential` tries multiple credential sources in order. If all sources fail, the error message lists every attempted credential.

1. Confirm your Azure CLI session is current: `az account show`.
1. Verify your account has access to the Foundry project: `az account set --subscription <your-subscription-id>`.
1. For managed identity in Container Apps, ensure the identity has the **Cognitive Services User** role on your Foundry resource.

### Workflow hangs and never completes

The most common cause is a circular edge definition. Set a `max_iterations` limit to break infinite loops and check your `add_edge()` calls for cycles.

```python
start_exec = YourStartExecutor(id="start")
workflow = WorkflowBuilder(
    max_iterations=10, start_executor=start_exec
).build()
```

## Related content

- [Audit, rebuild, and validate your Prompt Flow workflow in Microsoft Agent Framework](how-to-migrate-prompt-flow-to-agent-framework.md)
- [Migrate from Prompt Flow to Microsoft Agent Framework](prompt-flow-migration-overview.md)
- [Configure tracing for AI agent frameworks](../../foundry/observability/how-to/trace-agent-framework.md)
- [Microsoft Agent Framework on GitHub](https://github.com/microsoft/agent-framework)
- [Azure Container Apps documentation](/azure/container-apps/)
- [Azure Monitor OpenTelemetry](/azure/azure-monitor/app/opentelemetry-enable)
