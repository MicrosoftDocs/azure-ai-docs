---
title: Foundry Local on Windows Server 2025 - Frequently asked questions
description: "Foundry Local FAQ: Learn about its supported Windows Server versions, GPU compatibility, and how it handles inference requests in GPU-P environments."
#customer intent: As a developer, I want to know if Foundry Local is a Windows component, app, or service so that I can plan its deployment.
author: jonburchel
ms.author: jburchel
ms.reviewer: maanavdalal
ms.date: 02/02/2026
ms.topic: concept-article
ms.service: azure-ai-foundry
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Foundry Local on Windows Server 2025

Foundry Local on Windows Server 2025 lets you run selected Microsoft Foundry model capabilities entirely on a single Windows Server machine you operate.

## Prerequisites

Before you begin, ensure you have:

- **Operating system**: Windows Server 2025 Datacenter or Windows Server 2025 Standard
- **GPU (optional)**: GPU-P VM for CUDA acceleration (Foundry Local auto-detects and selects the appropriate execution provider)

### Install Foundry Local

Open a terminal and run:

```bash
winget install Microsoft.FoundryLocal
```

### Verify the installation

Confirm Foundry Local is installed:

```bash
foundry --version
```

You see the installed version number.

### Run your first model

Start a model to verify end-to-end functionality:

```bash
foundry model run qwen2.5-0.5b
```

Foundry Local downloads the model (first run) and starts an interactive prompt. Type a question like "Why is the sky blue?" to confirm the model responds.

Reference: [Foundry Local CLI reference](reference-cli.md)

## Frequently asked questions

- **Is Foundry Local a Windows component, an app, or a service?**

  Foundry Local runs as a service on a Windows Server machine. Install it by using winget (see [Prerequisites](#prerequisites)).

- **Which versions of Windows Server support Foundry Local?**

  - Windows Server 2025 Datacenter
  - Windows Server 2025 Standard

- **Does Foundry Local run on virtual machines with GPU-P?**

  Foundry Local detects the partitioned GPU inside a GPU-P VM and picks up a CUDA-enabled model when one is available. Otherwise, it falls back appropriately. The execution provider is also automatically selected based on the availability of GPU inside the VM.

- **What are the concurrency limitations of Foundry Local on server?**

  Foundry Local isn't optimized to serve multiple users as a shared on-premises endpoint and doesn't support concurrent inference requests. It processes requests sequentially. You must manage parallel execution across multiple endpoints at the application level. As concurrent requests increase, throughput drops and latency increases. There's no continuous batching in the Local runtime, so request coalescing doesn't happen under load. For multiple users or spiky traffic, move to [Microsoft Foundry](../../index.yml).

- **How is the Foundry Local SDK different from the Foundry Local service?**

  The [Foundry Local SDK](reference-sdk.md) is a development toolkit to build software or applications by using the Foundry Local service without using the Foundry Local CLI or REST APIs directly.

- **How does Foundry Local differ from Microsoft Foundry?**

  | **Capability** | **Foundry Local (on server)** | **Foundry (cloud)** |
  |----|----|----|
  | Model catalog | Local catalog is smaller, BYOM possible. Embeddings models aren't yet available in the Local catalog. | Broad catalog, including embeddings in the service; managed updates, evaluation, safety tools, and agent services. |
  | Scale & HA | Single node runtime. No built-in autoscale or multinode distribution. | Managed scale, multiregional options, HA/DR patterns, and platform governance. Best for high concurrency and bursting. |
  | Concurrency / throughput | Limited; throughput declines as concurrent clients grow. No continuous batching today. | Cloud scale and load distribution; platform services for concurrency and throughput. |
  | APIs | OpenAI-compatible REST surface for chat/completions; MCP integration possible. | Full Foundry APIs, Responses API, Agent Service, eval, and integration with dev tools. |
  | Operations | You operate it like any server app: install, secure, monitor, back up; manage model bits locally. | Enterprise governance, cost controls, environments, RBAC/Networking, evaluation, and integrated DevOps. |

## Sample code

The [ContosoMedical sample](https://github.com/microsoft/foundry-local-on-windowsserver-samples) demonstrates a medical report summarizer and translator using Foundry Local on Windows Server. The sample shows how to:

- Connect to Foundry Local endpoints over the network
- Use the OpenAI-compatible API for chat completions
- Process long medical records using map-reduce summarization

The following excerpt shows how the sample sends requests to the Foundry Local endpoint:

```csharp
var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(300) };
var endpoint = configurationManager.GetAppSetting("FoundryLocalEndPoint1");

var requestBody = new
{
    model = configurationManager.GetAppSetting("FoundryLocalLanguageModel"),
    messages = new[]
    {
        new { role = "system", content = "You are a medical summarization assistant..." },
        new { role = "user", content = "Summarize this medical record section..." }
    },
    max_tokens = 200,
    temperature = 0.0
};

var response = await httpClient.PostAsync(endpoint + "/v1/chat/completions", content);
```

Reference: [Foundry Local REST API reference](reference-rest.md)

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Foundry Local architecture](../concepts/foundry-local-architecture.md)