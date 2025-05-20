---
title: Personally Identifiable Information (PII) Filter
description: Learn about the Personally Identifiable Information (PII) filter for identifying and flagging known personal information in large language model outputs.
author: PatrickFarley
ms.author: pafarley
ms.date: 05/12/2025
ms.topic: conceptual
ms.service: azure-ai-openai
---

# Personally identifiable information (PII) filter

Personally identifiable information (PII) refers to any information that can be used to identify a particular individual, such as a name, address, phone number, email address, social security number, driver's license number, passport number, or similar information.

PII detection is used to prevent PII from being exposed or shared, protecting users from identity theft, financial fraud, or other types of privacy violations.

In the context of large language models (LLMs), PII detection involves analyzing text content in LLM completions. When PII has been identified, it can be flagged for further review, or the output can be blocked. The PII filter scans the output of LLMs to identify and flag known personal information. It's designed to help organizations prevent the generation of content that closely matches sensitive personal information.


## PII types

There are many different types of PII, and you can specify which types you want to filter. The set of PII types that can be detected by the filter matches the set that's defined in the [Azure AI Language docs](/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories).

## Filtering modes

The PII filter can be configured to operate in two modes. **Annotate** mode flags PII that's returned in the model output. **Annotate Block** mode blocks the entire output if PII is detected. The filtering mode is a global setting: it applies to all selected PII types.
