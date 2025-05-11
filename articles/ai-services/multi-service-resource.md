---
title: Create an AI Foundry resource
titleSuffix: Azure AI services
description: Create and manage an AI Foundry resource.
author: eric-urban
manager: nitinme
ms.service: azure-ai-services
ms.custom: devx-track-azurecli, devx-track-azurepowershell, build-2024, ignite-2024
ms.topic: quickstart
ms.date: 5/19/2025
ms.author: eur
zone_pivot_groups: programming-languages-portal-cli-ps
---

# Quickstart: Create an AI Foundry resource

Learn how to create and manage an AI Foundry resource. An AI Foundry resource allows you to access multiple Azure AI services with a single set of credentials. 

You can access Azure AI services through two different resource kinds: 

* Azure AI Foundry multi-service resource:
    * Access multiple Azure AI services with a single set of credentials.
    * Consolidates billing from the services you use.
* Single-service resource such as Face and Vision:
    * Access a single Azure AI service with a unique set of credentials for each service created. 
    * Most Azure AI services offer a free tier to try it out.

You access Azure AI services via Azure [resources](/azure/azure-resource-manager/management/manage-resources-portal) that you create in your Azure subscription. After you create an AI Foundry or other AI services resource, you can use the credentials generated to authenticate your applications.

## Usage in AI Foundry projects

You can use an AI Foundry resource with or without an AI Foundry project. For example:
- Create a project when you need to use the Azure AI Foundry Agent Service.
- Create a project when you need to fine-tune a model.
- You don't need a project when you want to use models as-is via REST API or SDKs.

> [!IMPORTANT]
> Unless otherwise noted, the instructions in this article are for creating an AI Foundry resource without any project association. For information about how to create a project, see [Create a project for Azure AI Foundry](../ai-foundry/how-to/create-projects.md).

Your AI Foundry resource might or might not be associated with an AI Foundry project.
- AI Foundry resources can be created in the Azure portal, Azure CLI, PowerShell, Bicep template, Terraform, or SDKs. In those cases, the AI Foundry resource by default isn't associated with a project. You can create a project later and associate it as a dependent of the AI Foundry resource.
- A [project can be created in the Azure AI Foundry portal](../ai-foundry/how-to/create-projects.md) and automatically associated as a dependent of a new AI Foundry resource. 
- An AI Foundry resource might have been created in the AI Foundry portal, but as a dependent resource of an [Azure AI Foundry hub](../ai-foundry/concepts/ai-resources.md). In this case, the resource is automatically associated with the project you create in the hub. 

For more information, see [Types of projects](../ai-foundry/what-is-azure-ai-foundry.md#project-types).

::: zone pivot="azportal"

[!INCLUDE [Azure portal quickstart](includes/quickstarts/management-azportal.md)]

::: zone-end

::: zone pivot="azcli"

[!INCLUDE [Azure CLI quickstart](includes/quickstarts/management-azcli.md)]

::: zone-end

::: zone pivot="azpowershell"

[!INCLUDE [Azure PowerShell quickstart](includes/quickstarts/management-azpowershell.md)]

::: zone-end

## Supported services with an AI Foundry resource

The AI Foundry resource enables access to the following Azure AI services with a single set of credentials. Some services are available via the AI Foundry resource and single-service resource.

> [!TIP]
> We recommend whenever possible to use the **AI Foundry** resource (where the API kind is `AIServices`) to access multiple Azure AI services with a single set of credentials. For services not available via the AI Foundry resource (such as Face and Custom Vision), you can create a single-service resource.

| Service | Description | Kind (via API) |
| --- | --- | --- |
| ![Azure AI Foundry icon](~/reusable-content/ce-skilling/azure/media/ai-services/ai-foundry.svg) [Azure AI Foundry Agent Service](./agents/index.yml) | Combine the power of generative AI models with tools that allow agents to access and interact with real-world data sources. | `AIServices` |
| ![Azure AI Foundry icon](~/reusable-content/ce-skilling/azure/media/ai-services/ai-foundry.svg) [Azure AI Model Inference](../ai-foundry/model-inference/index.yml) | Performs model inference for flagship models in the Azure AI Foundry model catalog. | `AIServices` |
| ![Azure OpenAI Service icon](~/reusable-content/ce-skilling/azure/media/ai-services/azure-openai.svg) [Azure OpenAI](./openai/index.yml) | Perform a wide variety of natural language tasks. | `AIServices`<br/>`OpenAI` |
| ![Content Safety icon](~/reusable-content/ce-skilling/azure/media/ai-services/content-safety.svg) [Content Safety](./content-safety/index.yml) | An AI service that detects unwanted contents. | `AIServices`<br/>`ContentSafety` |
| ![Custom Vision icon](~/reusable-content/ce-skilling/azure/media/ai-services/custom-vision.svg) [Custom Vision](./custom-vision-service/index.yml) | Customize image recognition for your business. | `CustomVision.Prediction` (Prediction only)<br/>`CustomVision.Training` (Training only) |
| ![Document Intelligence icon](~/reusable-content/ce-skilling/azure/media/ai-services/document-intelligence.svg) [Document Intelligence](./document-intelligence/index.yml) | Turn documents into intelligent data-driven solutions. | `AIServices`<br/>`FormRecognizer` |
| ![Face icon](~/reusable-content/ce-skilling/azure/media/ai-services/face.svg) [Face](./computer-vision/overview-identity.md) | Detect and identify people and emotions in images. | `Face` |
| ![Language icon](~/reusable-content/ce-skilling/azure/media/ai-services/language.svg) [Language](./language-service/index.yml) | Build apps with industry-leading natural language understanding capabilities. | `AIServices`<br/>`TextAnalytics` |
| ![Speech icon](~/reusable-content/ce-skilling/azure/media/ai-services/speech.svg) [Speech](./speech-service/index.yml) | Speech to text, text to speech, translation, and speaker recognition. | `AIServices`<br/>`Speech` |
| ![Translator icon](~/reusable-content/ce-skilling/azure/media/ai-services/translator.svg) [Translator](./translator/index.yml) | Use AI-powered translation technology to translate more than 100 in-use, at-risk, and endangered languages and dialects. | `AIServices`<br/>`TextTranslation` |
| ![Vision icon](~/reusable-content/ce-skilling/azure/media/ai-services/vision.svg) [Vision](./computer-vision/index.yml) | Analyze content in images and videos. | `AIServices` (Training and Prediction)<br/>`ComputerVision` |

## Azure AI services resource for Azure AI Search skills

Azure AI Search skills don't support the AI Foundry resource as described previously in this article. You must create a different kind of multi-service resource for Azure AI Search skills. 

The multi-service resource that you can use with Azure AI Search skills is listed under **AI Foundry** > **Classic AI services** > **Azure AI services multi-service account (classic)** in the portal. Look for the logo as shown here:

:::image type="content" source="./media/cognitive-services-resource-portal.png" alt-text="Screenshot of the Azure AI services multi-service account in the Azure portal." lightbox="./media/cognitive-services-resource-portal.png":::

To create a multi-service resource for Azure AI Search follow these instructions:
1. Select this link to create an **Azure AI services multi-service account (classic)** resource: [https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne](https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne)

1. On the **Create** page, provide the following information:

    |Project details| Description   |
    |--|--|
    | **Subscription** | Select one of your available Azure subscriptions. |
    | **Resource group** | The Azure resource group that will contain your Azure AI services multi-service account resource. You can create a new group or add it to a preexisting group. |
    | **Region** | The location of your Azure AI services multi-service account instance. Different locations may introduce latency, but have no impact on the runtime availability of your resource. |
    | **Name** | A descriptive name for your Azure AI services multi-service account resource. For example, *MyCognitiveServicesResource*. |
    | **Pricing tier** | The cost of your Azure AI services multi-service account depends on the options you choose and your usage. For more information, see the API [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/). |

1. Configure other settings for your resource as needed, read and accept the conditions (as applicable), and then select **Review + create**.

> [!TIP]
> If your subscription doesn't allow you to create an AI Foundry resource, you might need to enable the privilege of that [Azure resource provider](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) using the [Azure portal](/azure/azure-resource-manager/management/resource-providers-and-types#azure-portal), [PowerShell command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-powershell) or an [Azure CLI command](/azure/azure-resource-manager/management/resource-providers-and-types#azure-cli). If you are not the subscription owner, ask someone with the role of *Owner* or *Admin* to complete the registration for you or ask for the **/register/action** privileges to be granted to your account.

## Pricing

[!INCLUDE [SKUs and pricing](./includes/quickstarts/sku-pricing.md)]

## Related content

- Go to the [Azure AI services hub page](../ai-services/index.yml).
- Try AI services in the [Azure AI Foundry portal](../ai-services/connect-services-ai-foundry-portal.md).
