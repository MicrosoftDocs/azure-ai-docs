---
title: Data, privacy, and security for Azure Language in Foundry Tools
titleSuffix: Foundry Tools
description: This document details issues for data and privacy for Azure Language in Foundry Tools.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 08/15/2022
---

# Data, privacy, and security for Azure Language in Foundry Tools

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

This article provides details regarding how Azure Language in Foundry Tools processes your data. Language is designed with compliance, privacy, and security in mind. However, you are responsible for its use and the implementation of this technology. It's your responsibility to comply with all applicable laws and regulations in your jurisdiction.
 

## What data does Language process and how does it process it?

* Language processes text data that is sent by the customer to the system for the purposes of getting a response from one of the available features.
* All results of the requested feature are sent back to the customer in the API response as specified in the API reference. For example, if Language Detection is requested, the language code is returned along with a confidence score for each text record.
* Language uses aggregate telemetry such as which APIs are used and the number of calls from each subscription and resource for service monitoring purposes.
* Language doesn't store or process customer data outside the region where the customer deploys the service instance.
* Language encrypts all content, including customer data, at rest.


## How is data retained and what customer controls are available?

* Data sent in synchronous or asynchronous calls may be temporarily stored by Language for up to 48 hours only and is purged thereafter. This data is encrypted and is only accessible to authorized on call engineers when service support is needed for debugging purposes in the event of a catastrophic failure. To prevent this temporary storage of input data, the LoggingOptOut query parameter can be set accordingly. By default, this parameter is set to false for Language Detection, Key Phrase Extraction, Sentiment Analysis and Named Entity Recognition endpoints. The LoggingOptOut parameter is true by default for the PII and health feature endpoints. More information on the LoggingOptOut query parameter is available in the API reference.

To learn more about Microsoft's privacy and security commitments, visit the [Microsoft Trust Center](https://www.microsoft.com/trust-center)


## See also

* [Transparency note for Language](transparency-note.md)
* [Transparency note for Named Entity Recognition and Personally Identifying Information](transparency-note-named-entity-recognition.md)
* [Transparency note for the health feature](transparency-note-health.md)
* [Transparency note for Key Phrase Extraction](transparency-note-key-phrase-extraction.md)
* [Transparency note for Language Detection](transparency-note-language-detection.md)
* [Transparency note for Question answering](transparency-note-question-answering.md)
* [Transparency note for Summarization](transparency-note-extractive-summarization.md)
* [Transparency note for Sentiment Analysis](transparency-note-sentiment-analysis.md)
* [Guidance for integration and responsible use with Language](guidance-integration-responsible-use.md)
