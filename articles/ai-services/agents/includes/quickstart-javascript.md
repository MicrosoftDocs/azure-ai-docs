---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 03/28/2025
ms.custom: devx-track-js
---


| [Reference documentation](/javascript/api/overview/azure/ai-projects-readme) | [Samples](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/README.md) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects) | [Package (npm)](https://www.npmjs.com/package/@azure/ai-projects) |

## Prerequisites

* An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services).
* [Node.js LTS](https://nodejs.org/)
* Ensure that the individual deploying the template has the **Azure AI Developer** role assigned at the resource group level where the template is being deployed.
* Additionally, to deploy the template, you need to have the preset **Role Based Access Administrator** role at the subscription level.
   * The **Owner** role at the subscription level satisfies this requirement.
   * The specific admin role that is needed is `Microsoft.Authorization/roleAssignments/write`
* Ensure that each team member who wants to use the Agent Playground or Agent SDK to create or edit agents has been assigned the built-in **Azure AI Developer** [RBAC role](../../../ai-foundry/concepts/rbac-azure-ai-foundry.md) for the project.
    * Note: assign these roles after the template has been deployed
    * The minimum set of permissions required is: **agents/*/read**, **agents/*/action**, **agents/*/delete**  
* Install [the Azure CLI and the machine learning extension](/azure/machine-learning/how-to-configure-cli). If you have the CLI already installed, make sure it's updated to the latest version.



## Configure and run an agent

| Component | Description                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Agent     | Custom AI that uses AI models in conjunction with tools.                                                                                                                                                                                  |
| Tool      | Tools help extend an agent’s ability to reliably and accurately respond during conversation. Such as connecting to user-defined knowledge bases to ground the model, or enabling web search to provide current information.               |
| Thread    | A conversation session between an agent and a user. Threads store Messages and automatically handle truncation to fit content into a model’s context.                                                                                     |
| Message   | A message created by an agent or a user. Messages can include text, images, and other files. Messages are stored as a list on the Thread.                                                                                                 |
| Run       | Activation of an agent to begin running based on the contents of Thread. The agent uses its configuration and Thread’s Messages to perform tasks by calling models and tools. As part of a Run, the agent appends Messages to the Thread. |
| Run Step  | A detailed list of steps the agent took as part of a Run. An agent can call tools or create Messages during its run. Examining Run Steps allows you to understand how the agent is getting to its results.                                |

Key objects in this code include: 

* [AIProjectsClient](/javascript/api/@azure/ai-projects/aiprojectsclient)
* [ToolUtility](/javascript/api/@azure/ai-projects/toolutility)
* [Agent operations](/javascript/api/@azure/ai-projects/agentsoperations)

First, initialize a new project by running:

```console
npm init -y
```

Run the following commands to install the npm packages required.

```console
npm install @azure/ai-projects
npm install @azure/identity
npm install dotenv
```

Next, to authenticate your API requests and run the program, use the [az login](/cli/azure/authenticate-azure-cli-interactively) command to sign into your Azure subscription.

```azurecli
az login
```

Use the following code to create and run an agent. To run this code, you will need to create a connection string using information from your project. This string is in the format:

`<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>`

[!INCLUDE [connection-string-portal](endpoint-string-portal.md)]

`HostName` can be found by navigating to your `discovery_url` and removing the leading `https://` and trailing `/discovery`. To find your `discovery_url`, run this CLI command:

```azurecli
az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
```

For example, your connection string may look something like:

`eastus.api.azureml.ms;12345678-abcd-1234-9fc6-62780b3d3e05;my-resource-group;my-project-name`

Set this connection string as an environment variable named `PROJECT_CONNECTION_STRING` in a `.env` file.

> [!IMPORTANT] 
> * This quickstart code uses environment variables for sensitive configuration. Never commit your `.env` file to version control by making sure `.env` is listed in your `.gitignore` file.
> * _Remember: If you accidentally commit sensitive information, consider those credentials compromised and rotate them immediately._


Next, create an `index.js` file and paste in the code below:

:::code language="JavaScript" source="~/azure-typescript-e2e-apps/quickstarts/ai-agents/js/src/index.js":::


Run the code using `node index.js` and observe.