---
title: Retired Azure OpenAI models
titleSuffix: Azure OpenAI
description: Learn about retired models in Azure OpenAI.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 02/12/2026
ms.custom: references_regions, build-2023, build-2023-dataai
manager: nitinme
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Retired Azure OpenAI models

Azure OpenAI offers a variety of models for different use cases. The following models are no longer available for deployment.

For current model availability and lifecycle policy, see [Model deprecations and retirements](model-retirements.md).

> [!NOTE]
> - **Deprecation**: When a model is deprecated, it's no longer available for new customers. It continues to be available for use by customers who have existing deployments until the model is retired.
> - **Retirement**: When a model is retired, it's no longer available for use. Azure OpenAI deployments of a retired model always return error responses.
>
> Not all models go through a deprecation period before retirement. Some models or versions only have a retirement date.

## Retired models

These models are retired and are no longer available for use or for new deployments.

| Model | Deprecation date | Retirement date | Suggested replacement |
| --------- | --------------------- | ------------------- | -------------------- |
| `o1-preview`  | |  July 28, 2025                       | `o1`                                 |
| `gpt-4.5-preview`         |       |  July 14, 2025 | `gpt-4.1` version: `2025-04-14`      |
| `gpt-4o-realtime-preview` - `2024-10-01` | February 25, 2025 | March 26, 2025 | `gpt-4o-realtime-preview` (version 2024-12-17) or `gpt-4o-mini-realtime-preview` (version 2024-12-17) |
| `gpt-35-turbo` - 0301 | | February 13, 2025   | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`  |
| `gpt-35-turbo` - 0613 | | February 13, 2025 | `gpt-35-turbo` (0125) <br><br> `gpt-4o-mini`  |
| `gpt-4`<br>`gpt-4-32k` - 0314 |         | June 6, 2025                       | `gpt-4o` version: `2024-11-20`       |
| `gpt-4`<br>`gpt-4-32k` - 0613 |         | June 6, 2025                       | `gpt-4o` version: `2024-11-20`       |
| `gpt-35-turbo-16k`     - 0613 |         | April  30, 2025                    | `gpt-4.1-mini` version: `2025-04-14` |
| `babbage-002` | | January 27, 2025 |  |
| `davinci-002` | | January 27, 2025 | |
| `dall-e-2`|  | January 27, 2025 | `dall-e-3` |
| `ada` | July 6, 2023 | June 14, 2024 |  |
| `babbage` | July 6, 2023 | June 14, 2024 |  |
| `curie` | July 6, 2023 | June 14, 2024 | |
| `davinci` | July 6, 2023 | June 14, 2024 |  |
| `text-ada-001` | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| `text-babbage-001` | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| `text-curie-001` | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| `text-davinci-002` | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| `text-davinci-003` | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| `code-cushman-001` | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| `code-davinci-002` | July 6, 2023 | June 14, 2024 | gpt-35-turbo-instruct |
| `text-similarity-ada-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-similarity-babbage-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-similarity-curie-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-similarity-davinci-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-search-ada-doc-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-search-ada-query-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-search-babbage-doc-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-search-babbage-query-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-search-curie-doc-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-search-curie-query-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-search-davinci-doc-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `text-search-davinci-query-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `code-search-ada-code-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `code-search-ada-text-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `code-search-babbage-code-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
| `code-search-babbage-text-001` | July 6, 2023 | June 14, 2024 | text-embedding-3-small |
