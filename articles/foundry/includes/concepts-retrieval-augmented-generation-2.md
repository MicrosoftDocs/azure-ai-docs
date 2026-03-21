---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Security and privacy considerations

RAG systems can expose sensitive content if you don't design access and prompting carefully.

- **Apply access control at retrieval time**. If you're using Azure AI Search as a data source, you can use document-level access control with security filters. See the [document-level access control](../../foundry-classic/openai/concepts/use-your-data.md#document-level-access-control) section.
- **Prefer Microsoft Entra ID over API keys for production**. API keys are convenient for development but aren't recommended for production scenarios. For Azure AI Search RBAC guidance, see [Connect to Azure AI Search using roles](../../search/search-security-rbac.md).
- **Treat retrieved content as untrusted input**. Your system message and application logic should reduce the risk of prompt injection from documents and retrieved passages. See [Safety system messages](../openai/concepts/system-message.md).

## Cost and latency considerations

RAG adds extra work compared to a model-only request:

- **Retrieval costs and latency**: Querying an index adds round trips and compute.
- **Embedding costs and latency**: Vector search requires embeddings at indexing time, and often at query time.
- **Token usage**: Retrieved passages increase input tokens, which can increase cost.

If you're using Azure AI Search, confirm service tier and pricing before production rollout. If you're using semantic or hybrid retrieval, review Azure AI Search pricing and limits in the Azure AI Search documentation.

## Limitations and troubleshooting

### Known limitations

- RAG quality depends on content preparation, retrieval configuration, and prompt design. Poor data preparation or indexing strategy directly impacts response quality.
- If retrieval returns irrelevant or incomplete passages, the model can still produce incomplete or inaccurate answers despite grounding.
- If you don't control access to source content, grounded responses can leak sensitive information from your index.

### Common challenges and mitigation

- **Poor retrieval quality**: If your index isn't returning relevant passages, review your data chunking strategy, embedding model quality, and search configuration (keyword vs. semantic vs. hybrid).
- **Hallucination despite grounding**: Even with retrieved content, models can still generate inaccurate responses. Enable citations and use clear system messages and prompts to instruct the model to stick to retrieved content.
- **Latency issues**: Large indexes can slow retrieval. Consider indexing strategy, filtering, and re-ranking to reduce the volume of passages processed.
- **Token budget exceeded**: Retrieved passages can quickly consume token limits. Implement passage filtering, ranking, or summarization to stay within budget.

For guidance on evaluating RAG effectiveness, see the tutorials and quickstarts in the related content section below.
