---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 09/12/2025
ms.custom: devx-track-ts
---


| [Reference documentation](/javascript/api/overview/azure/ai-projects-readme) | [Samples](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/README.md) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects) | [Package (npm)](https://www.npmjs.com/package/@azure/ai-projects) |

## Prerequisites

[!INCLUDE [universal-prerequisites](universal-prerequisites.md)]
* [Node.js LTS](https://nodejs.org/)

## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

Key objects in this code include: 

* [AgentsClient](/javascript/api/@azure/ai-agents/agentsclient)

First, initialize a new TypeScript project by running:

```console
npm init -y
npm pkg set type="module"
```

Run the following commands to install the npm packages required.

```console
npm install @azure/ai-agents @azure/identity
npm install @types/node typescript --save-dev
```

Next, to authenticate your API requests and run the program, use the [az login](/cli/azure/authenticate-azure-cli-interactively) command to sign into your Azure subscription.

```azurecli
az login
```

Use the following code to answer the math question `I need to solve the equation '3x + 11 = 14'. Can you help me?`. To run this code, you'll need to get the endpoint for your project. This string is in the format:

`https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>`

[!INCLUDE [endpoint-string-portal](endpoint-string-portal.md)]

Set this endpoint as an environment variable named `PROJECT_ENDPOINT` in a `.env` file.

[!INCLUDE [model-name-portal](model-name-portal.md)]

Save the name of your model deployment name as an environment variable named `MODEL_DEPLOYMENT_NAME`. 

> [!IMPORTANT] 
> * This quickstart code uses environment variables for sensitive configuration. Never commit your `.env` file to version control by making sure `.env` is listed in your `.gitignore` file.
> * _Remember: If you accidentally commit sensitive information, consider those credentials compromised and rotate them immediately._

Create a tsconfig.json file with the following content:

:::code language="json" source="~/azure-sdk-for-js-docs/samples/foundry/azure-ai-agents-quickstart-math/tsconfig.json":::

Next, create an `index.ts` file and paste in the following code:

:::code language="typescript" source="~/azure-sdk-for-js-docs/samples/foundry/azure-ai-agents-quickstart-math/index.ts":::

Run the code using `npx tsx -r dotenv/config index.ts`. This code answers the question `I need to solve the equation '3x + 11 = 14'. Can you help me?`. Full [sample source code](https://github.com/Azure-Samples/azure-sdk-for-js-docs/blob/main/samples/foundry/azure-ai-agents-quickstart-math) available.
