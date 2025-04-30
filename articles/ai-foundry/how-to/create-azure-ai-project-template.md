---
title: "Quickstart: Create a project using Bicep"
description: Learn how to use a Bicep file (template) to create an Azure AI Foundry project in your Azure subscription.
author: Blackmist
ms.author: larryfr
manager: scottpolly
reviewer: andyaviles
ms.service: azure-ai-foundry
ms.topic: quickstart-bicep
ms.custom: "subject-bicepqs"
ms.date: 04/29/2025
# Customer intent: As a DevOps person, I need to automate or customize the creation of a hub by using templates.
---

# Quickstart: Create an Azure AI Foundry project using a Bicep file

> [!NOTE]
> The Bicep file used in this article is specific to a **[!INCLUDE [fdp](../includes/fdp-project-name.md)]**, and doesn't apply for a **[!INCLUDE [hub](../includes/hub-project-name.md)]**. For a template that creates a **[!INCLUDE [hub](../includes/hub-project-name.md)]**, see [Create an Azure AI Foundry hub using a template](create-azure-ai-hub-template.md).

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Use a [Microsoft Bicep](/azure/azure-resource-manager/bicep/overview) file (template) to create an [Azure AI Foundry](https://ai.azure.com) project. A template makes it easy to create resources as a single, coordinated operation. A Bicep file is a text document that defines the resources that are needed for a deployment. It might also specify deployment parameters. Parameters are used to provide input values when using the file to deploy resources.

## Prerequisites

- An Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/free/).

- A copy of the files from the GitHub repo. To clone the GitHub repo to your local machine, you can use [Git](https://git-scm.com/). Use the following command to clone the quickstart repository to your local machine and navigate to the `aifoundry-basics` directory.

    # [Azure CLI](#tab/cli)

    ```azurecli
    git clone https://github.com/Azure/azure-quickstart-templates
    cd azure-quickstart-templates/quickstarts/microsoft.machinelearningservices/aifoundry-basics
    ```

    # [Azure PowerShell](#tab/powershell)

    ```azurepowershell
    git clone https://github.com/Azure/azure-quickstart-templates
    cd azure-quickstart-templates\quickstarts\microsoft.machinelearningservices\aifoundry-basics
    ```

    ---

- The Bicep command-line tools. To install the Bicep command-line tools, use the [Install the Bicep CLI](/azure/azure-resource-manager/bicep/install) article.

## Review the Bicep file

The Bicep file used in this article can be found at [https://github.com/azure-ai-foundry/foundry-samples/tree/main/use-cases/infrastructure-as-code/00-basic](https://github.com/azure-ai-foundry/foundry-samples/tree/main/use-cases/infrastructure-as-code/00-basic).

:::code language="bicep" source="~/ai-foundry-samples/use-cases/infrastructure-as-code/00-basic/main.bicep":::

This template creates the following resources:

- [microsoft.cognitiveservices/accountsp](/azure/templates/microsoft.cognitiveservices/accounts?pivots=deployment-language-bicep)
- [microsoft.cognitiveservices/accounts/projects](/azure/templates/microsoft.cognitiveservices/accounts/projects?pivots=deployment-language-bicep)


## Deploy the Bicep file

1. Save the Bicep file as `main.bicep` to your local computer, or change to the `/use-cases/infrastructure-as-code/00-basic/main.bicep` directory if using a clone of the GitHub repo.

1. Deploy the Bicep file using either Azure CLI or Azure PowerShell.

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

    When the deployment finishes, you should seee a message indicating the deployment succeeded.

## Review deployed resources

Use the [Azure AI Foundry portal](https://ai.azure.com) to view the created resources. You can also use the Azure CLI or Azure PowerShell to list the resources.

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

If you plan to coninue working with subsequent quickstarts and tutorials, you can leave the resources created in this quickstart. If you want to remove the resources, use the followingg command.

# [Azure CLI](#tab/cli)

```azurecli
az group delete --name exampleRG
```

# [Azure PowerShell](#tab/powershell)

```azurepowershell
Remove-AzResourceGroup -Name exampleRG
```

## Related content

- [What is Azure AI Foundry?](../what-is-ai-foundry.md)
