---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 06/02/2026
ms.author: lajanuar
ms.custom: doc-kit-assisted
---
<!-- markdownlint-disable MD041 -->
## Prerequisites

> [!TIP]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Microsoft Foundry portal.
> * For more information, see [Connect services in the Microsoft Foundry portal](../../../../connect-services-foundry-portal.md).
> * Consider using a Foundry resource for the best experience. You can also follow these instructions with a Language resource.

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the **Foundry Account Owner** role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, see [Role based access control (RBAC)](../../../../../ai-foundry/openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* **Foundry resource**. Create a [Foundry resource](../../../../multi-service-resource.md) or see [Configure a Foundry resource](../../../concepts/configure-azure-resources.md). Alternatively, you can use a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* **A Foundry project**. For more information, see [Create a Foundry project](../../../../../ai-foundry/how-to/create-projects.md).

## Role-based access control (RBAC) requirements

Assign the correct roles to your user principal and project managed identity to access PII playgrounds. Microsoft recommends using Microsoft Entra ID authentication, which enforces role-based restrictions. Key-based authentication grants full access without role checks and should be avoided in production environments.

> [!IMPORTANT]
> The Foundry RBAC roles were recently renamed. **Foundry User**, **Foundry Owner**, **Foundry Account Owner**, and **Foundry Project Manager** were previously named Azure AI User, Azure AI Owner, Azure AI Account Owner, and Azure AI Project Manager. You might still see the previous names in some places while the rename rolls out. The role IDs and core permissions are unchanged.

* Assign the minimum required roles to both your user principal and project managed identity so they can access Foundry features.

* Verify current assignments using [Check access for a user to a single Azure resource](/azure/role-based-access-control/check-access).

### [New Foundry](#tab/new-foundry)

> [!NOTE]
> This content refers to the [new Foundry](https://ai.azure.com/) portal, which supports only [Foundry projects](../../../../../ai-foundry/what-is-foundry.md) and provides streamlined access to models, agents, and tools. To confirm that you're using new Foundry, make sure the version toggle in the portal banner is in the **on** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/new-foundry.png" border="false":::

You can use [new Foundry playground](https://ai.azure.com/) to:

> [!div class="checklist"]
>
> * Detect and redact PII from text, conversations, or documents
> * Configure redaction policies, entity filters, and excluded values
> * Review detected entities and confidence scores

## Navigate to the new Foundry playground

The active project appears in the upper-left corner. To create a new project:

1. Open the project drop-down menu.
1. Enter a project name or select an existing one.
1. Select **Create project**.

   :::image type="content" source="../../../media/new-foundry-homepage.png" alt-text="Screenshot of the new Foundry homepage.":::

There are two ways to access the PII playground:

1. Select the **Discover** tab from the upper right navigation bar to go to the **Models** page.
   * In the search bar under models, enter **Azure** and press enter.
   * Select your PII capability model from the search results.
   * Select the **Open in Playground** button.

1. Select the **Build** tab from the upper right navigation bar.
   * From the left navigation bar, select **Models**.
   * Select the **AI services** tab.
   * Select your PII capability model to go to the playground.

## Detect PII in the new Foundry playground

Each PII capability uses a dedicated model. On the **Playground** tab, select your capability from the drop-down menu:

| Capability | Model name |
| --- | --- |
| Text PII redaction | **Azure Language—Text PII redaction** |
| Conversation PII redaction | **Azure Language—Conversational PII redaction** |
| Document PII redaction | **Azure Language—Document PII redaction** |

1. Select sample input, use the paperclip icon to upload a file, or enter your own input data.

1. In the **Configure** side panel, set your preferred options. Available options vary by capability:

    | Option | Description |
    | --- | --- |
    | **API version** | Select the API version that you prefer to use. |
    | **Model version** | Select the model version that you prefer to use. |
    | **Language** | Select the language of your input. |
    | **Select types to include** | Select the PII types you want to detect or redact. |
    | **Value to exclude** | Specify values you want to exclude from detection. |
    | **Synonyms** | Provide alternative names for specific entity types. |
    | **Policy type** | Choose the type of redaction policy to apply (character mask, entity mask, or no mask). |
    | **Specify redaction character** | Choose the character used to mask sensitive text. Available with the **CharacterMask** policy. |

1. Select **Detect**. Detected entities are highlighted in the input and you can review the accompanying details in formatted text or as a JSON response.

    | Field | Description |
    | --- | --- |
    | **Type** | The detected entity type. |
    | **Confidence** | The model's level of certainty regarding whether it correctly identified an entity type. |
    | **Offset** | The number of characters from the beginning of the input to the entity. |
    | **Length** | The character length of the entity. |

Verify that the detected entities match the PII in your input. You can use the **Edit** button to modify the **Configure** parameters and rerun detection as needed.

### [Foundry (classic)](#tab/foundry-classic)

> [!NOTE]
> This content refers to the [Foundry (classic)](https://ai.azure.com/) portal, which supports hub-based projects and other resource types. To confirm that you're using Foundry (classic), make sure the version toggle in the portal banner is in the **off** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/classic-foundry.png" border="false":::

You can use [Foundry (classic)](https://ai.azure.com/) to:

> [!div class="checklist"]
>
> * Detect and redact PII from conversations and text
> * Configure redaction policies
> * Review detected entities and confidence scores

## Navigate to the Foundry (classic) playground

1. In the left pane, select **Playgrounds**.
1. Select the **Try Azure Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="Screenshot showing the Playgrounds navigation and the Try Azure Language Playground button in Foundry (classic)." lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Detect PII in the Foundry (classic) playground

The **Language Playground** consists of four sections:

| Section | Purpose |
| --- | --- |
| **Top banner** | Select the input language and choose a PII detection capability. |
| **Left pane** | Set **Configuration** options such as API version, model version, and redaction policy. |
| **Center pane** | Enter text or conversation data for processing and review highlighted results. |
| **Right pane** | View **Details** for each detected entity. |

Select your PII capability from the top banner tiles. Each capability targets a different scenario.

In **Configuration** you can select from the following options:

| Option | Description |
| --- | --- |
| Select API version | Select which version of the API to use. |
| Select model version | Select which version of the model to use. |
| Select text language | Select the language of your input. |
| Select types to include | Select the types of information you want to redact. |
| Specify redaction policy | Select the method of redaction. |
| Specify redaction character | Select the character used for redaction. Only available with the **CharacterMask** redaction policy. |

After the operation completes, each detected entity is highlighted in the center pane with its type label displayed beneath it.

The **Details** section contains the following fields for each entity:

| Field | Description |
| --- | --- |
| Entity | The detected entity. |
| Category | The entity type that was detected. |
| Offset | The number of characters from the beginning of the line to the entity. |
| Length | The character length of the entity. |
| Confidence | The model's level of certainty that the entity type is correct. |
| Tags | The model's confidence scores for each identified entity subtype. |

Verify that each PII entity appears highlighted with the correct category label. If no entities appear, check that the input contains recognizable PII patterns and that the **Types** filter includes the expected categories.

---