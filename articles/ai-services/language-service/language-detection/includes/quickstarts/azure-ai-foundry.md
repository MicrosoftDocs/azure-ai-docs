---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/05/2025
ms.author: lajanuar
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

## Navigate to the [Azure AI Foundry (new)](https://ai.azure.com/) Playground

Using the left side pane, select **Playgrounds**. Then select the **Try the Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="The development lifecycle" lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Use Language Detection in the Azure AI Foundry Playground

The **Language Playground** consists of four sections:

* Top banner: You can select any of the currently available Language services here.
* Right pane: This pane is where you can find the **Configuration** options for the service, such as the API and model version, along with features specific to the service.
* Center pane: This pane is where you enter your text for processing. After the operation is run, some results are shown here.
* Right pane: This pane is where **Details** of the run operation are shown.

Here you can select the Language Detection capability by choosing the top banner tile, **Detect language**.

## Use Detect language

**Detect language** is designed to identify the language typed in text.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select country hint| Select the origin country/region of the input text. |

After your operation is completed, the **Details** section contains the following fields for the most detected language and script:

|Field | Description|
|---|---|
|ISO 639-1 Code| The ISE 639-1 code for the most detected language.|
|Confidence Score| How confident the model is in the correctness of identification of the most typed language.|
|Script Name| The name of the most detected script in the text.
|Iso 15924 Script Code| The ISO 15924 script code for the most detected script.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/language-detection.png" alt-text="A screenshot of an example of detect language in Azure AI Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/language-detection.png":::

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

## Navigate to [Azure AI Foundry (new)](https://ai.azure.com/)

There are two ways to access the PII interface:
1. From Discover
   * Select Discover, which takes you to the Models page.
   * In the search bar under models, enter **Azure** and press enter.
   * Select **Azure-Language-detection** from the search results.
   * Select open in playground.

1. From Build
   * Select Build from the upper nav bar.
   * Select Models from the left nav bar.
   * Select AI services tab.
   * Select **Azure-Language-detection**.
   * Select open in playground.

## Use playground: extract PII from text

The **detect language** feature identifies the language used in written content.

1. On the **Playground tab**, you can choose a text sample from the drop-down menu, choose the paperclip icon to upload your own text, or type your text directly into the sample window.

1. Next select the **Configure** button. In the **Configure** side panel you can select from the following options:

   |Option|Description|
   |---|---
   |**API version**| Select the API version that you prefer to use.|
   |**Model version**| Select the model version that you prefer to use.|
   |**Country/region hint** (optional)| You can select the origin country/region for the source text.|

After you make your selections, choose the **Detect** button. Then review the text and accompanying details written in formatted text or as a JSON response:

   |Field | Description|
   |---|---|
   |**Confidence**| The model's level of certainty regarding whether it has correctly identified language.|
   |**ISO 639-1 code**| A two letter code for the detected language.|
   |**Detected script**| The name of the detected script in the text.
   |**Detected script code**| The ISO 15924 script code for the detected script (writing system).|

You can use the **Edit** button to modify the **Configure** parameters and customize your response as needed.