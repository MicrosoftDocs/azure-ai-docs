---
title: Use the conversation PII playground in Microsoft Foundry
FoundrytitleSuffix: Azure AI Language
description: Test conversation PII detection and redaction interactively in the Azure AI Foundry playground without writing code.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: quickstart
ms.date: 05/18/2026
ms.author: lajanuar
ms.custom: language-service-pii
---

<!-- markdownlint-disable MD025 -->
# Use the conversation PII playground in Microsoft Foundry

> [!NOTE]
> This content refers to the [new Foundry](https://ai.azure.com/) portal, which supports only [Foundry projects](../../../ai-foundry/what-is-foundry.md) and provides streamlined access to models, agents, and tools. To confirm that you're using new Foundry, make sure the version toggle in the portal banner is in the **on** position. :::image type="icon" source="media/quickstarts/azure-ai-foundry/new-foundry.png" border="false":::

The conversation PII playground in Azure AI Foundry lets you detect and redact personally identifiable information (PII) in conversational text interactively, without writing code. You can submit transcript-style input, configure redaction options, and review detected entities before integrating the feature into your application.

* [**Stable 2024-11-01: Generally Available (GA)**](/rest/api/language/analyze-conversations/operation-groups?view=rest-language-analyze-conversations-2024-11-01&preserve-view=true)
* [**Preview: 2025-11-15-preview**](/rest/api/language/analyze-conversations/operation-groups?view=rest-language-analyze-conversations-2025-11-15-preview&preserve-view=true)

> [!IMPORTANT]
> **Conversation PII API** (2025-11-15-preview) and **Conversation PII model** (2026-04-15-preview) are licensed to you as part part of your Azure subscrition and are subject to terms applicable  to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage) and the [Microsoft Products and Services Data Protection Addendum (DPA)](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA), as well as the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

## Prerequisites

> [!TIP]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Microsoft Foundry portal.
> * For more information, see [Connect services in the Microsoft Foundry portal](../../connect-services-foundry-portal.md).
> * Consider using a Foundry resource for the best experience. You can also follow these instructions with a Language resource.

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the **Foundry Account Owner** role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, see [Role based access control (RBAC)](../../../ai-foundry/openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* **Foundry resource**. Create a [Foundry resource](../../multi-service-resource.md) or see [Configure a Foundry resource](../concepts/configure-azure-resources.md). Alternatively, you can use a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* **A Foundry project**. For more information, see [Create a Foundry project](../../../ai-foundry/how-to/create-projects.md).

## Role-based access control (RBAC) requirements

Assign the correct roles to your user principal and project managed identity to access the conversation PII playground. Microsoft recommends using Microsoft Entra ID authentication, which enforces role-based restrictions. Key-based authentication grants full access without role checks and should be avoided in production environments.

> [!IMPORTANT]
> The Foundry RBAC roles were recently renamed. **Foundry User**, **Foundry Owner**, **Foundry Account Owner**, and **Foundry Project Manager** were previously named Azure AI User, Azure AI Owner, Azure AI Account Owner, and Azure AI Project Manager. You might still see the previous names in some places while the rename rolls out. The role IDs and core permissions are unchanged.

* Assign the minimum required roles to both your user principal and project managed identity so they can access Foundry features.

* Verify current assignments using [Check access for a user to a single Azure resource](/azure/role-based-access-control/check-access).


## Navigate to the playground

The active project appears in the upper-left corner. To create a new project:

1. Open the project drop-down menu.
1. Enter a project name or select an existing one.
1. Select **Create project**.

   :::image type="content" source="../media/new-foundry-homepage.png" alt-text="Screenshot of the new Foundry homepage.":::

There are two ways to access the conversation PII interface:

* Select the **Discover** tab from the upper-right navigation bar:
  1. In the search bar, enter **Azure** and press **Enter**.
  1. Select **Azure-Language-Conversational-PII redaction** from the results.
  1. Select **Open in Playground**.

* Select the **Build** tab from the upper-right navigation bar:
  1. From the left navigation bar, select **Models**.
  1. Select the **AI services** tab.
  1. Select **Azure-Language-Conversational-PII redaction** to go directly to the playground.

## Extract PII from conversations

The **extract PII from conversations** feature detects and masks personally identifying information in conversational text. This feature is designed to handle the unique structure and context of conversations, such as dialogues or chat logs.

1. On the **Playground** tab, select **Azure Language—Conversational PII redaction** from the drop-down menu.

1. Select a sample transcript, use the paperclip icon to upload your transcript, or enter conversation turn text.

1. Format your conversation with each turn on a new line and include speaker labels if possible. Inconsistent use of participant ID, colon, message, or new line may produce unexpected output. Here's an example of well-formatted conversation text:

    ```text
    Speaker 1: Hello, how are you?
    Speaker 2: I'm good, thank you! How about you?
    Speaker 1: I'm doing well, thanks for asking.
    ```

   > [!TIP]
   > You can use built-in formatting assistant (**Format for me**) in the playground to ensure your input meets expected conversation structure.

1. In the **Configure** pane, set the following options:

    | Option | Description |
    | --- | --- |
    | **API version** | Select the API version that you prefer to use. |
    | **Model version** | Select the model version that you prefer to use. |
    | **Language** | Select the language in which your source text is written. |
    | **Select types to include** | Select the PII types you want to redact. |
    | **Specify redaction character** | Choose the character used to mask sensitive text. |

1. Select **Detect**. Detected entities are highlighted in the text, and you can review the accompanying details in formatted text or as a JSON response.

    :::image type="content" source="media/quickstarts/azure-ai-foundry/new-foundry-conversation-detection.png" alt-text="Screenshot of PII conversation detection output in the Foundry playground." lightbox="media/quickstarts/azure-ai-foundry/new-foundry-conversation-detection.png":::

    | Field | Description |
    | --- | --- |
    | **Type** | The detected entity type. |
    | **Confidence** | The model's level of certainty that it correctly identified the entity type. |
    | **Offset** | The number of characters from the beginning of the text to the entity. |
    | **Length** | The character length of the entity. |

Verify that the detected entities match the PII in your input conversation. Select **Edit** to modify the **Configure** settings and rerun detection as needed.

## Open in Visual Studio Code 🆕

After validating your scenario in the playground, select **Open in VS Code** to carry your current configuration directly into a development environment—no manual setup required.

1. Configure your scenario in the playground:
   - Select your API version and model version.
   - Enter and test your sample input.
   - Adjust options such as entity types, redaction character, and language.
1. Select **Open in VS Code**.
1. Visual Studio Code opens with a preconfigured code sample that reflects your playground configuration, including your API version, model, and redaction settings.

> [!TIP]
> Use the playground to compare outputs across API versions—for example, preview versus GA—before exporting your configuration to code.

## Next steps

After opening in Visual Studio Code:

1. Add your authentication credentials.
1. Replace the sample input with your production data.
1. Run and validate the request.
1. Integrate the code into your application workflow.