---
title: Run AI Red Teaming Agent in the cloud (Azure AI Foundry SDK)
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to use the AI Red Teaming Agent to run an automated scan in the cloud of a Generative AI application with the Azure AI Foundry SDK.
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 09/02/2025
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
---

# Run AI Red Teaming Agent in the cloud (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Though the AI Red Teaming Agent (preview) can be run [locally](run-scans-ai-red-teaming-agent.md) during prototyping and development to help identify safety risks, running them in the cloud allows for pre-deployment AI red teaming runs on larger combinations of attack strategies and risk categories for a fuller analysis.

## Prerequisites

[!INCLUDE [uses-fdp-only](../../includes/uses-fdp-only.md)]

[!INCLUDE [evaluation-foundry-project-storage](../../includes/evaluation-foundry-project-storage.md)]

## Getting started

First, install Azure AI Foundry SDK's project client, which runs the AI Red Teaming Agent in the cloud.

```python
uv install azure-ai-projects==1.1.0b3 azure-identity
```

> [!NOTE]
> For more detailed information, see the [REST API Reference Documentation](/rest/api/aifoundry/aiprojects/red-teams).

Then, set your environment variables for your Azure AI Foundry resources

```python
import os

endpoint = os.environ["PROJECT_ENDPOINT"] # Sample : https://<account_name>.services.ai.azure.com/api/projects/<project_name>

```

## Supported targets

Running the AI Red Teaming Agent in the cloud currently only supports Azure OpenAI model deployments in your Azure AI Foundry project as a target.

## Configure your target

You can configure your target model deployment in two ways:

### Option 1: Using Foundry project deployments

If you're using model deployments that are part of your Azure AI Foundry project, set up the following environment variables:

```python
import os

model_endpoint = os.environ["MODEL_ENDPOINT"] # Sample : https://<account_name>.openai.azure.com
model_api_key = os.environ["MODEL_API_KEY"]
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"] # Sample : gpt-4o-mini
```

### Option 2: Using Azure OpenAI/AI Services deployments

If you want to use deployments from your Azure OpenAI or AI Services accounts, you first need to connect these resources to your Foundry project through connections.

1. **Create a connection**: Follow the instructions in [Configure project connections](../../foundry-models/how-to/configure-project-connection.md?pivots=ai-foundry-portal#add-a-connection) to connect your Azure OpenAI or AI Services resource to your Foundry project.

2. **Get the connection name**: After connecting the account, you'll see the connection created with a generated name in your Foundry project.

3. **Configure the target**: Use the format `"connectionName/deploymentName"` for your model deployment configuration:

```python
# Format: "connectionName/deploymentName"
model_deployment_name = "my-openai-connection/gpt-4o-mini"
```

## Create an AI red teaming run

# [Python](#tab/python)

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RedTeam,
    AzureOpenAIModelConfiguration,
    AttackStrategy,
    RiskCategory,
)

with AIProjectClient(
  endpoint=endpoint,
  credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
) as project_client:

  # Create target configuration for testing an Azure OpenAI model
  target_config = AzureOpenAIModelConfiguration(model_deployment_name=model_deployment_name)

  # Instantiate the AI Red Teaming Agent
  red_team_agent = RedTeam(
      attack_strategies=[AttackStrategy.BASE64],
      risk_categories=[RiskCategory.VIOLENCE],
      display_name="red-team-cloud-run", 
      target=target_config,
  )

  # Create and run the red teaming scan
  # If you configured target using Option 1, use:
  # headers = {"model-endpoint": model_endpoint, "api-key": model_api_key}
  # If you configured target using Option 2, use:
  # headers = {}

  # Choose one of the following based on your configuration option:
  headers = {"model-endpoint": model_endpoint, "api-key": model_api_key}  # For Option 1
  # headers = {}  # For Option 2

  red_team_response = project_client.red_teams.create(red_team=red_team_agent, headers=headers)
```

# [cURL](#tab/curl)

```bash
curl --request POST \  --url https://{{account}}.services.ai.azure.com/api/projects/{{project}}/redteams/runs:run \  --header 'content-type: application/json' \  --header 'authorization: Bearer {{ai_token}}'  --data '{  "displayName": "Red Team Scan #1",  "riskCategories": [ "Violence" ],  "attackStrategy": [ "Flip" ],  "numTurns": 1,  "target": {    "type": "AzureOpenAIModel",    "modelDeploymentName": "{{connectionName}}/{{deploymentName}}"  }}'
```

- Replace `{{account}}`, `{{project}}` with Foundry Project account name and project name.
- Replace `{{ai_token}}` with Bearer token with audience "<https://ai.azure.com>"
- For Option 1 (Foundry project deployments): Replace `"{{connectionName}}/{{deploymentName}}"` with just `"{{deploymentName}}"` (your model deployment name).
- For Option 2 (Azure OpenAI/AI Services deployments): Replace `"{{connectionName}}"` with the Azure OpenAI model connection name connected to the Foundry project account, and replace `"{{deploymentName}}"` with the Azure OpenAI deployment name of the Azure OpenAI connection account.

---

## Get an AI red teaming run

# [Python](#tab/python)

```python
# Use the name returned by the create operation for the get call
get_red_team_response = project_client.red_teams.get(name=red_team_response.name)
print(f"Red Team scan status: {get_red_team_response.status}")
```

# [cURL](#tab/curl)

```bash
curl --request GET \  --header 'authorization: Bearer {{ai_token}}'  --url https://{{account}}.services.ai.azure.com/api/projects/{{project}}/redteams/runs/{{scan_id}}
```

- Replace `"{{scan_id}"` with the ID returned by the POST API.

---

## List all AI red teaming runs

# [Python](#tab/python)

```python
for scan in project_client.red_teams.list():
  print(f"Found scan: {scan.name}, Status: {scan.status}")
```

# [cURL](#tab/curl)

```bash
curl --request GET \  --header 'authorization: Bearer {{ai_token}}'  --url https://{{account}}.services.ai.azure.com/api/projects/{{project}}/redteams/runs
```

---

[!INCLUDE [view-ai-red-teaming-results](../../includes/view-ai-red-teaming-results.md)]

## Related content

Try out an [example workflow](https://aka.ms/airedteamingagent-sample) in our GitHub samples.
