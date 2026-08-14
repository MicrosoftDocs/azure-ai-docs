---
title: Use Content Understanding with LangChain
titleSuffix: Foundry Tools
description: Learn how to use the Azure Content Understanding loader for LangChain to create Document objects from documents, images, audio, and video.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 07/16/2026
ms.service: azure-content-understanding-foundry-tools
ms.topic: how-to
ai-usage: ai-assisted
---

# Use Content Understanding with LangChain

The Azure Content Understanding in Foundry Tools document loader for [LangChain](/azure/foundry/how-to/develop/langchain) analyzes documents, images, audio, and video. It returns LangChain `Document` objects whose `page_content` contains Markdown and whose `metadata` can include analyzer information, extracted fields, confidence scores, and source information.

## Prerequisites

- An Azure subscription. You can [create a free Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account).
- A Microsoft Foundry resource with Content Understanding configured. See [Create a Microsoft Foundry resource](../how-to/create-multi-service-resource.md) for setup instructions. Copy the endpoint URL from your resource.
- Default model deployments configured for your resource. See [Foundry model deployments](../concepts/models-deployments.md).
- Python 3.10 or later.
- Authentication credentials, either a Microsoft Entra ID identity, such as `DefaultAzureCredential`, or an API key.

## Why use this integration

- **LangChain output.** The loader returns standard `Document` objects for use with LangChain components.
- **Multimodal input.** You can load documents, images, audio, and video through one loader, with an analyzer selected by file type.
- **Markdown content.** The `page_content` can preserve document structures such as tables and headings.
- **Structured fields.** Prebuilt or custom analyzers can add extracted fields and confidence scores to document metadata.
- **Input options.** Load from a local file path, a URL, or raw bytes.

## Install the package

The loader ships in the [`langchain-azure-ai`](https://github.com/langchain-ai/langchain-azure/tree/main/libs/azure-ai/langchain_azure_ai/document_loaders) package:

```bash
pip install -U langchain-azure-ai
```

## Load a document

Create an `AzureAIContentUnderstandingLoader`, provide your endpoint and credential, and point it at exactly one input source (`file_path`, `url`, or `bytes_source`). Call `load()` to get LangChain `Document` objects:

```python
from azure.identity import DefaultAzureCredential
from langchain_azure_ai.document_loaders import (
    AzureAIContentUnderstandingLoader,
)

loader = AzureAIContentUnderstandingLoader(
    endpoint="https://my-resource.services.ai.azure.com/",
    credential=DefaultAzureCredential(),
    file_path="report.pdf",
)
docs = loader.load()

print(docs[0].page_content)          # Markdown with preserved layout.
print(docs[0].metadata["analyzer_id"])
```

When you don't set `analyzer_id`, the loader auto-selects a prebuilt analyzer based on the file's modality: `prebuilt-documentSearch` for documents and images, `prebuilt-audioSearch` for audio, and `prebuilt-videoSearch` for video.

> [!TIP]
> For asynchronous pipelines, call `await loader.aload()` instead of `load()`.

## Extract structured fields

To extract domain-specific fields, set `analyzer_id` to a [prebuilt analyzer](../concepts/prebuilt-analyzers.md), such as `prebuilt-invoice`, or your own custom analyzer ID. Domain-specific analyzers require `model_deployments` to map model names to your deployments. The extracted fields appear in each document's `metadata["fields"]` with confidence scores:

```python
from azure.identity import DefaultAzureCredential
from langchain_azure_ai.document_loaders import (
    AzureAIContentUnderstandingLoader,
)

loader = AzureAIContentUnderstandingLoader(
    endpoint="https://my-resource.services.ai.azure.com/",
    credential=DefaultAzureCredential(),
    analyzer_id="prebuilt-invoice",       # Or your custom analyzer ID.
    file_path="invoice.pdf",
    model_deployments={"gpt-4.1": "gpt-4.1"},
)
docs = loader.load()

for name, data in docs[0].metadata.get("fields", {}).items():
    if isinstance(data, dict):
        print(name, data.get("value"), data.get("confidence"))
```

## Control how results map to documents

Use `output_mode` to choose how Content Understanding results become LangChain `Document` objects:

| `output_mode` | Result |
|---------------|--------|
| `markdown` (default) | One document per content item, with the full Markdown text. |
| `page` | One document per page, with document content only. |
| `segment` | One document per content segment. Requires a custom analyzer with segmentation enabled, and is supported for document and video analyzers only. |

To analyze only part of the input, set `content_range`. Pages use 1-based numbers, such as `"1-3,5,9-"`. Audio and video use milliseconds, such as `"0-60000"`.

## Supported file types

The loader accepts documents, images, audio, and video. For the complete list of supported formats and size limits, see [Content Understanding service quotas and limits](../service-limits.md).

## Next steps

- [Azure Content Understanding document loader for LangChain (GitHub)](https://github.com/langchain-ai/langchain-azure/tree/main/libs/azure-ai/langchain_azure_ai/document_loaders).
- [Explore prebuilt analyzers](../concepts/prebuilt-analyzers.md).
- [Build a retrieval-augmented generation solution](../tutorial/build-rag-solution.md).
