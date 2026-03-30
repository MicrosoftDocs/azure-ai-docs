---
title: Include file
description: Include file
author: ms-johnalex
ms.reviewer: dantaylo
ms.author: johalexander
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

A Foundry resource provides unified access to models, agents, and tools. This article explains which SDK and endpoint to use for your scenario.

| SDK | What it's for | Endpoint |
| --- | --- | --- |
| **Foundry SDK** | Foundry-specific capabilities with OpenAI-compatible interfaces. Includes access to Foundry direct models through the Responses API (not Chat Completions). | `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>` |
| **OpenAI SDK** | Latest OpenAI SDK models and features with the full OpenAI API surface. Foundry direct models available through Chat Completions API (not Responses). | `https://<resource-name>.openai.azure.com/openai/v1` |
| **Foundry Tools SDKs** | Prebuilt solutions (Vision, Speech, Content Safety, and more). | Tool-specific endpoints (varies by service). |
| **Agent Framework** | Multi-agent orchestration in code. Cloud-agnostic. | Uses the project endpoint via the Foundry SDK. |

**Choose your SDK**:
- Use **Foundry SDK** when building apps with agents, evaluations, or Foundry-specific features
- Use **OpenAI SDK** when maximum OpenAI compatibility is required, or using Foundry direct models via Chat Completions
- Use **Foundry Tools SDKs** when working with specific AI services (Vision, Speech, Language, etc.)
- Use **Agent Framework** when building multi-agent systems in code (local orchestration)

> [!NOTE]
> **Resource types:** A Foundry resource provides all endpoints previously listed. An Azure OpenAI resource provides only the `/openai/v1` endpoint.
>
> **Authentication:** Samples here use Microsoft Entra ID (`DefaultAzureCredential`). API keys work on `/openai/v1`. Pass the key as `api_key` instead of a token provider.

## Prerequisites

- [!INCLUDE [azure-subscription](azure-subscription.md)]

- Have one of the following Azure RBAC roles to create and manage Foundry resources:
  - **Azure AI User** (least-privilege role for development)
  - **Azure AI Project Manager** (for managing Foundry projects)
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
- Language runtime installed:
  - Python: `python --version` (≥3.8)
  - Node.js: `node --version` (≥18)
  - .NET: `dotnet --version` (≥6.0)
  - Java: `java --version` (≥11)
