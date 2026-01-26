---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
ai-usage: ai-assisted
---
## Prerequisites

* [Create a project in Foundry in the Microsoft Foundry portal](../../../../../ai-foundry/how-to/create-projects.md)

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

## [Foundry (classic)](https://ai.azure.com/) Playground

Using the left side pane, select **Playgrounds**. Then select the **Try Azure Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="Screenshot showing the Playgrounds navigation and the Try Azure Language Playground button in Foundry (classic)." lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Use Language Detection in the Foundry Playground

The **Language Playground** consists of four sections:

* Top banner: You can select any of the currently available Languages here.
* Left pane: This pane contains **Configuration** options for the service, such as the API version and model version.
* Center pane: This pane is where you enter your text for processing and review results.
* Right pane: This pane shows **Details** about the run.

Here you can select Azure Language Detection capability by choosing the top banner tile, **Detect language**.

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
|ISO 639-1 Code| The ISO 639-1 code for the most detected language.|
|Confidence Score| How confident the model is in the correctness of identification of the most typed language.|
|Script Name| The name of the most detected script in the text.|
|ISO 15924 Script Code| The ISO 15924 script code for the most detected script.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/language-detection.png" alt-text="A screenshot of an example of detect language in Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/language-detection.png":::

### [Foundry (new)](#tab/foundry-new)

> [!NOTE]
> This content refers to the [Foundry (new)](https://ai.azure.com/) portal, which supports only Foundry projects and provides streamlined access to models, agents, and tools. For more information, see [What is Microsoft Foundry?](../../../../../ai-foundry/what-is-foundry.md). To confirm that you're using Foundry (new), make sure the version toggle in the portal banner is in the **on** position. :::image type="icon" source="../../media/quickstarts/azure-ai-foundry/new-foundry.png" border="false":::

You can use [Foundry (new)](https://ai.azure.com/) to:

> [!div class="checklist"]
> * Create a project
> * Deploy a model
> * Create and run an agent
> * Upload files to the agent

## Navigate to [Foundry (new)](https://ai.azure.com/)

 The project you're working on appears in the upper-left corner.  
* You can select to create a new project from the drop-down menu:
  * Select the provided project name or create a new project name.
  * Finally, select **Create project**.

   :::image type="content" source="../../../media/new-foundry-homepage.png" alt-text="Screenshot of the Foundry (new) homepage":::

There are two ways to access the Language Detection interface:

1. Select the **Discover** tab from the upper right navigation bar to go to the **Models** page.
   * In the search bar under models, enter **Azure** and press enter.
   * Next, select **Azure-Language-detection** from the search results.
   * Finally, select the **Open in Playground** button.

1. Select the **Build** tab from the upper right navigation bar.
   * From the left navigation bar, select  **Models**.
   * Select the **AI services** tab.
   * Next, select  **Azure-Language-detection** to go to the playground.

## Use playground: detect language in text

The Foundry playground is an interactive environment where you can engage with deployed AI models.

The **Detect Language** feature identifies the language used in written content.

1. On the **Playground tab**, you can choose a text sample from the drop-down menu, choose the paperclip icon to upload your own text, or type your text directly into the sample window.

1. Next select the **Configure** button. In the **Configure** side panel, you can select from the following options:

   |Option|Description|
   |---|---|
   |**API version**| Select the API version that you prefer to use.|
   |**Model version**| Select the model version that you prefer to use.|
   |**Country/region hint** (optional)| You can select the origin country/region for the source text.|

After you make your selections, choose the **Detect** button. Then review the text and accompanying details written in formatted text or as a JSON response:

   |Field | Description|
   |---|---|
   |**Confidence**| The model's level of certainty regarding whether it correctly identified a language.|
   |**ISO 639-1 code**| A two letter code for the detected language.|
   |**Detected script**| The name of the detected script in the text.|
   |**Detected script code**| The ISO 15924 script code for the detected script (writing system).|

You can use the **Edit** button to modify the **Configure** parameters and customize your response as needed.