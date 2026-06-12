---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: dantaylo
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

A Foundry resource provides unified access to models, agents, and tools. This article explains which SDK and endpoint to use for your scenario.

The **Foundry SDK** is a thin-client SDK that exposes all of the Foundry project APIs through a single project endpoint. Higher-level SDKs build on it — for example, the Agent Framework `foundry` package depends on the Foundry SDK to access Foundry models, tools, and project configuration.

| SDK | What it's for | Endpoint |
| --- | --- | --- |
| **Foundry SDK** | Thin-client SDK over all Foundry project APIs. Access to Foundry Models and platform tools (file search, code interpreter, web search, memory, SharePoint, WorkIQ, Fabric IQ, MCP). | `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>` |
| **Agent Framework** | Hosted agents and multi-agent systems build using code. The `foundry` package depends on the Foundry SDK for project access. Run in your own process. | Responses API in the project endpoint, via `FoundryChatClient`. |
| **OpenAI SDK** | Full OpenAI API surface, including embeddings. Best latency and maximum OpenAI compatibility. | `https://<resource-name>.openai.azure.com/openai/v1` |
| **Anthropic SDK** | Anthropic Claude models deployed in Foundry. | `https://<resource-name>.services.ai.azure.com/anthropic` |
| **Foundry Tools SDKs** | Prebuilt solutions (Vision, Speech, Content Safety, and more). | Tool-specific endpoints. |

**Choose your SDK**:
- Use **Foundry SDK** when building apps with agents, evaluations, or Foundry-specific features
- Use **Agent Framework** when building hosted agents or multi-agent systems in code using the Responses API
- Use **OpenAI SDK** when maximum OpenAI compatibility or lowest latency is required, when generating embeddings, or when using Foundry direct models via Chat Completions
- Use **Anthropic SDK** when working with Anthropic Claude models deployed in Foundry
- Use **Foundry Tools SDKs** when working with specific AI services (Vision, Speech, Language, etc.)

> [!NOTE]
> **Resource types:** A Foundry resource provides all endpoints previously listed. An Azure OpenAI resource provides only the `/openai/v1` endpoint.
>
> **Authentication:** Samples here use Microsoft Entra ID (`DefaultAzureCredential`). API keys work on `/openai/v1`. Pass the key as `api_key` instead of a token provider.

## Prerequisites

- [!INCLUDE [azure-subscription](azure-subscription.md)]

- Have one of the following Azure RBAC roles to create and manage Foundry resources:
  - **Foundry User** (least-privilege role for development)

    [!INCLUDE [role-rename-note](./role-rename-note.md)]
  - **Foundry Project Manager** (for managing Foundry projects)
  - **Contributor** or **Owner** (for subscription-level permissions)
  
  For details on each role's permissions, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

- Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../how-to/develop/install-cli-sdk.md).

> [!IMPORTANT]
> Before starting, make sure your development environment is ready.  
> This article focuses on **scenario-specific steps** like SDK installation, authentication, and running sample code.
>

### Verify prerequisites

Before proceeding, confirm:

- Azure subscription is active: `az account show`
- You have the required RBAC role: Check Azure portal → Foundry resource → Access control (IAM)
::: zone pivot="programming-language-python"
- Language runtime installed:
  - Python: `python --version` (≥3.8)
::: zone-end
::: zone pivot="programming-language-javascript"
- Language runtime installed:
  - Node.js: `node --version` (≥18)
::: zone-end
::: zone pivot="programming-language-csharp"
- Language runtime installed:
  - .NET: `dotnet --version` (≥6.0)
::: zone-end
::: zone pivot="programming-language-java"
- Language runtime installed:
  - Java: `java --version` (≥11)
::: zone-end
