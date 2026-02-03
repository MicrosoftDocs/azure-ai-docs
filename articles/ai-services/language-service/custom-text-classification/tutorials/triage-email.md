---
title: Triage incoming emails with Power Automate
titleSuffix: Foundry Tools
description: Learn how to use custom text classification to categorize and triage incoming emails with Power Automate
#services: cognitive-services
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: tutorial
ms.date: 12/15/2025
ms.author: lajanuar
---
# Tutorial: Triage incoming emails with Power Automate

In this tutorial, you learn to categorize and triage incoming email using custom text classification. With this [Power Automate](/power-automate/getting-started) flow, a new email is received, its contents are classified, and, depending on the result, a message is sent to a designated channel on [Microsoft Teams](https://www.microsoft.com/microsoft-teams).


## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* <a href="https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics"  title="Create a Language resource"  target="_blank">A Language resource </a>
    * A trained [custom text classification](../overview.md) model.
    * You need the key and endpoint from your Language resource to authenticate your Power Automate flow.
* A successfully created and deployed [single text classification custom model](../quickstart.md)


## Create a Power Automate flow

1. [Sign in to Power Automate](https://make.powerautomate.com/)

2. From the left side menu, select **My flows** and create a **Automated cloud flow**

    :::image type="content" source="../media/create-flow.png" alt-text="A screenshot of the flow creation screen." lightbox="../media/create-flow.png":::

3. Name your flow `EmailTriage`. Below **Choose your flow's triggers**, search for *email* and select **When a new email arrives**. Then select **create**

    :::image type="content" source="../media/email-flow.png" alt-text="A screenshot of the email flow triggers." lightbox="../media/email-flow.png":::

4. Add the right connection to your email account. This connection is used to access the email content.

5. To add a Language connector, search for *Azure Language in Foundry Tools*.
  
    :::image type="content" source="../media/language-connector.png" alt-text="A screenshot of available Language connectors." lightbox="../media/language-connector.png":::

6. Search for *CustomSingleLabelClassification*.

    :::image type="content" source="../media/single-classification.png" alt-text="A screenshot of Classification connector." lightbox="../media/single-classification.png":::

7. Start by adding the right connection to your connector. This connection is used to access the classification project.

8. In the documents ID field, add **1**.

9. In the documents text field, add **body** from **dynamic content**.

10. Fill in the project name and deployment name of your deployed custom text classification model.

    :::image type="content" source="../media/classification.png" alt-text="A screenshot project details." lightbox="../media/classification.png":::

11. Add a condition to send a Microsoft Teams message to the right team by:
    1. Select **results** from **dynamic content**, and add the condition. For this tutorial, we're looking for `Computer_science` related emails. In the **Yes** condition, choose your desired option to notify a team channel. In the **No** condition, you can add other conditions to perform alternative actions.

    :::image type="content" source="../media/email-triage.png" alt-text="A screenshot of email flow." lightbox="../media/email-triage.png":::


## Next steps

* [Use Azure Language with Power Automate](../../tutorials/power-automate.md)
* [Available Language connectors](/connectors/cognitiveservicestextanalytics)
