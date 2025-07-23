---
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 07/23/2025
---

> [!IMPORTANT]
> Starting in May 2025, the Azure AI Agent Service uses an endpoint for [Foundry projects](../../what-is-azure-ai-foundry.md#project-types) instead of the connection string that were used for hub-based projects before this time. Connection strings are no longer supported in current versions of the SDKs and REST API. We recommend creating a new foundry project.
>
> If you want to continue using your hub-based project and connection string, you will need to: 
> 1. Use the connection string for your project located under **Connection string** in the overview of your project. 
>
>    :::image type="content" source="../../media/quickstarts/azure-ai-sdk/connection-string.png" alt-text="A screenshot showing the legacy connection string for a hub-based project.":::
>
> 2. Use one of the previous versions of the SDK and the associated sample code:
>     * [C#](https://github.com/Azure/azure-sdk-for-net/tree/feature/azure-ai-agents/sdk/ai/Azure.AI.Projects/samples): `1.0.0-beta.2` or earlier
>     * [Python](https://github.com/Azure/azure-sdk-for-python/tree/feature/azure-ai-projects-beta10/sdk/ai/azure-ai-projects/samples/agents): `1.0.0b10` or earlier
