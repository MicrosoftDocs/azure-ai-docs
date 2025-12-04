---
title: Foundry Local on Windows Server 2025 - Frequently asked questions
description: "Foundry Local FAQ: Learn about its supported Windows Server versions, GPU compatibility, and how it handles inference requests in GPU-P environments."
#customer intent: As a developer, I want to know if Foundry Local is a Windows component, app, or service so that I can plan its deployment.
author: jonburchel
ms.author: jburchel
ms.reviewer: maanavdalal
ms.date: 11/18/2025
ms.topic: concept-article
ms.service: azure-ai-foundry
---

# Foundry Local on Windows Server 2025

Foundry Local on Windows Server 2025 lets you run selected Microsoft Foundry model capabilities entirely on a single Windows Server machine you operate. Use this FAQ to quickly confirm what differentiates the Local runtime from the cloud service, how you deploy it, supported OS and GPU scenarios, concurrency behavior, and how the SDK relates to the service.

## Frequently asked questions

- **What is the capability differentiation between Foundry Local on Windows Server vs Foundry?**

  | **Capability** | **Foundry Local (on server)** | **Foundry (cloud)** |
  |----|----|----|
  | Model catalog | Local catalog is smaller, BYOM possible. Embeddings models aren't yet available in the Local catalog. | Broad catalog, including embeddings in the service; managed updates, evaluation, safety tools, and agent services. |
  | Scale & HA | Single node runtime. No ‑built-in ‑autoscale or ‑multinode‑ distribution. | Managed scale, multiregional‑ options, HA/DR patterns, and platform governance. Best for high concurrency and bursting. |
  | Concurrency / throughput | Limited; throughput declines as concurrent clients grow. No continuous batching today. | Cloud scale and load distribution; platform services for concurrency and throughput. |
  | APIs | OpenAI ‑compatible REST surface for chat/completions; MCP integration possible. | Full Foundry APIs, Responses API, Agent Service, eval, and integration with dev tools. |
  | Operations | You operate it like any server app: install, secure, monitor, back up; manage model bits locally. | Enterprise governance, cost controls, environments, RBAC/Networking, evaluation, and integrated DevOps. |

- **Is Foundry Local a Windows component, an app, or a service?**

  It runs as a service on a Windows Server machine. You can install it by using winget.

  ```bash
  winget install Microsoft.FoundryLocal
  ```
    
- **Which versions of server support Foundry Local?**

  - Windows Server 2025 Datacenter
  - Windows Server 2025 Standard

- **Does Foundry Local run on virtual machines with GPU-P?**

  Foundry Local **detects the partitioned GPU inside a GPU-P VM** and picks up a CUDA-enabled model when one is available. Otherwise, it falls back appropriately. The execution provider is also automatically selected based on the availability of GPU inside the VM.

- **What are the concurrency limitations of Foundry Local on server?**
  Foundry Local isn't optimized to serve multiple users as a shared on-premises endpoint. It doesn't yet support concurrent inference requests. Requests to one Foundry Local endpoint are processed sequentially. You must manage parallel execution across multiple endpoints at the application level. As concurrent requests increase, throughput drops and latency increases. There's no continuous batching in the Local runtime, so request coalescing doesn't happen under load. For multiple users or spiky traffic, move to [Microsoft Foundry](../index.yml).

- **How is Foundry Local SDK different from the Foundry Local service?**

  The [Foundry Local SDK](reference-sdk.md) is a development toolkit to build software or applications by using the Foundry Local service without using the Foundry Local CLI or REST APIs directly.

## Sample code

The [Medical report summary tool](https://github.com/microsoft/foundry-local-on-windowsserver-samples) demonstrates a medical report summarizer and translator using Foundry Local running in a remote Windows Server.

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Foundry Local architecture](../concepts/foundry-local-architecture.md)