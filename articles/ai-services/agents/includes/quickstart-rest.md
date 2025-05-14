---
manager: salmanq
author: pranavp
ms.author: pranavp
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 02/15/2025
---
| [Reference documentation](../../openai/assistants-reference.md) |

## Prerequisites

[!INCLUDE [universal-prerequisites](universal-prerequisites.md)]



## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models in conjunction with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

To authenticate your API requests, use the [az login](/cli/azure/authenticate-azure-cli-interactively) command to sign into your Azure subscription.

```azurecli
az login
```

Next, you will need to fetch the Entra ID token to provide as authorization to the API calls. Fetch the token using the CLI command:
```azurecli
az account get-access-token --resource 'https://ai.azure.com' | jq -r .accessToken | tr -d '"'
```
Set the access token as an environment variable named `AZURE_AI_AGENTS_TOKEN`.

To successfully make REST API calls to Azure AI Foundry Agent Service, you will need to use the endpoint as below:

`https://<your_ai_service_name>.services.ai.azure.com/api/projects/<your_project_name>`

For example, your endpoint may look something like:

`https://exampleaiservice.services.ai.azure.com/api/projects/project`

Set this endpoint as an environment variable named `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`.

For `API_VERSION`, the GA API version is `2025-05-01` and the latest Preview API version is `2025-05-15-preview`. 

### Create an agent

> [!NOTE]
> With Azure AI Agents Service the `model` parameter requires model deployment name. If your model deployment name is different than the underlying model name then you would adjust your code to ` "model": "{your-custom-model-deployment-name}"`.

```console
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=2025-05-01 \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
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
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

### Add a user question to the thread

```console
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=2025-05-01 \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
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
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```console
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2025-05-01 \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

### Retrieve the agent response

```console
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=2025-05-01 \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```
