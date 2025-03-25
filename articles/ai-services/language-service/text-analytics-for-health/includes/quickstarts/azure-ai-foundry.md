---
author: jboback
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 02/16/2025
ms.author: jboback
---

## Prerequisites

* [Create a Project in Foundry in the Azure AI Foundry Portal](../../../../../ai-foundry/how-to/create-projects.md)

## Navigate to the Azure AI Foundry Playground

Using the left side pane, select **Playgrounds**. Then select the **Try the Language Playground** button.

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png" alt-text="The development lifecycle" lightbox="../../media/quickstarts/azure-ai-foundry/foundry-playground-navigation.png":::

## Use Text Analytics for Health in the Azure AI Foundry Playground

The **Language Playground** consists of four sections:

* Top banner: You can select any of the currently available Language services here.
* Right pane: This pane is where you can find the **Configuration** options for the service, such as the API and model version, along with features specific to the service.
* Center pane: This pane is where you enter your text for processing. After the operation is run, some results are shown here.
* Right pane: This pane is where **Details** of the run operation are shown.

Here you can select the Text Analytics for Health capability by choosing the top banner tile, **Extract health information**.

## Use Extract health information

**Extract health information** is designed to identify and extract health information in text.

In **Configuration** there are the following options:

|Option              |Description                              |
|--------------------|-----------------------------------------|
|Select API version  | Select which version of the API to use.    |
|Select model version| Select which version of the model to use.|
|Select text language| Select which language the language is input in.|
|Return output in FHIR structure| Returns the output in the Fast Healthcare Interoperability Resources (FHIR) structure.|

After your operation is completed, the type of entity is displayed beneath each entity in the center pane and the **Details** section contains the following fields for each entity:

|Field | Description                |
|------|----------------------------|
|Entity|The detected entity.|
|Category| The type of entity that was detected.|
|Confidence| How confident the model is in the correctness of identification of entity's type.|

:::image type="content" source="../../media/quickstarts/azure-ai-foundry/text-analytics-for-health.png" alt-text="A screenshot of an example of extract health information in Azure AI Foundry portal." lightbox="../../media/quickstarts/azure-ai-foundry/text-analytics-for-health.png":::
