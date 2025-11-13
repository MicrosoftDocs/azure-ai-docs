---
manager: salmanq
author: pranavp
ms.author: pranavp
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: include
ms.date: 09/25/2025
---
| [Reference documentation](/rest/api/aifoundry/aiagents/) |

## Prerequisites

[!INCLUDE [universal-prerequisites](universal-prerequisites.md)]



## Configure and run an agent

To authenticate your API requests, use the [az login](/cli/azure/authenticate-azure-cli-interactively) command to sign into your Azure subscription.

```azurecli
az login
```

Next, you'll need to fetch the Entra ID token to provide as authorization to the API calls. Fetch the token using the CLI command:
```azurecli
az account get-access-token --resource 'https://ai.azure.com' | jq -r .accessToken | tr -d '"'
```
Set the access token as an environment variable named `AGENT_TOKEN`.

To successfully make REST API calls to Foundry Agent Service, you will need to use your project's endpoint:

`https://<your_ai_service_name>.services.ai.azure.com/api/projects/<your_project_name>`

For example, your endpoint will look something like:

`https://exampleaiservice.services.ai.azure.com/api/projects/project`

Set this endpoint as an environment variable named `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`.

> [!NOTE]
> * For `api-version` parameter, the GA API version is `2025-05-01` and the latest preview API version is `2025-05-15-preview`. You must use the preview API for tools that are in preview. 
> * Consider making your API version an environment variable, such as `$API_VERSION`.

### Create an agent

> [!NOTE]
> With Azure AI Agents Service the `model` parameter requires model deployment name. If your model deployment name is different than the underlying model name, then you would adjust your code to ` "model": "{your-custom-model-deployment-name}"`.

```console
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a helpful agent.",
    "name": "my-agent",
    "tools": [{"type": "code_interpreter"}],
    "model": "gpt-4o-mini"
  }'
```

### Create a thread

```console
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

### Add a user question to the thread

```console
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?"
    }'
```

### Run the thread

```console
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```console
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

### Retrieve the agent response

```console
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN"
```
