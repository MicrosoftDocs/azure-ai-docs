---
title: Use Content Understanding with MarkItDown
titleSuffix: Foundry Tools
description: Learn how to configure MarkItDown to use Azure Content Understanding for Markdown conversion and optional structured field extraction.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 07/16/2026
ms.service: azure-content-understanding-foundry-tools
ms.topic: how-to
ai-usage: ai-assisted
---

# Use Content Understanding with MarkItDown

[MarkItDown](https://github.com/microsoft/markitdown) is an open-source Python utility that converts files to Markdown for large language model (LLM) and text analysis pipelines.

Configure the Azure Content Understanding in Foundry Tools backend to process supported documents, images, audio, and video through Content Understanding. The result can include layout-aware Markdown and structured fields serialized as YAML front matter.

## Prerequisites

- An Azure subscription. You can [create a free Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account).
- A Microsoft Foundry resource with Content Understanding configured. See [Create a Microsoft Foundry resource](../how-to/create-multi-service-resource.md) for setup instructions. Copy the endpoint URL from your resource.
- Python 3.10 or later.

## When to use the Content Understanding backend

Use the Content Understanding backend for the following scenarios:

- **Audio and video files.** Content Understanding provides video analysis and cloud-based audio transcription through MarkItDown.
- **Structured field extraction.** [Prebuilt](../concepts/prebuilt-analyzers.md) or [custom](../how-to/customize-analyzer-content-understanding-studio.md) analyzers extract domain-specific fields, such as invoice amounts, receipt dates, and contract clauses, serialized as YAML front matter.
- **Document extraction.** Cloud-based layout analysis and optical character recognition (OCR) process scanned PDFs, complex tables, and multipage documents.
- **A single API for all modalities.** One endpoint handles documents, images, audio, and video with automatic analyzer routing.

The following table compares the extraction backends that MarkItDown supports:

| Capability | Built-in converters | Azure Document Intelligence | Azure Content Understanding |
|------------|---------------------|-----------------------------|-----------------------------|
| Document conversion | Offline, format-specific extraction | Cloud layout extraction | Cloud multimodal extraction |
| Structured fields | Not available | Not exposed by this integration | YAML front matter from analyzer fields |
| Custom analyzers | Not available | Not configurable in this integration | Supported with `cu_analyzer_id` |
| Audio and video | Basic audio, no video | Not supported | Audio and video analyzers |
| Cost | Local compute only | Billable Azure API calls | Billable Azure API calls |

## Install MarkItDown with Content Understanding support

Install MarkItDown with the Content Understanding optional dependency:

```bash
pip install 'markitdown[az-content-understanding]'
```

## Convert a file from the command line

Pass the `--use-cu` flag and your resource endpoint to convert a file through Content Understanding:

```bash
markitdown path-to-file.pdf --use-cu \
  --cu-endpoint "<content_understanding_endpoint>"
```

## Convert a file in Python

Set `cu_endpoint` when you create the `MarkItDown` object. MarkItDown auto-selects an analyzer for each file type:

```python
from markitdown import MarkItDown

# Zero-config: auto-selects an analyzer per file type.
md = MarkItDown(cu_endpoint="<content_understanding_endpoint>")
result = md.convert("report.pdf")   # Uses prebuilt-documentSearch.
result = md.convert("meeting.mp4")  # Uses prebuilt-videoSearch.
result = md.convert("call.wav")     # Uses prebuilt-audioSearch.
print(result.markdown)
```

### Extract structured fields with a custom analyzer

To extract domain-specific fields, set `cu_analyzer_id` to a custom analyzer. The extracted fields appear as YAML front matter above the Markdown:

```python
from markitdown import MarkItDown

md = MarkItDown(
    cu_endpoint="<content_understanding_endpoint>",
    cu_analyzer_id="my-invoice-analyzer",
)
result = md.convert("invoice.pdf")
print(result.markdown)
# ---
# contentType: document
# fields:
#   VendorName: CONTOSO LTD.
#   InvoiceDate: '2019-11-15'
# ---
# <!-- page 1 -->
# ...
```

When you set `cu_analyzer_id`, the converter scopes the analyzer to compatible file types based on its modality. Incompatible types, such as audio files with a document analyzer, route to the default prebuilt analyzers instead.

## Control cost

Each `convert()` call for a Content Understanding-routed format is a billable Azure API call. Use `cu_file_types` to restrict which formats route to Content Understanding.

```python
from markitdown import MarkItDown
from markitdown.converters import ContentUnderstandingFileType

md = MarkItDown(
    cu_endpoint="<content_understanding_endpoint>",
    # Only PDFs use Content Understanding.
    cu_file_types=[ContentUnderstandingFileType.PDF],
)
```

## Next steps

- [MarkItDown on GitHub](https://github.com/microsoft/markitdown#azure-content-understanding).
- [Explore prebuilt analyzers](../concepts/prebuilt-analyzers.md).
- [Build a retrieval-augmented generation solution](../tutorial/build-rag-solution.md).
