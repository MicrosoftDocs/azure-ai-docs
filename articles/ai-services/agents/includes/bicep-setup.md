---
manager: nitinme
author: fosteramanda
ms.author: fosteramanda
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 11/13/2024
---

## Set up your Azure AI Foundry Agent Service project

The following section shows you how to set up the required resources for getting started with Azure AI Foundry Agent Service: 

1. Creating an [Azure AI project](../../../ai-foundry/quickstarts/get-started-playground.md) creates an endpoint for your app to call, and sets up app services to access to resources in your tenant.

1. Connecting an Azure OpenAI resource or an Azure AI Services resource


## Choose Basic or Standard Agent Setup
   
**Basic Setup**:  Agents use multitenant search and storage resources fully managed by Microsoft. You don't have visibility or control over these underlying Azure resources.

**Standard Setup**: Agents use customer-owned, single-tenant search and storage resources. With this setup, you have full control and visibility over these resources, but you incur costs based on your usage.

[!INCLUDE [ai-foundry-setup](portal-agent-limitation.md)]

<!--
| Description   | Resources  | Autodeploy |
| -----------------------------------------------| -----------------------|----------------------|
| Deploy a basic agent setup that uses Managed Identity authentication on the AI Services and storage account connections. | AI hub, AI project, AI Services | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fbasic-agent-identity%2Fazuredeploy.json) |
| Deploy a standard agent setup that uses Managed Identity authentication on the AI Services, storage account, and Azure AI Search connections. |AI hub, AI project, storage account, key vault, Azure AI Search, AI Services | [![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json)|


old url
https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Frefs%2Fheads%2Fmaster%2Fquickstarts%2Fmicrosoft.azure-ai-agent-service%2Fstandard-agent%2Fazuredeploy.json
-->

| Description and Autodeploy  |  Diagram (click to zoom in) |
| -----------------------------------------------| -----------------------|
| Deploy a basic agent setup that uses Managed Identity for authentication. Resources for the AI project, storage account, and AI Services are created for you. <br><br> The AI Services account is connected to your project, and a gpt-4o-mini model is deployed in the eastus region. A Microsoft-managed key vault is used by default. <br><br> [![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Fmain%2Fscenarios%2FAgents%2Fsetup%2Fbasic-agent-identity%2Fazuredeploy.json) |  :::image type="content" source="../media/quickstart/basic-agent-setup-resources.png" alt-text="An architecture diagram for basic agent setup." lightbox="../media/quickstart/basic-agent-setup-resources.png"::: | 
| Deploy a standard agent setup that uses Managed Identity for authentication. <br><br> Resources for the AI project, key vault, storage account, AI Services, and AI Search are created for you. <br><br>The AI Services, AI Search, key vault, and storage account are connected to your project. A gpt-4o-mini model is deployed in eastus region. <br><br> [![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure-Samples%2Fazureai-samples%2Fmain%2Fscenarios%2FAgents%2Fsetup%2Fstandard-agent-with-threadstorage%2Fazuredeploy.json) | :::image type="content" source="../media/quickstart/standard-agent-setup-resources.png" alt-text="An architecture diagram for standard agent setup." lightbox="../media/quickstart/standard-agent-setup-resources.png"::: |


### [Optional] Model selection in autodeploy template
You can customize the model used by your agent by editing the model parameters in the autodeploy template. To deploy a different model, you need to update at least the `modelName` and `modelVersion` parameters. 

By default, the deployment template is configured with the following values:

| Model Parameter  | Default Value  |
|------------------|----------------|
| modelName        | gpt-4o         |
| modelFormat      | OpenAI (for Azure OpenAI) |
| modelVersion     | 2024-11-20     |
| modelSkuName     | GlobalStandard |
| modelLocation    | eastus         |

> [!IMPORTANT]
> **Don't change the modelFormat parameter.** 
>
> The templates only support deployment of Azure OpenAI models. See which Azure OpenAI models are supported in the [Azure AI Foundry Agent Service model support](../concepts/model-region-support.md) documentation.


### [Optional] Use your own resources during agent setup

> [!NOTE]
> If you use an existing AI Services or Azure OpenAI resource, no model will be deployed. You can deploy a model to the resource after the agent setup is complete. 

Use an existing AI Services, Azure OpenAI, AI Search, and/or Azure Blob Storage resource by providing the full arm resource ID in the parameters file:

- `aiServiceAccountResourceId`
- `aiSearchServiceResourceId`
- `aiStorageAccountResourceId`


If you want to use an existing Azure OpenAI resource, you need to update the `aiServiceAccountResourceId` and the `aiServiceKind` parameters in the parameter file. The `aiServiceKind` parameter should be set to `AzureOpenAI`. 

For more information, see [how to use your own resources](../how-to/use-your-own-resources.md).

<!--
## Basic agent setup resource architecture
:::image type="content" source="../media/quickstart/basic-agent-setup-resources.png" alt-text="An architecture diagram for basic agent setup." lightbox="../media/quickstart/basic-agent-setup-resources.png":::

Resources for the AI hub, AI project, and AI Services are created for you. A storage account is created because it's a required resource for hubs, but this storage account isn't used by agents. The AI Services account is connected to your project/hub and a gpt-4o-mini model is deployed in the eastus region. A Microsoft-managed key vault, storage account, and search resource is used by default.

## Standard agent setup resource architecture
:::image type="content" source="../media/quickstart/standard-agent-setup-resources.png" alt-text="An architecture diagram for standard agent setup." lightbox="../media/quickstart/standard-agent-setup-resources.png":::

Resources for the AI hub, AI project, key vault, storage account, AI Services, and AI Search are created for you. The AI Services, AI Search, key vault, and storage account are connected to your project and hub. A gpt-4o-mini model is deployed in eastus region using the Azure OpenAI endpoint for your resource.
-->
