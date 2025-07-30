---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 07/29/2025
ms.author: lajanuar
---

> [!NOTE]
>
> * If you already have an Azure AI Language or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Azure AI Foundry portal. 
> * For more information, see [How to use Azure AI services in the Azure AI Foundry portal](/azure/ai-services/connect-services-ai-foundry-portal.md).
> * We highly recommend that you use an Azure AI Foundry resource in the AI Foundry; however, you can also follow these instructions using a Language resource.

## Prerequisites

* An Azure subscription. If you don't have one, you can [create one for free](https://azure.microsoft.com/free/cognitive-services).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](/azure/openai/how-to/role-based-access-control.md#cognitive-services-contributor).
*  An [Azure AI Foundry multi-service resource](/azure/ai-services/multi-service-resource.md). For more information, *see* [Configure an Azure AI Foundry resource](../../how-to/configure-azure-resources.md).md#option-1-configure-an-azure-ai-foundry-resource). Alternately, you can use an [Azure AI Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* A Foundry project created in the Azure AI Foundry. For more information, *see* [Create an AI Foundry project](/azure/ai-foundry/how-to/create-projects.md).

## Azure Foundry language playground

Azure AI Foundry offers a unified platform for building, managing, and deploying AI solutions with a wide array of models and tools. Azure AI Foundry playgrounds are interactive environments within the Azure AI Foundry portal designed for exploring, testing, and prototyping with various AI models and tools.

1. Navigate to the [Azure AI Foundry](https://ai.azure.com/).
1. If you aren't already signed in, the portal prompts you to do so with your Azure credentials.
1. Once signed in, you can create or access your existing projects within Azure AI Foundry.
1. If you're not already at your project for this task, select it.
1. On the left side navigation pane, select **Playgrounds**, navigate to the **Language playground card**, and then choose the **Try the Language playground** button.

  :::image type="content" source="../../media/quickstarts/playground.png" alt-text="Screenshot of the playgrounds selection in Azure AI Foundry.":::

## Import project
For this quickstart, you can download this sample project file and import it. This project can predict the intended commands from user input, such as: reading emails, deleting emails, and attaching a document to an email.

## Try CLU in the Foundry playground

The top section of the Language playground is where you can view and select the available Language services. For CLU you can select **Fine-tune models**. For more information, *see* [Create a fine-tuning task project ](../../how-to/create-project.md).



## Clean up resources



