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

## Use Sentiment Analysis in the Foundry Playground

The **Language Playground** consists of four sections:

* Top banner: You can select any of the currently available Languages here.
* Right pane: This pane is where you can find the **Configuration** options for the service, such as the API and model version, along with features specific to the service.
* Center pane: This pane is where you enter your text for processing. After the operation is run, some results are shown here.
* Right pane: This pane is where **Details** of the run operation are shown.

Here you can select the Sentiment Analysis capability by choosing the top banner tile, **Analyze sentiment**.

## Use Analyze sentiment

**Analyze sentiment** is designed to identify positive, negative and neutral sentiment in text.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select text language| Select the language of the input text. |
|Enable opinion mining| Enables or disables the opinion mining skill.|

After your operation is completed, in the center pane, each sentence will be numbered and opinions will be labeled if **Enable opinion mining** was checked and the **Details** section contains the following fields for the overall sentiment and the sentiment of each sentence:

|Field | Description                |
|------|----------------------------|
|Sentence number|The number of the sentence in the order it was typed. This field is not present for **Overall sentiment**.|
|Sentiment| The detected overall sentiment for the segment of text.|
|Scores| The amount of positive, neutral and negative sentiment detected in the text segment.|

The following fields are only present if opinion mining is enabled:

|Field | Description                |
|------|----------------------------|
|Target|The target of the detected opinion.|
|Assessments| The detected opinion and the detected persuasion (positive, neutral, negative), as well as the percent of detected persuasion.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/sentiment-opinion-mining.png" alt-text="An example of Analyze sentiment in Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/sentiment-opinion-mining.png":::
