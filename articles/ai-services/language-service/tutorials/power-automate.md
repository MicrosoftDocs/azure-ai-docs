---
title: Use Language service in power automate
titleSuffix: Foundry Tools
description: Learn how to use Azure Language in Foundry Tools in power automate, without writing code.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: tutorial
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: cogserv-non-critical-language
---
#  Use Azure Language in Power Automate

You can use [Power Automate](/power-automate/getting-started) flows to automate repetitive tasks and bring efficiency to your organization. Using Azure Language in Foundry Tools, you can automate tasks like:
* Send incoming emails to different departments based on their contents. 
* Analyze the sentiment of new tweets.
* Extract entities from incoming documents. 
* Summarize meetings.
* Remove personal data from files before saving them.

In this tutorial, you'll create a Power Automate flow to extract entities found in text, using [Named entity recognition](../named-entity-recognition/overview.md).

## Prerequisites
* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* Once you have your Azure subscription, <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics"  title="Create a Language resource"  target="_blank">create a Language resource </a> in the Azure portal to get your key and endpoint.  After it deploys, select **Go to resource**.
    * You will need the key and endpoint from the resource you create to connect your application to the API. You'll paste your key and endpoint into the code below later in the quickstart.
    * You can use the free pricing tier (`Free F0`) to try the service, and upgrade later to a paid tier for production.
* Optional for this tutorial: A trained model is required if you're using a custom capability such as [custom NER](../custom-named-entity-recognition/overview.md), [custom text classification](../custom-text-classification/overview.md), or [conversational language understanding](../conversational-language-understanding/overview.md).

## Create a Power Automate flow

For this tutorial, you will create a flow that extracts named entities from text.

1. [Sign in to power automate](https://make.powerautomate.com/)

1. From the left side menu, select **My flows**. Then select **New flow** > **Automated cloud flow**.

    :::image type="content" source="../media/create-flow.png" alt-text="A screenshot of the menu for creating an automated cloud flow." lightbox="../media/create-flow.png":::

1. Enter a name for your flow such as `LanguageFlow`. Then select **Skip** to continue without choosing a trigger.

    :::image type="content" source="../media/language-flow.png" alt-text="A screenshot of automated cloud flow screen." lightbox="../media/language-flow.png":::

1. Under **Triggers** select **Manually trigger a flow**.

    :::image type="content" source="../media/trigger-flow.png" alt-text="A screenshot of how to manually trigger a flow." lightbox="../media/trigger-flow.png":::

1. Select **+ New step** to begin adding a Language connector. 

1. Under **Choose an operation** search for **Language**. Then select **Language**. This will narrow down the list of actions to only those that are available for Language.

    :::image type="content" source="../media/language-connector.png" alt-text="A screenshot of A Language connector." lightbox="../media/language-connector.png":::

1. Under **Actions** search for **Named Entity Recognition**, and select the connector. 

    :::image type="content" source="../media/entity-connector.png" alt-text="A screenshot of a named entity recognition connector." lightbox="../media/entity-connector.png":::

1. Get the endpoint and key for your Language resource, which will be used for authentication. You can find your key and endpoint by navigating to your resource in the [Azure portal](https://portal.azure.com), and selecting **Keys and Endpoint** from the left side menu.

    :::image type="content" source="../media/azure-portal-resource-credentials.png" alt-text="A screenshot of A language resource key and endpoint in the Azure portal." lightbox="../media/azure-portal-resource-credentials.png":::

1. Once you have your key and endpoint, add it to the connector in Power Automate.
 
    :::image type="content" source="../media/language-auth.png" alt-text="A screenshot of adding the language key and endpoint to the Power Automate flow." lightbox="../media/language-auth.png":::

1. Add the data in the connector
:::image type="content" source="../media/connector-data.png" alt-text="A screenshot of data being added to the connector." lightbox="../media/connector-data.png":::
    
    > [!NOTE]
    > You will need deployment name and project name if you're using custom language capability.
    
1. From the top navigation menu, save the flow and select **Test the flow**. In the window that appears, select **Test**. 
:::image type="content" source="../media/test-connector.png" alt-text="A screenshot of how to run the flow." lightbox="../media/test-connector.png":::

1. After the flow runs, you can see the response in the **outputs** field.

    :::image type="content" source="../media/response-connector.png" alt-text="A screenshot of flow response." lightbox="../media/response-connector.png":::

## Next steps 

* [Triage incoming emails with custom text classification](../custom-text-classification/tutorials/triage-email.md)
* [Available Language connectors](/connectors/cognitiveservicestextanalytics)


