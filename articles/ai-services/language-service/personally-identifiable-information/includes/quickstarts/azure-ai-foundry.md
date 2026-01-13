---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-pii
---
## Prerequisites

> [!TIP]
>
> * If you already have an Azure Language in Foundry Tools or multi-service resource—whether used on its own or through Language Studio—you can continue to use those existing Language resources within the Microsoft Foundry portal. 
> * For more information, see [How to use Foundry Tools in the Foundry portal](/azure/ai-services/connect-services-foundry-portal).
> * We highly recommended that you use a Foundry resource in the Foundry; however, you can also follow these instructions using a Language resource.

* **Azure subscription**. If you don't have one, you can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* **Requisite permissions**. Make sure the person establishing the account and project is assigned as the Azure AI Account Owner role at the subscription level. Alternatively, having either the **Contributor** or **Cognitive Services Contributor** role at the subscription scope also meets this requirement. For more information, *see* [Role based access control (RBAC)](/azure/ai-foundry/openai/how-to/role-based-access-control#cognitive-services-contributor).
*  [Foundry resource](/azure/ai-services/multi-service-resource). For more information, *see* [Configure a Foundry resource](../../../concepts/configure-azure-resources.md). Alternately, you can use a [Language resource](https://portal.azure.com/?Microsoft_Azure_PIMCommon=true#create/Microsoft.CognitiveServicesTextAnalytics).
* **A Foundry project created in the Foundry**. For more information, *see* [Create a Foundry project](/azure/ai-foundry/how-to/create-projects).


### [Foundry (classic)](#tab/foundry-classic)

> [!NOTE]
> This content refers to the [Foundry (classic)](https://ai.azure.com/) portal, which supports hub-based projects and other resource types. To confirm that you're using Foundry (classic), make sure the version toggle in the portal banner is in the **off** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/classic-foundry.png" border="false":::


You can use [Foundry (classic)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Run a chat completion
> * Create and run an agent
> * Upload files to your agent


## Navigate to the [Foundry (classic)](https://ai.azure.com/) Playground

Using the left side pane, select **Playgrounds**. Then select the **Try Azure Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="The development lifecycle" lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Use PII in the Foundry Playground

The **Language Playground** consists of four sections:

* Top banner: You can select any of the currently available Languages here.
* Right pane: This pane is where you can find the **Configuration** options for the service, such as the API and model version, along with features specific to the service.
* Center pane: This pane is where you enter your text for processing. After the operation is run, some results will be shown here.
* Right pane: This pane is where **Details** of the run operation are shown.

Here you can select from two Personally Identifying Information (PII) detection capabilities by choosing the top banner tiles, **Extract PII from conversation** or **Extract PII from text**. Each is for a different scenario.

### Extract PII from conversation

**Extract PII from conversation** is designed to identify and mask personally identifying information in conversational text.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select text language| Select which language the language is input in.|
|Select types to include| Select they types of information you want to redact.|
|Specify redaction policy| Select the method of redaction.|
|Specify redaction character| Select which character is used for redaction. Only available with the **CharacterMask** redaction policy.|

After your operation is completed, the type of entity is displayed beneath each entity in the center pane. The **Details** section contains the following fields for each entity:

|Field | Description                |
|------|----------------------------|
|Entity|The detected entity.|
|Category| The entity type that was detected.|
|Offset| The number of characters that the entity was detected from the beginning of the line.|
|Length| The character length of the entity.|
|Confidence| How confident the model is in the correctness of identification of entity's type.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/conversation-pii.png" alt-text="A screenshot of an example of extract PII from conversation in Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/conversation-pii.png":::

### Extract PII from text

**Extract PII from text** is designed to identify and mask personally identifying information in text.

In **Configuration** you can select from the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select text language| Select which language the language is input in.|
|Select types to include| Select the types of information you want to redact.|
|Specify redaction policy| Select the method of redaction.|
|Specify redaction character| Select which character is used for redaction. Only available with the **CharacterMask** redaction policy.|

After your operation is completed, the type of entity is displayed beneath each entity in the center pane. The **Details** section contains the following fields for each entity:

|Field | Description                |
|------|----------------------------|
|Entity|The detected entity.|
|Category| The entity type that was detected.|
|Offset| The number of characters that the entity was detected from the beginning of the line.|
|Length| The character length of the entity.|
|Confidence| How confident the model is in the correctness of identification of entity's type.|
|Tags| How confident the model is in the correctness for each identified entity type.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/text-pii.png" alt-text="A screenshot of an example of extract PII from text in Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/text-pii.png":::

### [Foundry (new)](#tab/foundry-new)

> [!NOTE]
> This content refers to the [Foundry (new)](https://ai.azure.com/) portal, which supports only [Foundry projects](/azure/ai-foundry/what-is-foundry) and provides streamlined access to models, agents, and tools. To confirm that you're using Foundry (new), make sure the version toggle in the portal banner is in the **on** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/new-foundry.png" border="false":::


You can use [Foundry (new)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Create and run an agent
> * Upload files to the agent


## Navigate to [Foundry (new)](https://ai.azure.com/)

* The project you're working on appears in the upper-left corner.  
* You can select to create a new project from the drop-down menu:
  * Select the provided project name or create a new project name.
  * Finally, select **Create project**.

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


## Use playground: extract PII from text

The Foundry playground is an interactive environment where you can engage with deployed AI models.

The **extract PII from text** feature detects and masks personally identifying information within written content.

1. On the **Playground** tab, select the sample tab, use the paperclip icon to upload your text, or enter your own text.

1. Next select the **Configure** button. In the **Configure** side panel, you can select from the following options:

| Option | Description |
|--|--|
| **API version** | Select the API version that you prefer to use. |
| **Model version** | Select the model version that you prefer to use. |
| **Language** | Select the language in which your source text is written. |
| **Types** | Select the types of information you want to redact. |
| **Specify redaction policy** | Select the method of redaction. |
| **Excluded values** | Select the values that you want to exclude. |
| **Synonyms** | Select a category for your redaction type values to target related synonyms. |

After you make your selections, choose the **Detect** button. Then review the text and accompanying details written in formatted text or as a JSON response:

| Field | Description |
|--|--|
| **Type** | The detected type. |
| **Confidence** | The model's level of certainty regarding whether it correctly identified an entity type. |
| **Offset** | The number of characters that the entity was detected from the beginning of the text. |
| **Length** | The character length of the entity. |

You can use the **Edit** button to modify the **Configure** parameters and customize your response as needed.