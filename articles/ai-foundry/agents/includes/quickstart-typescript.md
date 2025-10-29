---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: include
ms.date: 09/12/2025
ms.custom: devx-track-ts
---


| [Reference documentation](/javascript/api/overview/azure/ai-projects-readme) | [Samples](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/README.md) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects) | [Package (npm)](https://www.npmjs.com/package/@azure/ai-projects) |

## Prerequisites

[!INCLUDE [universal-prerequisites](universal-prerequisites.md)]
* [Node.js LTS](https://nodejs.org/)

## Configure and run an agent

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

Run the code using `npx tsx -r dotenv/config index.ts`. This code answers the question `I need to solve the equation '3x + 11 = 14'. Can you help me?`. Responses aren't deterministic, your output will look similar to the below output:

```console
Created agent, agent ID : asst_X4yDNWrdWKb8LN0SQ6xlzhWk
Created thread, thread ID : thread_TxqZcHL2BqkNWl9dFzBYMIU6
Threads for agent asst_X4yDNWrdWKb8LN0SQ6xlzhWk:
...
Created message, message ID : msg_R0zDsXdc2UbfsNXvS1zeS6hk
Creating run...
Received response with status: queued
Received response with status: in_progress
Received response with status: completed
Run finished with status: completed


========================================================
=================== CONVERSATION RESULTS ===================
========================================================


❓ USER QUESTION: I need to solve the equation `3x + 11 = 14`. Can you help me?

🤖 ASSISTANT'S ANSWER:
--------------------------------------------------
Certainly! Let's solve the equation step by step:

We have:
3x + 11 = 14

### Step 1: Eliminate the constant (+11) on the left-hand side.
Subtract 11 from both sides:
3x + 11 - 11 = 14 - 11
This simplifies to:
3x = 3

We have:
3x + 11 = 14

### Step 1: Eliminate the constant (+11) on the left-hand side.
Subtract 11 from both sides:
3x + 11 - 11 = 14 - 11
This simplifies to:
3x = 3

### Step 2: Solve for x.
Divide both sides by 3:
3x / 3 = 3 / 3
This simplifies to:
x = 1

### Final Answer:
x = 1
--------------------------------------------------


========================================================
====================== END OF RESULTS ======================
========================================================
```


 Full [sample source code](https://github.com/Azure-Samples/azure-sdk-for-js-docs/blob/main/samples/foundry/azure-ai-agents-quickstart-math) available.