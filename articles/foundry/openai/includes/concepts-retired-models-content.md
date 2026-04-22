---
title: include file
description: include file
author: mrbullwinkle
ms.author: mbullwin
ms.reviewer: josander
reviewer: johnrsanders
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/23/2026
ms.custom: include, classic-and-new
---

Microsoft Foundry offers a variety of models for different use cases. The following models are retired and no longer available for use or for new deployments.

## Azure OpenAI


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
| `dall-e-2`|  | January 27, 2025 | `gpt-image-1` |
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


## AI21 Labs

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| Jamba Instruct | March 1, 2025 | N/A |
| AI21-Jamba-1.5-Large | August 1, 2025 | N/A |
| AI21-Jamba-1.5-Mini | August 1, 2025 | N/A |

## Bria

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| Bria-2.3-Fast | October 31, 2025 | N/A |

## Cohere

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| Command R | June 30, 2025 | `Cohere-command-r-08-2024` |
| Command R+ | June 30, 2025 | `Cohere-command-r-plus-08-2024` |
| Cohere-rerank-v3-english | June 30, 2025 | `Cohere-rerank-v4.0-pro`, `Cohere-rerank-v4.0-fast` |
| Cohere-rerank-v3-multilingual | June 30, 2025 | `Cohere-rerank-v4.0-pro`, `Cohere-rerank-v4.0-fast` |

## Core42

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| jais-30b-chat | January 30, 2026 | N/A |

## DeepSeek

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| DeepSeek-V3 | August 31, 2025 | `DeepSeek-V3-0324` |

## Gretel

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| Gretel-Navigator-Tabular | September 16, 2025 | N/A |

## Meta

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| Llama-2-13b | June 30, 2025 | `Meta-Llama-3.1-8B-Instruct` |
| Llama-2-13b-chat | June 30, 2025 | `Meta-Llama-3.1-8B-Instruct` |
| Llama-2-70b | June 30, 2025 | `Llama-3.3-70B-Instruct` |
| Llama-2-70b-chat | June 30, 2025 | `Llama-3.3-70B-Instruct` |
| Llama-2-7b | June 30, 2025 | `Meta-Llama-3.1-8B-Instruct` |
| Llama-2-7b-chat | June 30, 2025 | `Meta-Llama-3.1-8B-Instruct` |
| Meta-Llama-3-70B-Instruct | June 30, 2025 | `Llama-3.3-70B-Instruct` |
| Meta-Llama-3-8B-Instruct | June 30, 2025 | `Meta-Llama-3.1-8B-Instruct` |
| Meta-Llama-3.1-70B-Instruct | June 30, 2025 | `Llama-3.3-70B-Instruct` |

## Microsoft

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| MAI-DS-R1 | February 27, 2026 | Any DeepSeek model available in the Model catalog |
| Phi-3-medium-4k-instruct | August 30, 2025 | `Phi-4` |
| Phi-3-medium-128k-instruct | August 30, 2025 | `Phi-4` |
| Phi-3-mini-4k-instruct | August 30, 2025 | `Phi-4-mini-instruct` |
| Phi-3-mini-128k-instruct | August 30, 2025 | `Phi-4-mini-instruct` |
| Phi-3-small-8k-instruct | August 30, 2025 | `Phi-4-mini-instruct` |
| Phi-3-small-128k-instruct | August 30, 2025 | `Phi-4-mini-instruct` |
| Phi-3.5-mini-instruct | August 30, 2025 | `Phi-4-mini-instruct` |
| Phi-3.5-MoE-instruct | August 30, 2025 | `Phi-4-mini-instruct` |
| Phi-3.5-vision-instruct | August 30, 2025 | `Phi-4-mini-instruct` |

## Mistral AI

| Model | Retirement date | Suggested replacement |
|-------|-----------------------|-----------------------------|
| Mistral-Nemo | January 30, 2026 | `Mistral-small-2503` |
| Mistral-large-2411 | January 30, 2026 | `Mistral-medium-2505` |
| Mistral-ocr-2503 | January 30, 2026 | `Mistral-document-ai-2505` |
| Mistral-small | July 31, 2025 | `Mistral-small-2503` |
| Mistral-large-2407 | May 13, 2025 | `Mistral-medium-2505` |
| Mistral-large | April 15, 2025 | `Mistral-medium-2505` |

## Moonshot AI

| Model | Retirement date | Suggested replacement  |
|-------|-----------------------|-----------------------------|
| Kimi-k2-thinking | March 29, 2026 | `Kimi-K2.5` |