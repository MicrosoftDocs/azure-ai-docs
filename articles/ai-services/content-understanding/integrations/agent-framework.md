---
title: Use Content Understanding with the Microsoft Agent Framework
titleSuffix: Foundry Tools
description: Learn how to use Azure Content Understanding as a Microsoft Agent Framework context provider to analyze file attachments in agent conversations.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.date: 07/16/2026
ms.service: azure-content-understanding-foundry-tools
ms.topic: how-to
ai-usage: ai-assisted
---

# Use Content Understanding with the Microsoft Agent Framework

The Azure Content Understanding in Foundry Tools integration for the [Microsoft Agent Framework](/agent-framework/overview/) provides a context provider for file attachments. The provider detects supported documents, images, audio, and video in agent input, analyzes the files, and adds Markdown and extracted fields to the model context.

## Prerequisites

- An Azure subscription. You can [create a free Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account).
- A Microsoft Foundry resource with Content Understanding configured. See [Create a Microsoft Foundry resource](../how-to/create-multi-service-resource.md) for setup instructions. Confirm your resource is in a [supported region](../language-region-support.md).
- Default model deployments configured for your resource. See [Foundry model deployments](../concepts/models-deployments.md).
- Python 3.10 or later.
- Sign in with the Azure CLI (`az login`) so the sample can authenticate with `AzureCliCredential`.

## Why use this integration

- **Automatic attachment processing.** The framework calls the provider before each model invocation, so you don't call the analyzer directly.
- **Multimodal input.** The provider accepts documents, images, audio, and video.
- **Structured output.** The provider can add Markdown and extracted fields to the model context.
- **Deferred processing.** A configurable wait time allows long-running analyses to continue in the background. Optional file search support uploads extracted Markdown to a vector store for retrieval-augmented generation (RAG).

## Install the package

Install the Content Understanding integration package for the Microsoft Agent Framework. The integration ships in the [`agent-framework-azure-contentunderstanding` package](https://github.com/microsoft/agent-framework/tree/main/python/packages/azure-contentunderstanding), which is also available on [PyPI](https://pypi.org/project/agent-framework-azure-contentunderstanding/):

```bash
pip install agent-framework-azure-contentunderstanding --pre
```

> [!NOTE]
> The `--pre` flag installs the current prerelease build of the package.

## Register Content Understanding as a context provider

Create a `ContentUnderstandingContextProvider`, pass it to your agent through the `context_providers` parameter, and run the agent inside the provider's `async with` block. The following example answers a question about an attached document:

```python
import asyncio
from agent_framework import Agent, AgentSession, Message, Content
from agent_framework.foundry import FoundryChatClient
from agent_framework.foundry import ContentUnderstandingContextProvider
from azure.identity import AzureCliCredential

credential = AzureCliCredential()

cu = ContentUnderstandingContextProvider(
    endpoint="https://my-resource.cognitiveservices.azure.com/",
    credential=credential,
    # Block until analysis completes before sending to the model.
    max_wait=None,
)

client = FoundryChatClient(
    project_endpoint="https://your-project.services.ai.azure.com",
    model="gpt-5.2",
    credential=credential,
)

async def main():
    async with cu:
        agent = Agent(
            client=client,
            name="DocumentQA",
            instructions="You are a helpful document analyst.",
            context_providers=[cu],
        )
        session = AgentSession()

        response = await agent.run(
            Message(role="user", contents=[
                Content.from_text("What's on this invoice?"),
                Content.from_uri(
                    "https://raw.githubusercontent.com/Azure-Samples/"
                    "azure-ai-content-understanding-assets/main/"
                    "document/invoice.pdf",
                    media_type="application/pdf",
                    additional_properties={"filename": "invoice.pdf"},
                ),
            ]),
            session=session,
        )
        print(response.text)

asyncio.run(main())
```

Before each model invocation, the framework calls the provider. The provider detects and analyzes supported attachments, so you don't invoke the analyzer directly.

## Configure the provider

Pass additional parameters to select an analyzer and control how much content the provider returns:

| Parameter | Purpose |
|-----------|---------|
| `endpoint` | The endpoint of your Microsoft Foundry resource. If omitted, the provider reads it from the `AZURE_CONTENTUNDERSTANDING_ENDPOINT` environment variable. |
| `credential` | An `AzureKeyCredential` for API key authentication, or an Azure identity credential, such as `AzureCliCredential` or `DefaultAzureCredential`, for Microsoft Entra ID authentication. |
| `analyzer_id` | A prebuilt or custom analyzer ID. If you omit this parameter, the provider selects `prebuilt-documentSearch` for documents and images, `prebuilt-audioSearch` for audio, and `prebuilt-videoSearch` for video. |
| `max_wait` | How many seconds to wait before deferring analysis to the background. The default is 5 seconds. Set it to `None` to wait until analysis completes. |
| `output_sections` | Which result sections to add to the model context. The default sections are Markdown and fields. |
| `file_search` | Optional configuration for uploading extracted Markdown to a vector store instead of adding the full content to the model context. |

> [!TIP]
> For domain-specific extraction, set `analyzer_id` to a prebuilt or custom analyzer ID. The provider then adds the analyzer's fields to the model context.

## Supported file types

The provider accepts documents, images, audio, and video. For the complete list of supported formats and size limits, see [Content Understanding service quotas and limits](../service-limits.md).

## Next steps

- [Azure Content Understanding for the Microsoft Agent Framework (GitHub)](https://github.com/microsoft/agent-framework/tree/main/python/packages/azure-contentunderstanding).
- [Explore prebuilt analyzers](../concepts/prebuilt-analyzers.md).
- [Build a retrieval-augmented generation solution](../tutorial/build-rag-solution.md).
