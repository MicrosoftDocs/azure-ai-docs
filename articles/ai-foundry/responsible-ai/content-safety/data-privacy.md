---
title: Data, privacy, and security for AI Content Safety
titleSuffix: Foundry Tools
description: This document details issues for data, privacy, and security for Azure AI Content Safety.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: concept-article
ms.date: 05/15/2023
---


# Data, privacy, and security for Azure AI Content Safety

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

This article provides details regarding how your data is processed, used, and stored by Azure AI Content Safety.

Azure AI Content Safety was designed with privacy and security in mind; however, the customer is responsible for its use and the implementation of this technology.


## How is data retained and what customer controls are available?

Azure AI Content Safety works to filter harmful content. This system works by running the input through an ensemble of classification models. Once your Azure AI Content Safety resource is created, you can submit text and images to the model through the REST API, client libraries, or the Azure AI Content Safety Studio; the model generates outputs that are returned through the API.

No input texts or images are stored in the model during detection (except for customer-supplied blocklists, as discussed below), and user inputs are not used to train, retrain, or improve the Azure AI Content Safety models.

- **Blocklist data**. The Blocklist API allows customers to upload their block items for the purpose of supplementing the Azure AI Content Safety model.  **Block Item data is stored in Azure Storage, encrypted at rest by Microsoft Managed keys, within the same region as the resource and logically isolated with the customer's Azure subscription and API Credentials**. Uploaded items can be deleted by the user via the DELETE API operation. Block Items are not used to improve the Azure AI Content Safety models.

To learn more about Microsoft's privacy and security commitments visit the [Microsoft Trust Center](https://www.microsoft.com/TrustCenter/CloudServices/Azure/default.aspx).

## Is customer data processed by Azure AI Content Safety transmitted outside of the Azure AI Content Safety service or the selected region?

No. Microsoft hosts the Azure AI Content Safety models within our Azure infrastructure. All customer data sent to Azure AI Content Safety remains within Azure AI Content Safety and in the region you chose and will not be transmitted to other regions.

## Is customer data used to train the Azure AI Content Safety models?

No. We do not use customer data to train, retrain or improve the models in Azure AI Content Safety.

## Does Azure OpenAI Abuse Monitoring apply to the data that customers send to Azure AI Content Safety? 

No. The Azure OpenAI [Abuse Monitoring process](/azure/ai-foundry/openai/concepts/abuse-monitoring) does not apply to customer data transmitted to Azure AI Content Safety. User input data sent to Azure AI Content Safety is not stored or made available for human review by Microsoft employees. 

## Feedback and Reporting

If you have feedback on Azure AI Content Safety; suspect that Azure AI Content Safety is being used in a manner that is abusive or illegal, infringes on your rights or the rights of other people, or violates these policies; or if the system fails to block harmful content that you believe should have been filtered, please report it to this [email](mailto:acm-team@microsoft.com).

## Next steps

* [AI Content Safety quickstart](/azure/ai-services/content-safety/quickstart-text)
* [Transparency Note](/azure/ai-foundry/responsible-ai/content-safety/transparency-note)
