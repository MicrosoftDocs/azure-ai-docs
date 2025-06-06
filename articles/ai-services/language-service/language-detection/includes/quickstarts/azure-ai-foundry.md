---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 02/16/2025
ms.author: lajanuar
---

## Prerequisites

* [Create a Project in Foundry in the Azure AI Foundry Portal](../../../../../ai-foundry/how-to/create-projects.md)

## Navigate to the Azure AI Foundry Playground

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

|Field | Description                |
|------|----------------------------|
|Sentence|
|Iso 639-1 Code| The ISE 639-1 code for the most detected language.|
|Confidence Score| How confident the model is in the correctness of identification of the most typed language.|
|Script Name| The name of the most detected script in the text.
|Iso 15924 Script Code| The ISO 15924 script code for the most detected script.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/language-detection.png" alt-text="A screenshot of an example of detect language in Azure AI Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/language-detection.png":::
