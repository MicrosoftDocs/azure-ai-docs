---
title: Run AI Red Teaming Agent in the cloud (Microsoft Foundry SDK)
titleSuffix: Microsoft Foundry
description: This article provides instructions on how to use the AI Red Teaming Agent to run an automated scan in the cloud of a Generative AI application with the Microsoft Foundry SDK.
ms.service: azure-ai-foundry
ms.custom:
  - references_regions
ms.topic: how-to
ms.date: 11/18/2025
ms.reviewer: minthigpen
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
# customer intent: As a developer, I want to run AI Red Teaming Agent scans in the cloud using the Microsoft Foundry SDK so I can perform comprehensive pre-deployment safety analysis at scale.
---

# Run AI Red Teaming Agent in the cloud (preview)

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

::: moniker range="foundry-classic"

Though the AI Red Teaming Agent (preview) can be run [locally](run-scans-ai-red-teaming-agent.md) during prototyping and development to help identify safety risks, running them in the cloud allows for pre-deployment AI red teaming runs on larger combinations of attack strategies and risk categories for a fuller analysis.

::: moniker-end

::: moniker range="foundry"

Though the AI Red Teaming Agent can be run [locally](run-scans-ai-red-teaming-agent.md) during prototyping and development to help identify safety risks, running them in the cloud allows for the following scenarios:

- Pre-deployment AI red teaming runs on larger combinations of attack strategies and risk categories for a fuller analysis,
- Post-deployment continuous AI red teaming runs that can be scheduled to run at set time intervals
- Agentic-specific risk scenarios to support a minimally sandboxed environment for the AI red teaming run

::: moniker-end

## Prerequisites

::: moniker range="foundry-classic"

[!INCLUDE [uses-fdp-only](../../includes/uses-fdp-only.md)]

[!INCLUDE [evaluation-foundry-project-storage](../../includes/evaluation-foundry-project-storage.md)]

::: moniker-end

::: moniker range="foundry"

- A [Foundry project](/azure/ai-foundry/how-to/create-projects).

::: moniker-end


## Getting started

First, install Microsoft Foundry SDK's project client, which runs the AI Red Teaming Agent in the cloud.

::: moniker range="foundry-classic"

```bash
pip install azure-ai-projects==1.1.0b3 azure-identity
```

::: moniker-end

::: moniker range="foundry"

```bash
pip install azure-ai-projects>=2.0.0b1 azure-identity
```

::: moniker-end

Then, set your environment variables for your Microsoft Foundry resources

::: moniker range="foundry-classic"

```python
import os

endpoint = os.environ["PROJECT_ENDPOINT"] # Sample : https://<account_name>.services.ai.azure.com/api/projects/<project_name>

```

::: moniker-end

::: moniker range="foundry"


```python
import os

endpoint = os.environ["PROJECT_ENDPOINT"] # Sample : https://<account_name>.services.ai.azure.com/api/projects/<project_name>
agent_name = os.environ["AZURE_AI_AGENT_NAME"] # Required. The name of the Agent to perform red teaming evaluation on.
```

::: moniker-end

## Supported targets

::: moniker range="foundry-classic"

Running the AI Red Teaming Agent in the cloud currently only supports Azure OpenAI model deployments in your Foundry project as a target.
::: moniker-end

::: moniker range="foundry"

Running the AI Red Teaming Agent in the cloud currently only supports the following:

- Foundry project deployments
- Azure OpenAI model deployments
- Foundry Agents (prompt and container agents) in your Microsoft Foundry project as a target.

::: moniker-end

## Configure your target model

You can configure your target model deployment in two ways:

### Option 1: Foundry project deployments

If you're using model deployments that are part of your Foundry project, set up the following environment variables:

```python
import os

model_endpoint = os.environ["MODEL_ENDPOINT"] # Sample : https://<account_name>.openai.azure.com
model_api_key = os.environ["MODEL_API_KEY"]
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"] # Sample : gpt-4o-mini
```

### Option 2: Azure OpenAI/Foundry Tools deployments

If you want to use deployments from your Azure OpenAI or Foundry Tools accounts, you first need to connect these resources to your Foundry project through connections.

1. **Create a connection**: Follow the instructions in [Configure project connections](../../foundry-models/how-to/configure-project-connection.md?pivots=ai-foundry-portal#add-a-connection) to connect your Azure OpenAI or AI Services resource to your Foundry project.

2. **Get the connection name**: After connecting the account, you'll see the connection created with a generated name in your Foundry project.

3. **Configure the target**: Use the format `"connectionName/deploymentName"` for your model deployment configuration:

```python
# Format: "connectionName/deploymentName"
model_deployment_name = "my-openai-connection/gpt-4o-mini"
```
::: moniker range="foundry-classic"

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
- For Option 2 (Azure OpenAI/Foundry Tools deployments): Replace `"{{connectionName}}"` with the Azure OpenAI model connection name connected to the Foundry project account, and replace `"{{deploymentName}}"` with the Azure OpenAI deployment name of the Azure OpenAI connection account.

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


::: moniker-end

::: moniker range="foundry"

## Create an AI red team

Create a red team to hold one or more runs that share a data source and risk categories.

# [Python](#tab/python)

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
model_deployment = os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"]

with DefaultAzureCredential() as credential:
    with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
        client = project_client.get_openai_client()

        # Create a red team with built-in safety evaluators
        red_team = client.evals.create(
            name="Red Team Agentic Safety Evaluation",
            data_source_config={"type": "azure_ai_source", "scenario": "red_team"},
            testing_criteria=[
                {
                    "type": "azure_ai_evaluator",
                    "name": "Prohibited Actions",
                    "evaluator_name": "builtin.prohibited_actions",
                    "evaluator_version": "1"
                },
                {
                    "type": "azure_ai_evaluator",
                    "name": "Task Adherence",
                    "evaluator_name": "builtin.task_adherence",
                    "evaluator_version": "1",
                    "initialization_parameters": {"deployment_name": model_deployment},
                },
                {
                    "type": "azure_ai_evaluator",
                    "name": "Sensitive Data Leakage",
                    "evaluator_name": "builtin.sensitive_data_leakage",
                    "evaluator_version": "1"
                },
            ],
        )
        print(f"Created red team: {red_team.id}")
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url 'https://{{account}}.services.ai.azure.com/api/projects/{{project}}/openai/evals?api-version=2025-11-15-preview' \
  --header 'authorization: Bearer <token>' \
  --header 'content-type: application/json' \
  --data '{
  "name": "bardus earum bellum",
  "data_source_config": {
    "type": "azure_ai_source",
    "scenario": "red_team"
  },
  "testing_criteria": [
    {
      "type": "azure_ai_evaluator",
      "name": "Prohibited Actions",
      "evaluator_name": "builtin.prohibited_actions",
      "evaluator_version": "1"
    },
    {
      "type": "azure_ai_evaluator",
      "name": "Task Adherence",
      "evaluator_name": "builtin.task_adherence",
      "evaluator_version": "1",
      "initialization_parameters": {
        "deployment_name": "{{model_deployment}}"
      }
    },
    {
      "type": "azure_ai_evaluator",
      "name": "Sensitive Data Leakage",
      "evaluator_name": "builtin.sensitive_data_leakage",
      "evaluator_version": "1"
    }
  ]
}'
```

---

What it does:

- Creates a red team to hold all red teaming runs
- Configures the red team with three built‑in evaluators (Prohibited Actions, Task Adherence, Sensitive Data Leakage).

You’ll receive:

- A JSON body with the group’s metadata, including ID (save it as `{{red_team_id}}` for later).

## Get a red team

Use this to verify the red team exists and review configuration (criteria, data source, timestamps).

# [Python](#tab/python)

```python
print(f"[Group] Retrieving group by id={red_team.id} ...")
red_team_fetched = client.evals.retrieve(red_team.id)
print("[Group] Response:")
print(red_team_fetched)
```

# [cURL](#tab/curl)

```bash
curl --request GET \
  --url 'https://{{account}}.services.ai.azure.com/api/projects/{{project}}/openai/evals/{{red_team_id}}?api-version=2025-11-15-preview' \
  --header 'authorization: Bearer <token>'
```

---

## Create (or update) an evaluation taxonomy

To red team for the agentic risk category of prohibited actions, you need to be able to confirm, edit, or update the evaluation taxonomy of prohibited actions generated by the prohibited action red teaming workflow. The next example will generate a JSON file with a generated taxonomy of prohibited actions to be used in dynamically generating the attack prompts to test agentic behavior based on user-approved policy. Once you've reviewed and confirmed the taxonomy, it will then be used to create a red teaming run as well as assess the Attack Success Rate (ASR) of the agent outputs.

# [Python](#tab/python)

```python
from azure.ai.projects.models import (
    AzureAIAgentTarget,
    AgentTaxonomyInput,
    EvaluationTaxonomy,
    RiskCategory,
)

# Define the agent target for taxonomy generation
target = AzureAIAgentTarget(
    name=agent_name,
    version=agent_version.version,
)

# Create taxonomy for prohibited actions risk category
taxonomy = project_client.evaluation_taxonomies.create(
    name=agent_name,
    body=EvaluationTaxonomy(
        description="Taxonomy for red teaming run",
        taxonomy_input=AgentTaxonomyInput(
            risk_categories=[RiskCategory.PROHIBITED_ACTIONS],
            target=target
        ),
    )
)
taxonomy_file_id = taxonomy.id
print(f"Created taxonomy: {taxonomy_file_id}")
```

# [cURL](#tab/curl)

```bash
curl --request PUT \
  --url 'https://{{account}}.services.ai.azure.com/api/projects/{{project}}/evaluationtaxonomies/{{name}}?api-version=2025-11-15-preview' \
  --header 'authorization: Bearer <token>' \
  --header 'content-type: application/json' \
  --data '{
  "taxonomyInput": {
    "type": "agent",
    "target": {
      "type": "azure_ai_agent",
      "name": "transmitter",
      "version": "1",
      "tool_descriptions": [
        {
          "name": "Dragon APIs",
          "description": "APIs to get information from local RAG applications"
        }
      ]
    },
    "riskCategories": [
      "ProhibitedActions"
    ]
  }
}'
```

---

What it does:

- Creates/updates a taxonomy resource named `{{name}}` that:
  - Defines an agent target and tool descriptions
  - Specifies the risk categories of `ProhibitedActions`

You’ll reference it

- via a `file_id` URI in the **Create Run** request.

## Create a run in a red team

A run generates items from a source (for example, taxonomy) and red teams the target agent with chosen attack strategies.

# [Python](#tab/python)

```python
# Create a red team run with attack strategies
eval_run = client.evals.runs.create(
    eval_id=red_team.id,
    name="Red Team Agent Safety Eval Run",
    data_source={
        "type": "azure_ai_red_team",
        "item_generation_params": {
            "type": "red_team_taxonomy",
            "attack_strategies": ["Flip", "Base64", "IndirectJailbreak"],
            "num_turns": 5,
            "source": {"type": "file_id", "id": taxonomy_file_id},
        },
        "target": target.as_dict(),
    },
)
print(f"Created run: {eval_run.id}, status: {eval_run.status}")
```

# [cURL](#tab/curl)

```bash
curl --request POST \
  --url 'https://{{account}}.services.ai.azure.com/api/projects/{{project}}/openai/evals/{{red_team_id}}/runs?api-version=2025-11-15-preview' \
  --header 'authorization: Bearer <token>' \
  --header 'content-type: application/json' \
  --data '{
  "name": "vitiosus delectatio doloremque",
  "data_source": {
    "type": "azure_ai_red_team",
    "item_generation_params": {
      "type": "red_team_taxonomy",
      "attack_strategies": [
        "Flip",
        "Base64",
        "IndirectJailbreak"
      ],
      "num_turns": 5,
      "source": {
        "type": "file_id",
        "id": "azureai://accounts/{{account}}/projects/{{project}}/evaluationtaxonomies/{{taxonomy_name}}/versions/{{version}}"
      }
    },
    "target": {
      "type": "azure_ai_agent",
      "name": "grok-bird",
      "version": "1",
      "tool_descriptions": [
        {
          "name": "Dragon APIs",
          "description": "APIs to get information from local RAG applications"
        }
      ]
    }
  }
}'
```

---

Key fields to configure your run:

- `attack_strategies`: For example, "Flip", "Base64", "IndirectJailbreak" (choose the ones you want to test)
- `num_turns`: multi‑turn depth for generated red‑team items
- `source.id`: points to your taxonomy by file‑ID URI
- `target`: the agent under test (name, version, tools)

You’ll receive

- A run object including `id` (save as `{{eval_run_id}}`)

## Get a red teaming run (by ID)

Use this to check status of your red teaming run (for example, queued, running, succeeded, failed).

# [Python](#tab/python)

```python
import time

# Poll for run completion
while True:
    run = client.evals.runs.retrieve(run_id=eval_run.id, eval_id=red_team.id)
    print(f"Status: {run.status}")
    if run.status in ("completed", "failed", "canceled"):
        break
    time.sleep(5)
```

# [cURL](#tab/curl)

```bash
curl --request GET \
  --url 'https://{{account}}.services.ai.azure.com/api/projects/{{project}}/openai/evals/{{red_team_id}}/runs/{{eval_run_id}}?api-version=2025-11-15-preview' \
  --header 'authorization: Bearer <token>'
```

---

> [!NOTE]
> The API is synchronous per request, but runs themselves are processed server‑side; poll this endpoint until completion before fetching output items.

## List red teaming run output items and results

Use this to inspect summary metrics after completion of the red teaming run.

# [Python](#tab/python)

```python
print("[Run] Fetching output items...")
items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=red_team.id))
output_path = os.path.join(data_folder, f"redteam_eval_output_items_{agent_name}.json")
with open(output_path, "w") as f:
    f.write(json.dumps(_to_json_primitive(items), indent=2))
print(f"[Run] Done. Status={run.status}. Output items saved to {output_path}")
```

# [cURL](#tab/curl)

```bash
curl --request GET \
  --url 'https://{{account}}.services.ai.azure.com/api/projects/{{project}}/openai/evals/{{red_team_id}}/runs/{{eval_run_id}}/output_items?api-version=2025-11-15-preview' \
  --header 'authorization: Bearer <token>'
```

---
::: moniker-end

::: moniker range="foundry-classic"

[!INCLUDE [view-ai-red-teaming-results](../../includes/view-ai-red-teaming-results.md)]

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [Example workflow for agent red teaming in the cloud](https://aka.ms/airedteamingagent-sample)
- [REST API Reference Documentation](/rest/api/aifoundry/aiprojects/red-teams)

::: moniker-end

::: moniker range="foundry"

- [Example workflow for agent red teaming in the cloud](https://aka.ms/agent-redteam-sample)
- [REST API reference](../../reference/foundry-project-rest-preview.md#openai-evals---list-evals)

::: moniker-end
