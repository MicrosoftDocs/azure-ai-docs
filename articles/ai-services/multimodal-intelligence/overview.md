---
title: What is Azure AI Multimodal Intelligence?
titleSuffix: Azure AI services
description: Learn about Multimodal Intelligence solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-document-intelligence
ms.topic: overview
ms.date: 10/09/2024
#Customer intent: As a developer of content management software, I want to find out whether Azure AI Multimodal Intelligence is the right solution for my moderation needs.
---

# What is Azure AI Multimodal Intelligence?

:::image type="content" source="media/overview/media-input.png" alt-text="Screenshot of accepted media input files.":::

Azure AI Multimodal Intelligence is a cloud-based solution on the Azure platform designed to process various data modalities such as documents, images, videos, and audio within a unified workflow. Integrating these diverse modalities enables Multimodal Intelligence to deliver more extensive, efficient, and accurate results compared to single modality processing. Utilizing the Multimodal Intelligence service, provides you with access to the following processes:

* [**Comprehensive content extraction and analysis**](#features-and-capabilities)

* [**Diverse modality processing**](#features-and-capabilities).

* [**High-level schema extraction**](#features-and-capabilities).

* [**Grounded results for higher accuracy**](#features-and-capabilities)

* [**Enhanced data-input alignment framework**](#features-and-capabilities)

* [**Precise and efficient extraction of modality-specific details for secondary processing scenarios**](#features-and-capabilities).


## Features and capabilities

|Capability|Description|
|:---------|:----------|
|Comprehensive content extraction and analysis|&bullet; **Synchronous**. Process a given document and return the result in the same REST API call.</br></br>&bullet; **Long-running operations (LRO)**. Process larger documents and return an operation location where user can poll for the result.</br></br>&bullet; **Batch**. Process a a set of documents from a blob and write the results to a blob.|
|Diverse modality processing|Multimodal Intelligence intakes document, image, audio, video, and mixed media input and converts it into a structured format easily analyzed and further processed by other services and applications.|
|High-level schema extraction|Users can define the structure and the schema of the extracted results or use a predefined schema for specific schema values: </br></br>&bullet; **Extracted (explicit)**. Values like the name of the product in a recording or the brand/logo from a video are examples of extracted values.</br></br>&bullet; **Inferred (implicit)**. Inferred values aren't explicitly present in the content but can be determined based on the content. The sum of all line items in an invoice or the end date of a contract given a start date and duration are examples of inferred values.</br></br>&bullet; **Abstracted (tacit)**. Abstracted values are generated based on the content of the input. Examples include summaries, outlines, recaps are examples of abstracted values.
|Grounded results for higher accuracy|Multimodal Intelligence ensures that responses are anchored to your input files, leading to higher precision in extracted values. The source information is pivotal to assessing groundedness, serving as the foundation for both grounding and accuracy. A grounded response adheres strictly to the provided information, avoiding any speculation or fabrication. |
|Highly precise confidence scores|The Multimodal Intelligence enhanced data-input alignment framework ensures a high level of certainty and accuracy across various contexts. A confidence score, ranging from 0 to 1, quantifies the likelihood by assessing the statistical certainty that the extracted result is accurate, correct, and reliable. High confidence scores signify precise data extraction. Accurate extraction scores facilitate straight-through processing (STP) in automation workflows.|
|Precise and efficient extraction of modality-specific details for secondary processing scenarios| Users can extract specific content that is suitable for secondary scenarios likeLarge Language Model (LLM) processing.|

## Use cases

|Use|Scenario|
|--------|-------|
|Tax processing automation| Tax preparing companies can use the extended capabilities of Multimodal Intelligence to generate a unified view of information from different documents and generate comprehensive tax returns.|
|Call center post-call analytics| Businesses and call center operators can generate insights from call recordings to track key KPIs to improve product experience, generate business insights, create differentiated customer experiences, and answer queries faster and more accurately.
|Marketing automation digital asset management| Independent software and media vendors that build media asset management solutions can use Multimodal Intelligence to extract richer, targeted content from images and videos.|

## Getting started

Before you get started using Multimodal Intelligence, you need an Azure AI services multi-service resource. The multi-service resource enables access to multiple Azure AI services with a single set of credentials.

1.  To get started, you need an active [**Azure account**](https://azure.microsoft.com/free/cognitive-services/). If you don't have one, you can [**create a free 12-month subscription**](https://azure.microsoft.com/free/).

1. Sign in to the [Azure portal](https://portal.azure.com) and select **Create a resource** from the Azure portal home page. The Azure AI services multi-service resource is listed under Azure AI services → Azure AI services in the portal as shown here:

  :::image type="content" source="media/overview/azure-multi-service-resource.png" alt-text="Screenshot of the multi-service resource page in the Azure portal.":::

  > [!IMPORTANT]
  > Azure provides more than one resource types named Azure AI services. Be sure to select the one that is listed under Azure AI services → Azure AI services with the logo as shown previously.

1. Select the **Create** button.

1. Next, you're going to fill out the **`Create Document Intelligence`** fields with the following values:

    * **Subscription**. Select one of your available Azure subscriptions.
    * **Resource group**. The [Azure resource group](/azure/cloud-adoption-framework/govern/resource-consistency/resource-access-management#what-is-an-azure-resource-group) that contains your resource. You can create a new group or add it to an existing group.
    * **Region**. Select your local region. Different locations may introduce latency, but have no impact on the runtime availability of your resource.
    * **Name**. Enter a name for your resource. We recommend using a descriptive name, for example *YourNameAIServicesResource*.
    * **Pricing tier**. The cost of your resource depends on the pricing tier and options you choose and your usage. For more information, see [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/). You can use the free pricing tier (F0) to try the service, and upgrade later to a paid tier for production.

1. Configure other settings for your resource as needed, read, and accept the conditions (as applicable), and then select **Review + create**.

1. Azure will run a quick validation check, after a few seconds you should see a green banner that says **Validation Passed**.

1. Once the validation banner appears, select the **Create** button from the bottom-left corner.

1. After you select create, you'll be redirected to a new page that says **Deployment in progress**. After a few seconds, you'll see a message that says, **Your deployment is complete**.

## Pricing

Pricing tiers (and the amount you're billed) are based on the number of transactions that you send by using your authentication information. Each pricing tier specifies the:

* Maximum number of allowed transactions per second (TPS).
* Service features enabled within the pricing tier.
* Cost for a predefined number of transactions. Going above this number causes an extra charge, as specified in the [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services) for your service.





