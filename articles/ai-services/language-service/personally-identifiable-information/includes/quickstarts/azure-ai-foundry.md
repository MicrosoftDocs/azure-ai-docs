---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/05/2025
ms.author: lajanuar
ms.custom: language-service-pii
---

## Prerequisites

* [Create a Project in Foundry in the Azure AI Foundry Portal](/azure/ai-foundry/how-to/create-projects)

### [Azure AI Foundry (classic)](#tab/foundry-classic)

> [!NOTE]
> This content refers to the [Azure AI Foundry (classic)](https://ai.azure.com/) portal, which supports hub-based projects and other resource types.Look for :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/classic-foundry.png" border="false"::: in the portal banner to confirm you're using Azure AI Foundry (classic).
> 
> → You can switch to the [Azure AI Foundry (new) ](https://ai.azure.com/) portal for streamlined access to models, agents, and tools with Foundry projects.
>

You can use [Azure AI Foundry (classic)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Run a chat completion
> * Create and run an agent
> * Upload files to the agent


## Navigate to the Azure AI Foundry Playground

Using the left side pane, select **Playgrounds**. Then select the **Try the Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="The development lifecycle" lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Use PII in the Azure AI Foundry Playground

The **Language Playground** consists of four sections:

* Top banner: You can select any of the currently available Language services here.
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

After your operation is completed, the type of entity is displayed beneath each entity in the center pane and the **Details** section contains the following fields for each entity:

|Field | Description                |
|------|----------------------------|
|Entity|The detected entity.|
|Category| The type of entity that was detected.|
|Offset| The number of characters that the entity was detected from the beginning of the line.|
|Length| The character length of the entity.|
|Confidence| How confident the model is in the correctness of identification of entity's type.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/conversation-pii.png" alt-text="A screenshot of an example of extract PII from conversation in Azure AI Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/conversation-pii.png":::

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

After your operation is completed, the type of entity is displayed beneath each entity in the center pane and the **Details** section contains the following fields for each entity:

|Field | Description                |
|------|----------------------------|
|Entity|The detected entity.|
|Category| The type of entity that was detected.|
|Offset| The number of characters that the entity was detected from the beginning of the line.|
|Length| The character length of the entity.|
|Confidence| How confident the model is in the correctness of identification of entity's type.|
|Tags| How confident the model is in the correctness for each identified entity type.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/text-pii.png" alt-text="A screenshot of an example of extract PII from text in Azure AI Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/text-pii.png":::

### [Azure AI Foundry (new)](#tab/foundry-new)

> [!NOTE]
> This content refers to the [Azure AI Foundry (new)](https://ai.azure.com/) portal, which supports only [Foundry projects](/azure/what-is-azure-ai-foundry/view=foundry-classic&preserve-view=true#project-types) and provides streamlined access to models, agents, and tools. Look for :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/new-foundry.png" border="false"::: in the portal banner to confirm you're using Azure AI Foundry (new).
> 
> → You can switch to the [Azure AI Foundry (classic)](https://ai.azure.com/) portal to use other resource types, such as hub-based projects.
>

You can use [Azure AI Foundry (new)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Create and run an agent
> * Upload files to the agent


## Navigate to Azure AI Foundry


There are two ways to access the PII interface:
1. From Discover
   * Select Discover, which takes you to the Models page
   * In the search bar under models, enter **Azure** and press enter.
   * Select **Azure-Language-Text-PII redaction** from the search results.
   * Select open in playground

1. From Build
   * Select Build from the upper nav bar
   * Select Models from the left nav bar
   * Select AI services tab
   * Select **Azure-Language-Text-PII redaction**.
   * Select open in playground

## Use playground: extract PII from text

The **extract PII from text** feature detects and masks personally identifying information within written content.

1. On the **Playground** tab, select the sample tab, use the paperclip icon to upload your text, or enter your own text.

1. Next select the **Configure** button. In the **Configure** side panel you can select from the following options:

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
| **Confidence** | The model's level of certainty regarding whether it has correctly identified an entity's type. |
| **Offset** | The number of characters that the entity was detected from the beginning of the text. |
| **Length** | The character length of the entity. |

You can use the **Edit** button to modify the **Configure** parameters and customize your response as needed.