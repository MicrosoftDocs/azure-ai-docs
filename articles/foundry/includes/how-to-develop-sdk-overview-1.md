---
title: Explore Microsoft Foundry SDKs and endpoints
description: Learn how to choose among Microsoft Foundry, Agent Framework, OpenAI, Anthropic, and Foundry Tools SDKs and use the correct endpoint.
author: sdgilley
ms.reviewer: dantaylo
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include, doc-kit-assisted
ai-usage: ai-assisted
---

A Foundry resource provides unified access to models, agents, and tools. This article explains which SDK and endpoint to use for your scenario.

The **Foundry SDK** is a thin-client SDK that exposes all of the Foundry project APIs through a single project endpoint. Higher-level SDKs build on it — for example, the Agent Framework `foundry` package depends on the Foundry SDK to access Foundry models, tools, and project configuration.

| SDK | What it's for | Endpoint |
| --- | --- | --- |
| **Foundry SDK** | Thin-client SDK over all Foundry project APIs. Access to Foundry Models and platform tools (file search, code interpreter, web search, memory, SharePoint, WorkIQ, Fabric IQ, MCP). | `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>` |
| **Agent Framework** | Unified multi-agent orchestration for hosted agents and multi-agent systems, available in C#/.NET and Python. The `foundry` package depends on the Foundry SDK for project access. | Responses API in the project endpoint, via `FoundryChatClient`. |
| **OpenAI SDK** | Full OpenAI API surface, including embeddings and Foundry Models sold by Azure through Chat Completions. Best latency and maximum OpenAI compatibility. | `https://<resource-name>.openai.azure.com/openai/v1` |
| **Anthropic SDK** | Anthropic Claude models deployed in Foundry. | `https://<resource-name>.services.ai.azure.com/anthropic` |
| **Foundry Tools SDKs** | Prebuilt solutions (Vision, Speech, Content Safety, and more). | Tool-specific endpoints. |

**Choose your SDK**:
- Use **Foundry SDK** when building apps with agents, evaluations, or Foundry-specific features
- Use **Agent Framework** for hosted agents or multi-agent systems in code using the Responses API in C#/.NET or Python
- Use **OpenAI SDK** when maximum OpenAI compatibility or lowest latency is required, when generating embeddings, or when using Models sold by Azure through Chat Completions
- Use **Anthropic SDK** when working with Anthropic Claude models deployed in Foundry
- Use **Foundry Tools SDKs** when working with specific AI services (Vision, Speech, Language, etc.)

> [!NOTE]
> **Resource types:** A Foundry resource provides all endpoints previously listed. An Azure OpenAI resource provides only the `/openai/v1` endpoint.
>
> **Authentication:** Samples here use Microsoft Entra ID (`DefaultAzureCredential`). API keys work on `/openai/v1`. Pass the key as `api_key` instead of a token provider.

## Prerequisites

- [!INCLUDE [azure-subscription](azure-subscription.md)]

- Have the Azure RBAC role required for your task at the narrowest scope:
  - **Foundry User** on the Foundry project for day-to-day development.

    [!INCLUDE [role-rename-note](./role-rename-note.md)]
  - **Foundry Project Manager** on the Foundry project to manage an existing project and its connections.
  - **Foundry Account Owner** on the Foundry resource to create projects or manage account-level resources. Assign this role on the target resource group only when you need to create a Foundry resource.

    Activate the resource-group assignment just in time through Microsoft Entra Privileged Identity Management (PIM), and deactivate it after provisioning. Day-to-day developers and runtime users don't need this elevated assignment.
  
  For details on each role's permissions, see [Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

- Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../how-to/develop/install-cli-sdk.md).

### Verify prerequisites

Before proceeding, confirm each check returns the stated result:

- Confirm that the Azure CLI uses the intended subscription and tenant:

  ```azurecli
  az account show --query "{subscription:name, tenant:tenantId}" --output table
  ```

  The command exits successfully and displays the expected subscription and tenant.

- Confirm that your local credential can request a Foundry access token without displaying the token:

  ```azurecli
  az account get-access-token --resource https://ai.azure.com --query expiresOn --output tsv
  ```

  The command exits successfully and displays the token expiration time. If it fails, run `az login` with an identity that has the required Foundry role.

- Confirm that you have the required RBAC role in the Azure portal under **Foundry resource** > **Access control (IAM)**.
::: zone pivot="programming-language-python"
- Run `python --version`. The command exits successfully and reports Python 3.9 or later.
::: zone-end
::: zone pivot="programming-language-javascript"
- Run `node --version`. The command exits successfully and reports Node.js 22 or later.
::: zone-end
::: zone pivot="programming-language-csharp"
- Run `dotnet --version`. The command exits successfully and reports .NET 8 or later.
::: zone-end
::: zone pivot="programming-language-java"
- Run `java --version`. The command exits successfully and reports Java 17 or later.
::: zone-end

- Confirm that your project endpoint has this format:
  `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`.

- Confirm that the `gpt-5-mini` deployment is ready:

  ```azurecli
  az cognitiveservices account deployment show \
    --name <resource-name> \
    --resource-group <resource-group> \
    --deployment-name gpt-5-mini \
    --query properties.provisioningState \
    --output tsv
  ```

  The command returns `Succeeded`. Use the deployed name in the code examples if your deployment has a different name.
