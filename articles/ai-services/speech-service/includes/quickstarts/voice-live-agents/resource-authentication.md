---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 11/06/2025
ai-usage: ai-assisted
---

> [!NOTE]
> The agent integration requires Entra ID authentication. Key-based authentication isn't supported in Agent mode.

Create a new file named `.env` in the folder where you want to run the code. 

In the `.env` file, add the following environment variables for authentication:

```plaintext
# Settings for Foundry Agent
PROJECT_ENDPOINT=<endpoint copied from welcome screen>
AGENT_NAME="MyVoiceAgent"
MODEL_DEPLOYMENT_NAME="gpt-4.1-mini"
# Settings for Voice Live
AGENT_NAME=<name-used-to-create-agent> # See above
AGENT_VERSION=<version-of-the-agent>
CONVERSATION_ID=<specific conversation id to reconnect to>
PROJECT_NAME=<your_project_name>
VOICELIVE_ENDPOINT=<your_endpoint>
VOICELIVE_API_VERSION=2026-01-01-preview
```

Replace the default values with your actual project name, agent name, and endpoint values.

| Variable name | Value |
| ------------- | ----- |
| `PROJECT_ENDPOINT` | The Foundry project endpoint copied from the project welcome screen. |
| `AGENT_NAME` | The name of the agent to use. |
| `AGENT_VERSION` | Optional: The version of the agent to use. |
| `CONVERSATION_ID` | Optional: A specific conversation ID to reconnect to. |
| `PROJECT_NAME` | The name of your Microsoft Foundry project. Project name is the last element of the project endpoint value. |
| `VOICELIVE_ENDPOINT` | This value can be found in the **Keys and Endpoint** section when examining your resource from the Azure portal. |
| `FOUNDRY_RESOURCE_OVERRIDE` | Optional: The Foundry resource name hosting the agent project (for example, `my-resource-name`). |
| `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID` | Optional: The managed identity client ID of the Voice Live resource. |

Learn more about [keyless authentication](/azure/ai-services/authentication) and [setting environment variables](/azure/ai-services/cognitive-services-environment-variables).
