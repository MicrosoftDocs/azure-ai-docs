---
title: Run AI Red Teaming Agent in the cloud (Azure AI Foundry SDK)
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to use the AI Red Teaming Agent to run an automated scan in the cloud of a Generative AI application with the Azure AI Foundry SDK.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 06/03/2025
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
---

# Run AI Red Teaming Agent in the cloud (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Though the AI Red Teaming Agent (preview) can be run [locally](run-scans-ai-red-teaming-agent.md) during prototyping and development to help identify safety risks, running them in the cloud allows for pre-deployment AI red teaming runs on larger combinations of attack strategies and risk categories for a fuller analysis.

## Prerequisites

[!INCLUDE [uses-fdp-only](../../includes/uses-fdp-only.md)]

- An Azure AI Foundry project. To learn more, see [Create a project](../create-projects.md).

If this is your first time running evaluations or AI red teaming runs on your Azure AI Foundry project, you might need to do a few additional setup steps.

1. [Create and connect your storage account](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/infrastructure-setup/01-connections/connection-storage-account.bicep) to your Azure AI Foundry project at the resource level. This bicep template provisions and connects a storage account to your Foundry project with key authentication.
2. Make sure the connected storage account has access to all projects.
3. If you connected your storage account with Microsoft Entra ID, make sure to give MSI (Microsoft Identity) permissions for Storage Blob Data Owner to both your account and Foundry project resource in Azure portal.

## Getting started

First, install Azure AI Foundry SDK's project client which runs the AI Red Teaming Agent in the cloud

```python
uv install azure-ai-projects azure-identity
```

> [!NOTE]
> For more detailed information, see the [REST API Reference Documentation](/rest/api/aifoundry/aiprojects/red-teams).

Then, set your environment variables for your Azure AI Foundry resources

```python
import os

endpoint = os.environ["PROJECT_ENDPOINT"] # Sample : https://<account_name>.services.ai.azure.com/api/projects/<project_name>
model_endpoint = os.environ["MODEL_ENDPOINT"] # Sample : https://<account_name>.services.ai.azure.com
model_api_key= os.environ["MODEL_API_KEY"]
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"] # Sample : gpt-4o-mini
```

## Supported targets

Running the AI Red Teaming Agent in the cloud currently only supports Azure OpenAI model deployments in your Azure AI Foundry project as a target.

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
red_team_response = project_client.red_teams.create(red_team=red_team_agent, headers={"model-endpoint": model_endpoint, "api-key": model_api_key,})
```

# [cURL](#tab/curl)

```bash
curl --request POST \  --url https://{{account}}.services.ai.azure.com/api/projects/{{project}}/redteams/runs:run \  --header 'content-type: application/json' \  --header 'authorization: Bearer {{ai_token}}'  --data '{  "scanName": "sample_scan_magic_1",  "riskCategories": [    "Violence"  ],  "attackStrategy": [    "Flip"  ],  "numTurns": 1,  "target": {    "type": "AzureOpenAIModel",    "modelDeploymentName": "{{connectionName}}/{{deploymentName}}"  }}'
```

- Replace `{{account}}`, `{{project}}` with Foundry Project account name and project name.
- Replace `{{ai_token}}` with Bearer token with audience "<https://ai.azure.com>"
- Replace `"{{connectionName}}"` with the Azure OpenAI model connection name connected to the Foundry project account.
- Replace `"{{deploymentName}}"` with the Azure OpenAI deployment name of the AOAI connection account.

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

Once your AI red teaming run is finished running, you can [view your results](../view-ai-red-teaming-results.md) in your Azure AI Foundry project.

## Related content

Try out an [example workflow](https://aka.ms/airedteamingagent-sample) in our GitHub samples.
