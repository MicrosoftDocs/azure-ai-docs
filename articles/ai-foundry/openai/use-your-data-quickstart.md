---
title: "Use your own data with Azure OpenAI in Microsoft Foundry Models"
titleSuffix: Azure OpenAI
description: Use this article to import and use your data in Azure OpenAI.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 09/22/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: quickstart
ms.custom:
  - devx-track-dotnet
  - devx-track-extended-java
  - devx-track-js
  - devx-track-ts
  - devx-track-go
  - devx-track-python
  - build-2025
zone_pivot_groups: openai-use-your-data
---

# Quickstart: Chat with Azure OpenAI models using your own data

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

In this quickstart, you use your own data with Azure OpenAI models to create a powerful, conversational AI platform that enables faster and more accurate communication.

> [!IMPORTANT]
> There are new ways to build conversational solutions with your own data. For the latest recommended approach, see [Quickstart: Agentic retrieval](../../search/search-get-started-agentic-retrieval.md).

::: zone pivot="ai-foundry-portal"

## Prerequisites

- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.

[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [Studio quickstart](includes/use-your-data-studio.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.
- The [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)

[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [Csharp quickstart](includes/use-your-data-dotnet.md)]

::: zone-end

::: zone pivot="programming-language-spring"

[Source code](https://github.com/spring-projects-experimental/spring-ai)| [Source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai) | [Sample](https://github.com/rd-1-2022/ai-azure-retrieval-augmented-generation)

## Prerequisites

- [Azure OpenAI](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI)
- [Azure Blob Storage](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM)
- [Azure AI Search](https://portal.azure.com/#create/Microsoft.Search)
- An [Azure OpenAI](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI) or  deployed in a [supported region and with a supported model](./concepts/use-your-data.md#regional-availability-and-model-support).
    - Be sure that you're assigned at least the [Cognitive Services Contributor](./how-to/role-based-access-control.md#cognitive-services-contributor) role for the Azure OpenAI resource.
- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.
    
[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [Spring quickstart](includes/use-your-data-spring.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[Reference documentation](https://platform.openai.com/docs/api-reference/chat) | [Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource deployed in a [supported region and with a supported model](./concepts/use-your-data.md#regional-availability-and-model-support).

- Be sure that you're assigned at least the [Cognitive Services Contributor](./how-to/role-based-access-control.md#cognitive-services-contributor) role for the Azure OpenAI resource.

- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [JavaScript quickstart](includes/use-your-data-javascript.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[Reference documentation](https://platform.openai.com/docs/api-reference/chat) | [Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [TypeScript](https://www.typescriptlang.org/download/)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource deployed in a [supported region and with a supported model](./concepts/use-your-data.md#regional-availability-and-model-support).

- Be sure that you're assigned at least the [Cognitive Services Contributor](./how-to/role-based-access-control.md#cognitive-services-contributor) role for the Azure OpenAI resource.

- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [TypeScript quickstart](includes/use-your-data-typescript.md)]

::: zone-end

::: zone pivot="programming-language-python"

## Prerequisites

- [Azure OpenAI](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI)
- [Azure Blob Storage](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM)
- [Azure AI Search](https://portal.azure.com/#create/Microsoft.Search)
- An [Azure OpenAI resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI) deployed in a [supported region and with a supported model](./concepts/use-your-data.md#regional-availability-and-model-support).
    - Be sure that you're assigned at least the [Cognitive Services Contributor](./how-to/role-based-access-control.md#cognitive-services-contributor) role for the Azure OpenAI resource.
- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.

[Reference](https://platform.openai.com/docs/api-reference?lang=python) | [Source code](https://github.com/openai/openai-python) | [Package (pypi)](https://pypi.org/project/openai/) | [Samples](https://github.com/openai/openai-cookbook/)

These links reference the OpenAI API for Python. There's no Azure-specific OpenAI Python SDK. [Learn how to switch between the OpenAI services and Azure OpenAI](/azure/ai-foundry/openai/how-to/switching-endpoints).

[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [Python quickstart](includes/use-your-data-python.md)]

::: zone-end

::: zone pivot="programming-language-powershell"


## Prerequisites

- [Azure OpenAI](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI)
- [Azure Blob Storage](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM)
- [Azure AI Search](https://portal.azure.com/#create/Microsoft.Search)
- An [Azure OpenAI resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI) deployed in a [supported region and with a supported model](./concepts/use-your-data.md#regional-availability-and-model-support).
    - Be sure that you're assigned at least the [Cognitive Services Contributor](./how-to/role-based-access-control.md#cognitive-services-contributor) role for the Azure OpenAI resource.
- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.

[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [PowerShell quickstart](includes/use-your-data-powershell.md)]

::: zone-end

::: zone pivot="programming-language-go"


## Prerequisites

- [Azure OpenAI](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI)
- [Azure Blob Storage](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM)
- [Azure AI Search](https://portal.azure.com/#create/Microsoft.Search)
- An [Azure OpenAI resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI) deployed in a [supported region and with a supported model](./concepts/use-your-data.md#regional-availability-and-model-support).
    - Be sure that you're assigned at least the [Cognitive Services Contributor](./how-to/role-based-access-control.md#cognitive-services-contributor) role for the Azure OpenAI resource.
- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.

[Reference](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go) | [Source code](https://github.com/Azure/azure-sdk-for-go) | [Package (Go)](https://pkg.go.dev/github.com/azure/azure-dev) | [Samples](https://github.com/azure-samples/azure-sdk-for-go-samples)

[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [Go quickstart](includes/use-your-data-go.md)]

::: zone-end

::: zone pivot="rest-api"


## Prerequisites

- [Azure OpenAI](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI)
- [Azure Blob Storage](https://portal.azure.com/#create/Microsoft.StorageAccount-ARM)
- [Azure AI Search](https://portal.azure.com/#create/Microsoft.Search)
- An [Azure OpenAI resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI) deployed in a [supported region and with a supported model](./concepts/use-your-data.md#regional-availability-and-model-support).
    - Be sure that you're assigned at least the [Cognitive Services Contributor](./how-to/role-based-access-control.md#cognitive-services-contributor) role for the Azure OpenAI resource.
- Download the example data from [GitHub](https://github.com/Azure-Samples/cognitive-services-sample-data-files/blob/master/openai/contoso_benefits_document_example.pdf) if you don't have your own data.

[!INCLUDE [Connect your data to OpenAI](includes/connect-your-data-studio.md)]

[!INCLUDE [REST API quickstart](includes/use-your-data-rest.md)]

::: zone-end

## Clean up resources

If you want to clean up and remove an Azure OpenAI or Azure AI Search resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure AI Search resources](/azure/search/search-get-started-portal#clean-up-resources)
- [Azure app service resources](/azure/app-service/quickstart-dotnetcore?pivots=development-environment-vs#clean-up-resources)

## Next steps

- Learn more about [using your data in Azure OpenAI in Microsoft Foundry Models](./concepts/use-your-data.md)
- [Chat app sample code on GitHub](https://go.microsoft.com/fwlink/?linkid=2244395).
