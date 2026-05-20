---
title: Use the document PII playground in Azure AI Foundry
titleSuffix: Azure AI Language
description: Test document-based PII detection and redaction interactively in the Azure AI Foundry playground without writing code.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 05/18/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# Use the document PII playground in Azure AI Foundry

> [!NOTE]
> This content refers to the [new Foundry](https://ai.azure.com/) portal, which supports only [Foundry projects](../../../ai-foundry/what-is-foundry.md) and provides streamlined access to models, agents, and tools. To confirm that you're using new Foundry, make sure the version toggle in the portal banner is in the **on** position. :::image type="icon" source="media/quickstarts/azure-ai-foundry/new-foundry.png" border="false":::

The document PII playground in Azure AI Foundry lets you detect and redact personally identifiable information (PII) in native documents interactively, without writing code. You can upload document files, configure redaction options, and review redacted output before integrating the feature into your application.

> [!IMPORTANT]
> Document-based PII is currently in preview and may change before general availability (GA).

## Prerequisites

> [!TIP]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Microsoft Foundry portal.
> * For more information, see [Connect services in the Microsoft Foundry portal](../../connect-services-foundry-portal.md).
> * Consider using a Foundry resource for the best experience. You can also follow these instructions with a Language resource.

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, see [Role based access control (RBAC)](../../../ai-foundry/openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* **Foundry resource**. Create a [Foundry resource](../../multi-service-resource.md) or see [Configure a Foundry resource](../concepts/configure-azure-resources.md). Alternatively, you can use a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* **A Foundry project**. For more information, see [Create a Foundry project](../../../ai-foundry/how-to/create-projects.md).

## Navigate to the playground

The active project appears in the upper-left corner. To create a new project:

1. Open the project drop-down menu.
1. Enter a project name or select an existing one.
1. Select **Create project**.

   :::image type="content" source="../media/new-foundry-homepage.png" alt-text="Screenshot of the new Foundry homepage.":::

There are two ways to access the document PII interface:

* Select the **Discover** tab from the upper-right navigation bar:
  1. In the search bar, enter **Azure** and press **Enter**.
  1. Select **Azure-Language-Document-PII redaction** from the results.
  1. Select **Open in Playground**.

* Select the **Build** tab from the upper-right navigation bar:
  1. From the left navigation bar, select **Models**.
  1. Select the **AI services** tab.
  1. Select **Azure-Language-Document-PII redaction** to go directly to the playground.

## Redact PII from documents

The **Azure-Language-Document-PII redaction** model identifies and redacts personally identifiable information in native document files, including `.pdf`, `.docx`, and `.txt` files. The playground preserves document layout and formatting in the redacted output.

1. On the **Playground** tab, select **Azure Language—Document PII redaction** from the drop-down menu.

1. Use the paperclip icon to upload a `.pdf`, `.docx`, or `.txt` document.

1. In the **Configure** pane, set the following options:

    | Option | Description |
    | --- | --- |
    | **API version** | Select the API version that you prefer to use. |
    | **Model version** | Select the model version that you prefer to use. |
    | **Language** | Select the language in which your document is written. |
    | **Select types to include** | Select the PII types you want to redact. |
    | **Policy type** | Choose the type of redaction policy to apply (character mask, entity mask, or no mask). |

1. Select **Detect**. After processing completes, the redacted document is displayed and you can review the detected entities in the **Details** pane.

    | Field | Description |
    | --- | --- |
    | **Type** | The detected entity type. |
    | **Confidence** | The model's level of certainty regarding whether it correctly identified an entity type. |
    | **Offset** | The position of the entity within the document. |
    | **Length** | The character length of the entity. |

Verify that the detected entities match the PII in your input document. Use the **Edit** button to modify **Configure** parameters and resubmit the document as needed.