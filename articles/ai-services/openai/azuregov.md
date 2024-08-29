---
title: Azure OpenAI in Azure Government
titleSuffix: Azure OpenAI
description: Learn how to use Azure OpenAI in the Azure Government cloud.
author: chaparker
manager: gregc
ms.service: azure-ai-openai
ms.topic: how-to
ms.custom: references_regions, azuregov
ms.date: 8/29/2024
recommendations: false
---

# Azure OpenAI service in Azure Government

This article highlights the differences when using Azure OpenAI in Azure Government as compared to the commercial cloud offering. Learn more about the Azure OpenAI service itself in [Azure OpenAI Service documentation](/azure/ai-services/openai/).

## Azure OpenAI Features in Azure Government:

|Feature|Azure OpenAI|
|--------|--------|
|Models available|US Gov Arizona:<br>&nbsp;&nbsp;&nbsp;GPT-4o (2024-05-13)&nbsp;&nbsp;&nbsp;GPT-4 (1106-Preview)<br>&nbsp;&nbsp;&nbsp;GPT-3.5-Turbo (0125)&nbsp;&nbsp;&nbsp;GPT-3.5-Turbo (1106)<br>&nbsp;&nbsp;&nbsp;text-embedding-ada-002 (version 2)<br><br>US Gov Virginia:<br>&nbsp;&nbsp;&nbsp;GPT-4o (2024-05-13)&nbsp;&nbsp;&nbsp;GPT-4 (1106-Preview)<br>&nbsp;&nbsp;&nbsp;GPT-3.5-Turbo (0125)<br>&nbsp;&nbsp;&nbsp;text-embedding-ada-002 (version 2)<br><br>Learn more about the different capabilities of each model in [Azure OpenAI Service models](/azure/ai-services/openai/concepts/models)|
|Virtual network support & private link support| Yes. |
| Connect your data | Available in US Gov Virginia and Arizona. Virtual network and private links are supported. Deployment to a web app or a copilot in Copilot Studio is not supported. |
|Managed Identity|Yes, via Microsoft Entra ID|
|UI experience|**Azure portal** for account & resource management<br>**Azure OpenAI Studio** for model exploration|
|Abuse Monitoring|Not all features of Abuse Monitoring are enabled for AOAI in Azure Government. You will be responsible for implementing reasonable technical and operational measures to detect and mitigate any use of the service in violation of the Product Terms. [Automated Content Classification and Filtering](/azure/ai-services/openai/concepts/content-filter) remains enabled by default for Azure Government.|
|Data Storage|In AOAI, customer data is only stored at rest as part of our Finetuning solution. Since Finetuning is not enabled within Azure Gov, there is no customer data stored at rest in Azure Gov associated with AOAI. However, Customer Managed Keys (CMK) can still be enabled in Azure Gov to support use of the same policies in Azure Gov as in Public cloud. Note also that if Finetuning is enabled in Azure Gov in the future, any existing CMK deployment would be applied to that data at that time.|

## Next steps
* To request quota increases for the pay-as-you-go consumption model, apply at [https://aka.ms/AOAIGovQuota](https://aka.ms/AOAIGovQuota)
* If modified content filters are required, apply at [https://aka.ms/AOAIGovModifyContentFilter](https://aka.ms/AOAIGovModifyContentFilter)

## Service Endpoints

|Service category|Service name|Azure Public|Azure Government|Notes|
|-----------|-----------|-------|----------|----------------------|
||Azure OpenAI Service|openai.azure.com|openai.azure.us||
