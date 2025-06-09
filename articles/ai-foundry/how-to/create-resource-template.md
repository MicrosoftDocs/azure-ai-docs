---
title: "Quickstart: Create an AI Foundry resource using Bicep"
titleSuffix: Azure AI Foundry
description: Learn how to use a Bicep file (template) to create an Azure AI Foundry resource in your Azure subscription.
author: deeikele
ms.author: larryfr
manager: scottpolly
reviewer: deeikele
ms.date: 05/18/2025
ms.service: azure-ai-foundry
ms.topic: quickstart-bicep
ms.custom:
  - "subject-bicepqs"
  - "build-aifnd"
  - "build-2025"
# Customer intent: As a DevOps person, I need to automate or customize the creation of an AI Foundry resource by using templates.
---

# Quickstart: Create an Azure AI Foundry resource using a Bicep file

> [!NOTE]
> The Bicep file used in this article is specific to a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**, and doesn't apply for a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. For a template that creates a **[!INCLUDE [hub](../includes/hub-project-name.md)]**, see [Create an Azure AI Foundry hub using a template](create-azure-ai-hub-template.md).

Use a [Microsoft Bicep](/azure/azure-resource-manager/bicep/overview) file (template) to create an [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) resource. A template makes it easy to create resources as a single, coordinated operation. A Bicep file is a text document that defines the resources that are needed for a deployment. It might also specify deployment parameters. Parameters are used to provide input values when using the file to deploy resources.

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).

- A copy of the files from the GitHub repo. To clone the GitHub repo to your local machine, you can use [Git](https://git-scm.com/). Use the following command to clone the quickstart repository to your local machine and navigate to the `aifoundry-basics` directory.

    # [Azure CLI](#tab/cli)

    ```azurecli
    git clone https://github.com/Azure-AI-Foundry/foundry-samples
    cd foundry-samples/samples/microsoft/infrastructure-setup/00-basic
    ```

    # [Azure PowerShell](#tab/powershell)

    ```azurepowershell
    git clone https://github.com/Azure-AI-Foundry/foundry-samples
    cd foundry-samples/samples/microsoft/infrastructure-setup/00-basic
    ```

    ---

- The Bicep command-line tools. To install the Bicep command-line tools, use the [Install the Bicep CLI](/azure/azure-resource-manager/bicep/install) article.

## Review the Bicep file

The Bicep file used in this article can be found at [https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/00-basic](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup/00-basic).

This template creates the following resources:

- [microsoft.cognitiveservices/accounts](/azure/templates/microsoft.cognitiveservices/accounts?pivots=deployment-language-bicep)
- [microsoft.cognitiveservices/accounts/projects](/azure/templates/microsoft.cognitiveservices/accounts/projects?pivots=deployment-language-bicep)


## Deploy the Bicep file

Deploy the Bicep file using either the Azure CLI or Azure PowerShell.

# [Azure CLI](#tab/cli)

```azurecli
az group create --name exampleRG --location eastus
az deployment group create --resource-group exampleRG --template-file main.bicep --parameters aiServicesName=myai aiProjectName=myai-proj 
```

# [Azure PowerShell](#tab/powershell)

```azurepowershell
New-AzResourceGroup -Name exampleRG -Location eastus
New-AzResourceGroupDeployment -ResourceGroupName exampleRG -TemplateFile main.bicep -aiHubName myai -aiProjectName myai-proj
```

---

> [!NOTE]
> Replace `myai` with the name of your resource.

When the deployment finishes, you should see a message indicating the deployment succeeded.

## Review deployed resources

Use the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) to view the created resources. You can also use the Azure CLI or Azure PowerShell to list the resources.

# [Azure CLI](#tab/cli)

```azurecli
az resource list --name exampleRG
```

# [Azure PowerShell](#tab/powershell)

```azurepowershell
Get-AzResource -ResourceGroupName exampleRG
```

---

## Clean up resources

If you plan to continue working with subsequent quickstarts and tutorials, you can leave the resources created in this quickstart. If you want to remove the resources, use the following command.

# [Azure CLI](#tab/cli)

```azurecli
az group delete --name exampleRG
```

# [Azure PowerShell](#tab/powershell)

```azurepowershell
Remove-AzResourceGroup -Name exampleRG
```

---

## Security configurations samples

See the [Azure AI Foundry Samples](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/infrastructure-setup) repository with example Bicep template configurations for the most common enterprise security configurations. Template examples include [network isolation](configure-private-link.md), [customer-managed key encryption](../concepts/encryption-keys-portal.md), [advanced identity options](../concepts/rbac-azure-ai-foundry.md) and [Agents standard setup](../../ai-services/agents/how-to/use-your-own-resources.md) with your resources for storing data.

## Related content

- [Get started with the SDK](../quickstarts//get-started-code.md?pivots=fdp-project)
