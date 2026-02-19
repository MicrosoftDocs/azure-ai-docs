---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
---
## Prerequisites

* [Create a Project in Foundry in the Microsoft Foundry portal](../../../../../ai-foundry/how-to/create-projects.md)

## Navigate to the Foundry Playground

Using the left side pane, select **Playgrounds**. Then select the **Try Azure Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="The development lifecycle" lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Use Key Phrase Extraction in the Foundry Playground

The **Language Playground** consists of four sections:

* Top banner: You can select any of the currently available Languages here.
* Right pane: This pane is where you can find the **Configuration** options for the service, such as the API and model version, along with features specific to the service.
* Center pane: This pane is where you enter your text for processing. After the operation is run, some results are shown here.
* Right pane: This pane is where **Details** of the run operation are shown.

Here you can select the Key Phrase Extraction capability by choosing the top banner tile, **Extract key phrases**.

## Use Extract key phrases

**Extract key phrases** is designed to extract key phrases from text.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select text language| Select the language of the input text. |

After your operation is completed, each entity is underlined in the center pane and the **Details** section contains the following fields for the overall sentiment and the sentiment of each sentence:

|Field | Description                |
|------|----------------------------|
|Extracted key phrases|A list of the extracted key phrases.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/key-phrase-extraction.png" alt-text="A screenshot of an example of Extract key phrases in Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/key-phrase-extraction.png":::
