---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 02/06/2026
ms.author: lajanuar
ms.custom: language-service-pii
ai-usage: ai-assisted
---
## Prerequisites

> [!TIP]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Microsoft Foundry portal. 
> * For more information, see [Connect services in the Microsoft Foundry portal](../../../../connect-services-foundry-portal.md).
> * Consider using a Foundry resource for the best experience. You can also follow these instructions with a Language resource.

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, see [Role based access control (RBAC)](../../../../../ai-foundry/openai/how-to/role-based-access-control.md#cognitive-services-contributor).
* **Foundry resource**. Create a [Foundry resource](../../../../multi-service-resource.md) or see [Configure a Foundry resource](../../../concepts/configure-azure-resources.md). Alternatively, you can use a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* **A Foundry project**. For more information, see [Create a Foundry project](../../../../../ai-foundry/how-to/create-projects.md).


### [Foundry (classic)](#tab/foundry-classic)

> [!NOTE]
> This content refers to the [Foundry (classic)](https://ai.azure.com/) portal, which supports hub-based projects and other resource types. To confirm that you're using Foundry (classic), make sure the version toggle in the portal banner is in the **off** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/classic-foundry.png" border="false":::


You can use [Foundry (classic)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Extract PII from conversations
> * Extract PII from text
> * Configure redaction policies
> * Review detected entities and confidence scores


## Navigate to the Foundry (classic) playground

1. In the left pane, select **Playgrounds**.
1. Select the **Try Azure Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="Screenshot showing the Playgrounds navigation and the Try Azure Language Playground button in Foundry (classic)." lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Detect PII in the Foundry playground

The **Language Playground** consists of four sections:

| Section | Purpose |
| --- | --- |
| **Top banner** | Select the input language and choose a PII detection capability. |
| **Left pane** | Set **Configuration** options such as API version, model version, and redaction policy. |
| **Center pane** | Enter text for processing and review highlighted results. |
| **Right pane** | View **Details** for each detected entity. |

Select either **Extract PII from conversation** or **Extract PII from text** from the top banner tiles. Each capability targets a different scenario.

### Extract PII from conversation

**Extract PII from conversation** is designed to identify and mask personally identifying information in conversational text.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select text language| Select the language of your input text.|
|Select types to include| Select the types of information you want to redact.|
|Specify redaction policy| Select the method of redaction.|
|Specify redaction character| Select the character used for redaction. Only available with the **CharacterMask** redaction policy.|

After the operation completes, each detected entity is highlighted in the center pane with its type label displayed beneath it.

The **Details** section contains the following fields for each entity:

|Field | Description                |
|------|----------------------------|
|Entity|The detected entity.|
|Category| The entity type that was detected.|
|Offset| The number of characters from the beginning of the line to the entity.|
|Length| The character length of the entity.|
|Confidence| The model's level of certainty that the entity type is correct.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/conversation-pii.png" alt-text="A screenshot showing detected PII entities highlighted in a conversation with entity details displayed in the right pane of the Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/conversation-pii.png":::

Verify that each PII entity appears highlighted with the correct category label. If no entities appear, check that the input text contains recognizable PII patterns and that the **Types** filter includes the expected categories.

### Extract PII from text

**Extract PII from text** is designed to identify and mask personally identifying information in text.

In **Configuration** you can select from the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select text language| Select the language of your input text.|
|Select types to include| Select the types of information you want to redact.|
|Specify redaction policy| Select the method of redaction.|
|Specify redaction character| Select the character used for redaction. Only available with the **CharacterMask** redaction policy.|

After the operation completes, each detected entity is highlighted in the center pane with its type label displayed beneath it.

The **Details** section contains the following fields for each entity:

|Field | Description                |
|------|----------------------------|
|Entity|The detected entity.|
|Category| The entity type that was detected.|
|Offset| The number of characters from the beginning of the line to the entity.|
|Length| The character length of the entity.|
|Confidence| The model's level of certainty that the entity type is correct.|
|Tags| The model's confidence scores for each identified entity subtype.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/text-pii.png" alt-text="A screenshot showing detected PII entities highlighted in text with entity details and confidence scores displayed in the right pane of the Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/text-pii.png":::

Verify that each PII entity appears highlighted with the correct category label. The **Tags** column shows subcategory confidence scores when applicable.

### [Foundry (new)](#tab/foundry-new)

> [!NOTE]
> This content refers to the [Foundry (new)](https://ai.azure.com/) portal, which supports only [Foundry projects](../../../../../ai-foundry/what-is-foundry.md) and provides streamlined access to models, agents, and tools. To confirm that you're using Foundry (new), make sure the version toggle in the portal banner is in the **on** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/new-foundry.png" border="false":::


You can use [Foundry (new)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Extract PII from text
> * Configure redaction policies and excluded values
> * Review detected entities and confidence scores


## Navigate to the Foundry (new) playground

The active project appears in the upper-left corner. To create a new project:

1. Open the project drop-down menu.
1. Enter a project name or select an existing one.
1. Select **Create project**.

   :::image type="content" source="../../../media/new-foundry-homepage.png" alt-text="Screenshot of the Foundry (new) homepage":::


There are two ways to access the PII interface:

1. Select the **Discover** tab from the upper right navigation bar to go to the **Models** page.
   * In the search bar under models, enter **Azure** and press enter.
   * Next, select **Azure-Language-Text-PII redaction** from the search results.
   * Finally, select the **Open in Playground** button.

1. Select the  **Build** tab from the upper right navigation bar.
   * From the left navigation bar, select  **Models**.
   * Select the **AI services** tab.
   * Next, select **Azure-Language-Text-PII redaction** to go to the playground.


## Detect PII in the Foundry playground

The **extract PII from text** feature detects and masks personally identifying information within written content.

1. On the **Playground** tab, select the sample text, use the paperclip icon to upload your text, or enter your own text.

1. Select the **Configure** button. In the **Configure** side panel, set the following options:

| Option | Description |
|--|--|
| **API version** | Select the API version that you prefer to use. |
| **Model version** | Select the model version that you prefer to use. |
| **Language** | Select the language in which your source text is written. |
| **Types** | Select the types of information you want to redact. |
| **Specify redaction policy** | Select the method of redaction. |
| **Excluded values** | Select the values that you want to exclude. |
| **Synonyms** | Select a category for your redaction type values to target related synonyms. |

After you make your selections, choose the **Detect** button. Detected entities are highlighted in the text and you can review the accompanying details in formatted text or as a JSON response:

> [!NOTE]
> The Foundry (new) playground currently supports **text PII** detection. For **conversation PII**, use the **Foundry (classic)** tab.

| Field | Description |
|--|--|
| **Type** | The detected type. |
| **Confidence** | The model's level of certainty regarding whether it correctly identified an entity type. |
| **Offset** | The number of characters that the entity was detected from the beginning of the text. |
| **Length** | The character length of the entity. |

Verify that the detected entities match the PII in your input text. You can use the **Edit** button to modify the **Configure** parameters and rerun detection as needed.