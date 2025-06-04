---
title: Data, privacy, and security for Azure AI Translator
titleSuffix: Azure AI services
description: This document details issues for data, privacy, and security for Azure AI Translator
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-translator
ms.topic: article
ms.date: 05/12/2024
---


# Data, privacy, and security for Azure AI Translator

This article provides some high-level details regarding how Azure AI Translator processes data provided by customers.

## What data does Translator process? 

- **Text translation**: Processes textual content submitted by the customer in plain text or HTML format. Text translation translates text by using either general or custom machine translation models.
- **Document translation**: Processes rich documents in a variety of formats including plain text, HTML, .docx, .xlsx, .pptx, .pdf, .md, and others. Document translation translates documents by using either general or custom machine translation models.

## How does Translator process data? 

The following diagram illustrates how your data is processed.

###  Text Translation

:::image type="content" source="media/translator-data.png" alt-text="A diagram of the data flow between a client and the Text Translation service.":::

###  Document Translation

:::image type="content" source="media/translator-document-data.png" alt-text="Diagram of the data flow between a client and the Document Translation service.":::

## Does Translator keep my data? 

Translator doesn’t persist customer data submitted for translation:

- **Text translation** processes customer data at REST and doesn’t store customer data.
- **Document translation** temporarily stores customer data while processing. After processing, the customer data is removed permanently with a hard delete. No customer data is persisted.

To learn more about the Translator no-trace policy and compliance, visit [Translator No Trace](https://aka.ms/TranslatorNoTrace).

## Next steps

* [Azure AI Translator transparency note](/azure/ai-foundry/responsible-ai/translator/transparency-note?context=/azure/ai-services/translator/context/context)
