---
title: Export & delete data - LUIS
titleSuffix: Azure AI services
description: You have full control over viewing, exporting, and deleting their data. Delete customer data to ensure privacy and compliance.
ms.author: lajanuar
author: laujan
manager: nitinme
ms.custom: references_regions
ms.service: azure-ai-language
ms.subservice: azure-ai-luis
ms.topic: reference
ms.date: 06/12/2025
---

# Export and delete your customer data in Language Understanding (LUIS) in Azure AI services

[!INCLUDE [deprecation notice](./includes/deprecation-notice.md)]


Delete customer data to ensure privacy and compliance.

## Summary of customer data request features​
Language Understanding Intelligent Service (LUIS) preserves customer content to operate the service, but the LUIS user has full control over viewing, exporting, and deleting their data. This can be done through the LUIS web [Azure portal](luis-reference-regions.md) or the [LUIS Authoring (also known as Programmatic) APIs](/rest/api/luis/operation-groups).

[!INCLUDE [GDPR-related guidance](~/reusable-content/ce-skilling/azure/includes/gdpr-intro-sentence.md)]

Customer content is stored encrypted in Microsoft regional Azure storage and includes:

- User account content collected at registration
- Training data required to build the models
- Logged user queries used by [active learning](how-to/improve-application.md) to help improve the model
  - Users can turn off query logging by appending `&log=false` to the request, details [here](./faq.md#how-can-i-disable-the-logging-of-utterances)

## Deleting customer data
LUIS users have full control to delete any user content, either through the LUIS web portal or the LUIS Authoring (also known as Programmatic) APIs. The following table displays links assisting with both:

| | **User Account** | **Application** | **Example Utterance(s)** | **End-user queries** |
| --- | --- | --- | --- | --- |
| **Portal** | [Link](luis-concept-data-storage.md#delete-an-account) | [Link](how-to/sign-in.md) | [Link](luis-concept-data-storage.md#utterances-in-an-intent) | [Active learning utterances](how-to/improve-application.md)<br>[Logged Utterances](luis-concept-data-storage.md#disable-logging-utterances) |
| **APIs** | [Link](/rest/api/luis/azure-accounts/remove-from-app) | [Link](/rest/api/luis/apps/delete) | [Link](/rest/api/luis/examples/delete) | [Link](/rest/api/luis/versions/delete-unlabelled-utterance) |


## Exporting customer data
LUIS users have full control to view the data on the portal, however it must be exported through the LUIS Authoring (also known as Programmatic) APIs. The following table displays links assisting with data exports via the LUIS Authoring (also known as Programmatic) APIs:

| | **User Account** | **Application** | **Utterance(s)** | **End-user queries** |
| --- | --- | --- | --- | --- |
| **APIs** | [Link](/rest/api/luis/azure-accounts/list-user-luis-accounts) | [Link](/rest/api/luis/versions/export) | [Link](/rest/api/luis/examples/list) | [Link](/rest/api/luis/apps/download-query-logs) |

## Location of active learning

To enable [active learning](how-to/improve-application.md#log-user-queries-to-enable-active-learning), users' logged utterances, received at the published LUIS endpoints, are stored in the following Azure geographies:

* [Europe](#europe)
* [Australia](#australia)
* [United States](#united-states)

With the exception of active learning data (detailed below), LUIS follows the [data storage practices for regional services](https://datacenters.microsoft.com/globe/explore/).

[!INCLUDE [portal consolidation](includes/portal-consolidation.md)]


### Europe

Europe Authoring (also known as Programmatic APIs) resources are hosted in Azure's Europe geography, and support deployment of endpoints to the following Azure geographies:

* Europe
* France
* United Kingdom

When deploying to these Azure geographies, the utterances received by the endpoint from end users of your app will be stored in Azure's Europe geography for active learning.

### Australia

Australia Authoring (also known as Programmatic APIs) resources are hosted in Azure's Australia geography, and support deployment of endpoints to the following Azure geographies:

* Australia

When deploying to these Azure geographies, the utterances received by the endpoint from end users of your app will be stored in Azure's Australia geography for active learning.

### United States

United States Authoring (also known as Programmatic APIs) resources are hosted in Azure's United States geography, and support deployment of endpoints to the following Azure geographies:

* Azure geographies not supported by the Europe or Australia authoring regions

When deploying to these Azure geographies, the utterances received by the endpoint from end users of your app will be stored in Azure's United States geography for active learning.

### Switzerland North

Switzerland North Authoring (also known as Programmatic APIs) resources are hosted in Azure's Switzerland geography, and support deployment of endpoints to the following Azure geographies:

* Switzerland 

When deploying to these Azure geographies, the utterances received by the endpoint from end users of your app will be stored in Azure's Switzerland geography for active learning.

## Disable active learning

To disable active learning, see [Disable active learning](how-to/improve-application.md).


## Next steps

> [!div class="nextstepaction"]
> [LUIS regions reference](./luis-reference-regions.md)
