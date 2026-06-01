---
title: "Managed compute in Microsoft Foundry"
description: "Learn how managed compute in Microsoft Foundry hosts open-source models on dedicated GPU capacity through the same endpoint, SDKs, identity, networking, observability, and billing as other Foundry deployment types."
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.custom:
  - build-2026
ms.topic: concept-article
ms.date: 05/31/2026
ms.author: mabables
author: ManojBableshwar
ms.reviewer: mopeakande
reviewer: msakande
ai-usage: ai-assisted
#CustomerIntent: As a Microsoft Foundry developer or platform owner, I want to understand what managed compute is, how it fits alongside pay-per-token and provisioned throughput, and what models, runtimes, accelerators, billing, and access control it provides, so that I can decide when to use it and plan a deployment.
---

# Managed compute in Microsoft Foundry

Managed compute is a deployment type in Microsoft Foundry that hosts open-source models on dedicated GPU capacity without requiring you to provision virtual machines, operate a Kubernetes cluster, build container images, or own a model serving runtime. Microsoft owns the GPU topology, runtime, container image, and security patching. You choose the model, deployment template, accelerator family, and scaling behavior that fit your workload.

Managed compute uses the same Foundry resource, project, endpoint, authentication, network configuration, SDKs, observability, and billing surface as the other deployment types in Foundry. After you deploy a model with managed compute, your application code is the same as any other Foundry model — only the deployment name changes.

This article explains the deployment type, the concepts you work with (model instances, deployment templates, accelerator families, runtimes), the catalog you can deploy from, inference endpoints, scaling, billing and quota, access control, and current limitations. For step-by-step deployment instructions, see [Deploy open-source models with managed compute](../how-to/deploy-models-managed.md).

## Where managed compute fits in Foundry

Foundry offers three deployment types. Managed compute is the deployment type for open-source models on dedicated GPU capacity.

| Deployment type | What it serves | Billing | Best for |
|---|---|---|---|
| Pay-per-token | First-party (Azure Direct) models, including Azure OpenAI | Per input and output token | Lowest-friction path to get started; bursty traffic on hosted models with no capacity planning. |
| Provisioned throughput units (PTU) | First-party (Azure Direct) models | Reserved throughput units | Predictable, sustained load on first-party models with consistent latency. |
| Managed compute | Open-source and community models from the Foundry catalog | Hourly per accelerator family | Hosting open-source models on dedicated GPUs with Foundry-managed runtimes, private networking, and the same SDKs as the other deployment types. |

All three share a single Foundry endpoint, the same authentication patterns (Microsoft Entra ID and key), the same SDKs, the same observability surface, and a single bill. You can mix all three deployment types in a single Foundry project and call them from the same client code.

## Key concepts

### Model instance

A **model instance** is the unit of deployment in managed compute. You don't choose a virtual machine SKU or size a node — you describe the workload in model terms, and Foundry chooses the GPU topology underneath. An instance might use one accelerator or several, depending on the model and the deployment template you pick. You scale a deployment by changing the number of model instances (the `capacity` value on the deployment SKU).

### Deployment template

A **deployment template** is a named, versioned asset that encodes how a specific model should run. A template pins:

- The serving runtime (for example, vLLM or SGLang).
- The accelerator family and count per instance (for example, one H100 80 GB, or two A100 80 GB).
- The supported context length and any quantization choices.
- Runtime-specific tuning — tool-call and reasoning parsers, scoring path, health probes, request concurrency, and any model-specific context-extension settings.

When you script a deployment, you reference the template ID and Foundry handles the rest. Each model in the catalog typically ships with multiple templates that trade off accelerator family, context length, and latency vs. throughput. For example, the `qwen3-32b` model exposes four templates side by side:

| Template | Runtime | Accelerator | Context |
|---|---|---|---|
| `qwen--qwen3-32b--40k-nvidia-a100` | vLLM | 1 × A100 80 GB | 40 K |
| `qwen--qwen3-32b--40k-nvidia-h100` | vLLM | 1 × H100 80 GB | 40 K |
| `qwen--qwen3-32b--128k-nvidia-2xa100` | vLLM | 2 × A100 80 GB | 128 K |
| `qwen--qwen3-32b--128k-nvidia-2xh100` | vLLM | 2 × H100 80 GB | 128 K |

Choosing a template is the only knob you turn for *how* a model runs.

### Accelerator families

Managed compute deployments target an **accelerator family**, not a specific virtual machine SKU. The supported families today are:

- NVIDIA A100 80 GB (`A100_80GB`)
- NVIDIA H100 80 GB (`H100_80GB`)
- AMD MI300X 192 GB (`MI_300_192GB`)

Quota is granted per accelerator family per region.

### Model runtimes

Managed compute runs each model on a serving runtime that Microsoft builds, scans, signs, and patches. You don't operate or rebuild containers. The runtime portfolio is selected per model architecture:

| Runtime | Use for | Notes |
|---|---|---|
| vLLM | High-throughput LLM serving | Continuous batching, PagedAttention, tensor parallelism, LoRA hot-swap. Default for most large language models. |
| SGLang | Structured-output LLM serving | JSON, regex, and grammar-constrained generation for agentic and tool-using workloads. |
| TensorRT-LLM | NVIDIA-optimized LLM serving | Low-latency NVIDIA inference for model families where TRT-LLM wins on latency or throughput. |
| NVIDIA NIM | NVIDIA Inference Microservices | TensorRT-LLM backend with NIM API compatibility for NVIDIA-published models. |
| Text Embeddings Inference (TEI) | Embeddings, rerankers, classifiers | Accelerator-specific kernels for embedding and retrieval hot paths. |
| llama.cpp | CPU and small-GPU serving | GGUF-quantized models behind the same OpenAI-compatible API. |
| hf-serve | Vision, audio, segmentation, other Transformers-native pipelines | Hugging Face's multi-model server for modalities outside the LLM and embedding fast paths. |

Runtime upgrades and CVE patches are applied to live customer deployments automatically. You don't redeploy your model to pick up a runtime update.

## Models you can deploy

Managed compute deploys models from the **Hugging Face Collection** in the Foundry model catalog, served from the `azure-huggingface` registry.

- **Curated and refreshed weekly.** Trending models from the Hugging Face ecosystem are added continuously as the community publishes them. The catalog spans text, vision, audio, and multimodal models — LLMs and vision-language models for chat and agents, automatic speech recognition (ASR), speech translation, embeddings, segmentation, and image generation.
- **SafeTensors only, no untrusted code.** Every model in the Collection is screened. Repositories that would require executing third-party Python at load time (`trust_remote_code` patterns) are remediated or excluded.
- **Pre-staged weights.** Model weights are pulled from Hugging Face once, validated, and stored in Microsoft-managed Azure storage in the regions where the model is served. Container images live in a Microsoft-managed registry. As a result, **managed compute deployments don't need outbound network access to Hugging Face Hub** — you can deploy into a fully private network with no egress.
- **License metadata preserved.** Each catalog model card captures and surfaces the upstream license; license review against Microsoft's enterprise distribution policy happens during curation.

Every model in the Collection passes through a five-stage curation pipeline before it appears in the catalog:

1. Identify trending models based on community signals, partner requests, and customer demand.
2. Screen for compliance and security — license review, inspection for `trust_remote_code` and custom executable code.
3. Build, scan, and publish runtime container images — built by Microsoft, scanned for CVEs, signed, and published to a Microsoft-managed registry.
4. Upload weights to secure Azure storage — validated against the model card and stored in the regions where the model is served.
5. Validate and publish — every model + runtime + accelerator combination is tested for API conformance and performance, then published to the catalog with a one-click deploy path.

## Inference endpoints

Deploying a model to managed compute makes the model available for inference on the **unified Foundry project endpoint** — the same endpoint used by pay-per-token and provisioned throughput deployments. The base endpoint follows the pattern:

```text
https://<account>.services.ai.azure.com
```

### Endpoint routes

A managed compute deployment can be invoked over two route families on the unified endpoint. The route you choose depends on whether the underlying model and runtime expose an OpenAI-compatible API.

| Route | Path | Applies to | Behavior |
|---|---|---|---|
| Managed deployments route (OSS) | `<endpoint>/managed-deployments/<deployment-name>/` | All managed compute deployments | Works for every model deployed on managed compute, including bespoke models that ship with their own SDK. Models that expose `/chat/completions` can also be called over this route with the OpenAI SDK by pointing the client `base_url` at this path. |
| OpenAI-compatible route | `<endpoint>/openai/v1/` | Managed compute deployments whose runtime exposes an OpenAI-compatible API (for example, vLLM, SGLang, TensorRT-LLM, llama.cpp serving chat or embeddings) | The OpenAI SDK can call the deployment by setting `base_url` to this path and passing the **deployment name** in the `model` field of the request payload. If a request targets this route with a deployment name whose underlying model or runtime doesn't support the OpenAI-compatible surface, the runtime returns **HTTP 404**. |

In short: every managed compute deployment is reachable on the `managed-deployments/<deployment-name>/` route, and any deployment whose runtime is OpenAI-compatible is *additionally* reachable on the `openai/v1/` route. Use the OpenAI route when you want to share client code with other Foundry deployments; use the managed-deployments route for models that ship a custom SDK or non-OpenAI API.

A chat-completions managed compute deployment can also be added to a Foundry Agent as an admin-connected model and called through the Foundry Responses API with the same OpenAI SDK — same authentication, endpoint, and observability as any other Foundry model.

### Endpoint authentication

Managed compute deployments use the same authentication patterns as the rest of the Foundry endpoint:

- **Microsoft Entra ID (recommended).** Acquire a token for the `https://ai.azure.com/.default` scope and pass it as a bearer token in the `Authorization` header. To call a managed compute deployment with Entra ID, the calling identity needs the **Azure AI User** role on the Foundry account scope. The OpenAI SDK in token-based mode and `DefaultAzureCredential` work without any managed-compute-specific configuration.
- **Account API key.** Pass the Foundry account key as `Authorization: Bearer <key>`. The OpenAI SDK sends the key in this form automatically when you set the `api_key` argument. Keys grant the same access on managed compute deployments as on pay-per-token and PTU deployments on the same account.

Both authentication options work on both endpoint routes. For end-to-end client code samples (OpenAI SDK with Entra ID, OpenAI SDK with API key, and REST), see [Deploy open-source models with managed compute](../how-to/deploy-models-managed.md#step-6-send-a-test-request).

## Scaling

You scale a managed compute deployment by changing the number of model instances — set the `capacity` value on the deployment SKU and Foundry adjusts the GPU count accordingly. Total GPUs equal the number of model instances multiplied by the GPUs-per-instance defined by the deployment template you chose. Foundry doesn't ask you to size a node or pick a VM family.

## Billing, quota, and deployment scopes

Managed compute is billed **hourly per accelerator**. Unlike VM-based infrastructure where you rent whole GPU servers and pay for every GPU on the box whether your model uses it or not, managed compute charges for model instances. Foundry right-sizes each model to the GPUs it actually needs — one, two, four, or eight — so you're not paying for idle accelerators sitting next to your workload. The cost of a deployment is:

**Accelerators per model instance × model instances × hours running × hourly rate**

Hourly rates vary by accelerator family (A100, H100, MI300X) and by deployment scope. For current pricing, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

### Deployment scopes

Managed compute supports two deployment scopes, set through the deployment SKU. **Global** is available at preview launch and gives you the broadest accelerator capacity at the lowest rate. **Data Zone** — for when traffic needs to stay within a defined data-residency boundary — is **coming soon**. Code, SDKs, and workflow are identical across scopes — only the SKU name changes.

| Scope | SKU name | Availability | Use for |
|---|---|---|---|
| Global | `GlobalManagedCompute` | Available | Broadest accelerator capacity and best pricing. |
| Data Zone | `DataZoneManagedCompute` | Coming soon | Regional residency and sovereignty requirements. |

For the current list of regions and accelerator families per region, see the Foundry [general availability matrix](general-availability.md).

### Quota

Managed compute quota is granted per accelerator family per region through the Foundry quota process. Managed compute quota is **separate from Azure VM quota** — Azure VM quota is an infrastructure-as-a-service allocation tied to specific regional VM SKUs, while managed compute is a managed PaaS offering. Existing Azure VM quota can't be applied to a managed compute deployment.

For details on viewing usage, attributing cost to a project, and requesting quota, see [Plan and manage costs for Microsoft Foundry](manage-costs.md) and [Manage and increase quotas](../how-to/quota.md).

## Access control

Managed compute uses Foundry's role-based access control (RBAC) model. The set of Azure resource provider operations required to create, read, update, and delete a managed compute deployment is documented in [Role-based access control for Microsoft Foundry — managed compute control-plane operations](rbac-foundry.md#managed-compute-control-plane-operations), along with the built-in roles that grant each operation.

At a glance:

- **Cognitive Services Contributor** (or **Foundry Owner** / **Foundry Account Owner**) grants full create / read / update / delete on managed compute deployments.
- **Cognitive Services User** and **Foundry User** grant read-only access to deployments.
- **Foundry Project Manager** grants read access to deployments and to accelerator usage data, but not create or delete.

Inference (data plane) on the unified Foundry endpoint follows the standard Foundry pattern — assign **Azure AI User** on the Foundry account scope to call deployments with Microsoft Entra ID.

## Limitations

Managed compute is in **public preview**. Note the following before deploying production workloads:

- **Content filtering.** Built-in Azure AI Content Safety filters aren't part of the managed compute data path in public preview. If you need request- or response-level filtering, call the [Azure AI Content Safety APIs](/azure/ai-services/content-safety/overview) directly from your application.
- **Region availability.** Managed compute launches with Global scope. Data Zone deployments and additional regions are rolling out — see the [general availability matrix](general-availability.md) for current coverage.
- **Pricing.** Per-hour rates by accelerator family and region, reserved capacity, and commitment discounts are evolving during preview. For current rates, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

## Related content

- [Deploy open-source models with managed compute](../how-to/deploy-models-managed.md)
- [Deployment overview for Microsoft Foundry Models](deployments-overview.md)
- [Role-based access control for Microsoft Foundry](rbac-foundry.md)
- [Plan and manage costs for Microsoft Foundry](manage-costs.md)
- [Manage and increase quotas](../how-to/quota.md)
- [Authentication and authorization in Foundry](authentication-authorization-foundry.md)
