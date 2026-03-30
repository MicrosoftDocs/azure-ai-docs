---
title: Include file
description: Include file
author: msakande
ms.reviewer: ambadal
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Best practices

Follow these best practices when working with Claude models in Foundry:

### Model selection

Choose the appropriate Claude model based on your specific requirements:

- **Claude Opus 4.6**: Most intelligent model for building agents, coding, and enterprise workflows.
- **Claude Opus 4.5**: Best performance across coding, agents, computer use, and enterprise workflows.
- **Claude Opus 4.1**: Complex reasoning and enterprise applications.
- **Claude Sonnet 4.6**: Frontier intelligence at scale for coding, agents, and most use cases.
- **Claude Sonnet 4.5**: Balanced performance and capabilities, production workflows.
- **Claude Haiku 4.5**: Speed and cost optimization, high-volume processing.

### Prompt engineering

- **Clear instructions**: Provide specific and detailed prompts.
- **Context management**: Use the available context window effectively.
- **Role definitions**: Use system messages to define the assistant's role and behavior.
- **Structured prompts**: Use consistent formatting for better results.

### Cost optimization

- **Token management**: Monitor and optimize token usage.
- **Model selection**: Use the most cost-effective model for your use case.
- **Caching**: Implement [explicit prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching#continuing-a-multi-turn-conversation) where appropriate.
- **Request batching**: Combine multiple requests when possible.

## Troubleshooting

The following table lists common errors when you work with Claude models in Foundry and their solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or expired API key, or incorrect Entra ID token scope. | Verify your API key is correct. For Entra ID, confirm you use scope `https://ai.azure.com/.default`. |
| 403 Forbidden | Insufficient permissions on the resource or subscription. | Verify you have **Contributor** or **Owner** role on the resource group. For Entra ID, ensure the **Cognitive Services User** role is assigned. |
| 404 Not Found | Incorrect endpoint URL or deployment name. | Confirm your base URL follows the pattern `https://<resource-name>.services.ai.azure.com/anthropic` and the deployment name matches your configuration. |
| 429 Too Many Requests | Rate limit exceeded for your subscription tier. | Implement exponential backoff with retry logic. Consider reducing request frequency or requesting a [quota increase](https://aka.ms/oai/stuquotarequest). |
| Subscription eligibility error | Non-Enterprise or non-MCA-E subscription. | Claude models require an Enterprise or MCA-E subscription. See [API quotas and limits](#api-quotas-and-limits) for details. |
| Region not available | Deployment attempted in an unsupported region. | Deploy to **East US2** or **Sweden Central**, the supported regions for Claude models. |

## Related content

- [Data, privacy, and security for Claude models in Microsoft Foundry (preview)](../../responsible-ai/claude-models/data-privacy.md)
- [Monitor model usage and costs](../../../foundry-classic/how-to/costs-plan-manage.md)
- [How to generate text responses with Microsoft Foundry Models](../how-to/generate-responses.md)
- [Explore Microsoft Foundry Models](../../../foundry-classic/concepts/foundry-models-overview.md)
- [Claude Docs: Claude in Microsoft Foundry](https://docs.claude.com/en/docs/build-with-claude/claude-in-microsoft-foundry)
