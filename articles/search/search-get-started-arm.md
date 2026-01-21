---
title: 'Quickstart: Deploy Using an ARM Template'
titleSuffix: Azure AI Search
description: Learn how to deploy an Azure AI Search service instance using an Azure Resource Manager template.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.custom:
  - subject-armqs
  - mode-arm
  - devx-track-arm-template
  - ignite-2023
ms.date: 03/04/2025
ms.update-cycle: 365-days
---

# Quickstart: Deploy Azure AI Search using an Azure Resource Manager template

In this quickstart, you use an Azure Resource Manager (ARM) template to deploy an Azure AI Search service in the Azure portal.

[!INCLUDE [About Azure Resource Manager](~/reusable-content/ce-skilling/azure/includes/resource-manager-quickstart-introduction.md)]

Only those properties included in the template are used in the deployment. If more customization is required, such as [setting up network security](search-security-overview.md#network-security), you can update the service as a post-deployment task. To customize an existing service with the fewest steps, use [Azure CLI](search-manage-azure-cli.md) or [Azure PowerShell](search-manage-powershell.md). If you're evaluating preview features, use the [Management REST API](search-manage-rest.md).

Assuming your environment meets the prerequisites and you're familiar with using ARM templates, select the **Deploy to Azure** button. The template will open in the Azure portal.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/template-deployments/deploy-to-azure-button.svg" alt-text="Button to deploy the Resource Manager template to Azure." border="false" link="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.search%2Fazure-search-create%2Fazuredeploy.json":::

## Prerequisites

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

## Review the template

The template used in this quickstart is from [Azure Quickstart Templates](https://azure.microsoft.com/resources/templates/azure-search-create/).

:::code language="json" source="~/quickstart-templates/quickstarts/microsoft.search/azure-search-create/azuredeploy.json":::

The Azure resource defined in this template:

- [Microsoft.Search/searchServices](/azure/templates/Microsoft.Search/searchServices): create an Azure AI Search service

## Deploy the template

Select the following image to sign in to Azure and open a template. The template creates an Azure AI Search resource.

:::image type="content" source="~/reusable-content/ce-skilling/azure/media/template-deployments/deploy-to-azure-button.svg" alt-text="Button to deploy the Resource Manager template to Azure." border="false" link="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fazure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.search%2Fazure-search-create%2Fazuredeploy.json":::

The Azure portal displays a form that allows you to easily provide parameter values. Some parameters are prefilled with the default values from the template. Provide your subscription, resource group, location, and service name. If you want to use Foundry Tools in an [AI enrichment](cognitive-search-concept-intro.md) pipeline, such as analyzing binary image files for text, choose a location that offers both Azure AI Search and Foundry Tools. Unless you use a keyless connection (preview), your Azure AI Search service and Microsoft Foundry resource must be in the same region for AI enrichment workloads. After you complete the form, agree to the terms and conditions, and then select the purchase button to complete your deployment.

> [!div class="mx-imgBorder"]
> ![Azure portal display of template](./media/search-get-started-arm/arm-portalscrnsht.png)

## Review deployed resources

When your deployment is complete, you can access your new resource group and new search service in the Azure portal.

## Clean up resources

Other Azure AI Search quickstarts and tutorials build upon this quickstart. If you plan to continue on to work with subsequent quickstarts and tutorials, you may wish to leave this resource in place. When no longer needed, you can delete the resource group, which deletes the Azure AI Search service and related resources.

## Related content

In this quickstart, you created an Azure AI Search service using an ARM template and then validated the deployment. To learn more about Azure AI Search and Azure Resource Manager, see the following articles:

- [What is Azure AI Search?](search-what-is-azure-search.md)
- [Quickstart: Full-text search in the Azure portal](search-get-started-portal.md)
- [Quickstart: Create a demo search app in the Azure portal](search-create-app-portal.md)
- [Quickstart: Create a skillset in the Azure portal](search-get-started-skillset.md)
