---
title: Deploy open-source AI models with managed compute in Foundry
description: Learn how managed compute in Microsoft Foundry lets you deploy and serve open-source AI models on elastic GPU capacity without managing virtual machines, Kubernetes clusters, or model runtimes.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.custom:
  - build-2026
ms.topic: how-to
ms.date: 05/25/2026
ms.author: mopeakande
author: msakande
ms.reviewer: mabables
reviewer: ManojBableshwar
ai-usage: ai-assisted

#CustomerIntent: As an Azure AI developer, I want to use managed compute to deploy and serve open-source AI models on elastic GPU capacity without the operational burden of managing virtual machines, Kubernetes clusters, or model runtimes.
---

# Deploy open-source AI models with managed compute

Managed compute in Microsoft Foundry is a deployment type that lets you serve open-source and custom-weight models on dedicated GPU capacity without provisioning virtual machines, Kubernetes clusters, or model runtimes. Microsoft handles GPU allocation, container images, scaling, and security patching, while you choose the model, runtime profile, GPU family, and scaling behavior that fit your workload.

Managed compute sits alongside the two other Foundry deployment types: pay-per-token (serverless, token-billed inference for first-party models) and provisioned throughput units (PTU) for reserved, predictable capacity on first-party models. Use managed compute when you need to run open-source models from the Foundry model catalog or your own fine-tuned weights on managed GPUs.

This article explains how managed compute works, how to deploy a model from the catalog or your own weights, how to send inference requests, and how to scale, monitor, and bill the deployment.

## Prerequisites

- An active Azure subscription with permission to create Microsoft Foundry resources.
- A Microsoft Foundry resource and project. To create one, see [Create a Foundry project](../../how-to/create-projects.md).
- The **Cognitive Services Contributor** role (or an equivalent custom role) on the Foundry resource.
- Approved managed-compute quota for the GPU accelerator SKU you plan to use (A100, H100, H200, or MI300X). Managed-compute quota is requested through the Foundry quota process and is **separate from Azure VM quota** — existing VM quota cannot be applied to managed compute deployments.
- For the SDK examples in this article: Python 3.10 or later and the following packages:

    ```bash
    pip install azure-ai-inference azure-mgmt-cognitiveservices azure-identity
    ```

- For the CLI examples: Azure CLI 2.60 or later with the `cognitiveservices` extension installed.

## What is managed compute deployment?

Managed compute is a managed GPU compute platform within Microsoft Foundry. It lets you deploy, customize, and scale open-source models on dedicated GPU compute without managing VMs, clusters, or infrastructure. It extends Foundry's model hosting with a deployment type built specifically for open-source models.

Managed compute shares the same authentication, networking, endpoints, SDKs, and portal experience as Foundry's other deployment types, so open-source model serving fits into existing Foundry workflows without new access configuration or client code.

### Where it fits in Foundry

| Deployment type | What it is | Best for |
|---|---|---|
| Pay-per-token | Serverless, token-based inference for first-party models | Bursty traffic on hosted Foundry models with no capacity planning |
| PTU | Reserved throughput units with consistent performance | Predictable, sustained load on first-party models |
| Managed compute | Dedicated GPU compute for open-source models — model-centric, no VM management | Hosting open-source or custom-weight models on managed GPUs |

Managed compute brings together three capability pillars:

- **Model catalog.** Thousands of open-source models curated by Microsoft and trusted partners, with enterprise-grade vulnerability scanning and licensing compliance.
- **Optimized inference stack.** High-performance runtimes (vLLM, SGLang, NVIDIA NIM) with advanced serving features such as continuous batching, speculative decoding, and LoRA hot-swap.
- **Managed GPUs.** Deploy by model instance — Microsoft owns runtime patching, scaling, and updates, and you can scale to zero when idle.

## When to use managed compute

Managed compute is purpose-built for managed, model-centric GPU PaaS. Use this section to determine whether it fits your workload.

- **Foundry managed compute** — managed AI platform, maximum time-to-value, moderate customization.
- **Azure Machine Learning or AKS** — maximum customer control, bring-your-own everything, medium scale.
- **Azure GPU IaaS** — maximum scale, full hardware access, frontier training and HPC.

| Attribute | Foundry managed compute | Not a fit? Use instead |
|---|---|---|
| **Control** | Configurable within supported bounds — model, runtime profile, GPU family, scaling | Need full control over frameworks, containers, or custom serving code? Azure Machine Learning or AKS |
| **Scale** | Designed for 8–64 GPU workloads; total fleet around 1,000 GPUs | Need 1,000–10,000 GPUs with capacity blocks and InfiniBand? Azure Machine Learning or AKS (managed GPU IaaS) |
| **Runtime** | Microsoft-managed runtimes (vLLM, SGLang, NIM) — auto-patched, no container ownership | Need your own framework, custom container, or non-LLM serving stack? Azure Machine Learning or AKS |
| **Workload** | LLM inference, custom-weight serving, LoRA-based multi-variant serving | Need custom training with your own code and frameworks? Azure Machine Learning managed compute |
| **Purchase** | Virtual GPUs via model instances — pay for GPUs, not nodes | Need VM-level capacity reservations with InfiniBand? Azure Machine Learning or AKS capacity blocks |
| **HPC scale** | Not designed for frontier-scale pretraining or HPC | Need 10,000+ GPUs, bare metal, or supercomputer-class workloads? Azure GPU IaaS |

## Supported models

Managed compute supports a broad surface of open-source and partner models:

- **Open-source catalog.** Thousands of open-source models curated by Microsoft and trusted partners, including Hugging Face, NVIDIA, and Microsoft Research. Approximately 50 new models are published each month, with more than 10,000 models available in the catalog today. New models are typically published within hours of upstream release and are scanned for vulnerabilities and licensing compliance.
- **NVIDIA Inference Microservice (NIM) models.** NIM models published by NVIDIA, optimized for NVIDIA-tuned kernels and the TensorRT-LLM backend.
- **Domain-specific industry models.** Models from industry partners such as Bayer and Sight Machine.
- **Custom-weight (BYOW) models.** Bring your own full model weights or LoRA adapters and serve them on managed GPUs.
- **Format.** Models must be in SafeTensors format with a tokenizer and config file.

Models are served on Microsoft-curated runtimes that are matched to each model architecture:

| Runtime | Best for | Key features |
|---|---|---|
| **vLLM** | High throughput, general purpose | PagedAttention, continuous batching, speculative decoding, tensor parallelism, LoRA hot-swap |
| **SGLang** | Structured generation, constrained decoding | RadixAttention, constrained grammar output, tree-structured batch scheduling |
| **NVIDIA NIM** | NVIDIA-optimized models (Nemotron, Llama) | TensorRT-LLM backend, NVIDIA-tuned kernels, NIM API compatibility |
| **TensorRT-LLM** | NVIDIA-optimized models | Low-latency NVIDIA inference runtime |

## Deploy a model with managed compute

You can deploy a model from the Foundry catalog or import your own weights (BYOW). Both flows use the same scaling, GPU selection, and deployment template machinery.

### Deploy a catalog model

1. **Choose your model.** Browse open-source models in the Foundry portal model catalog, or select one programmatically by registry ID.
1. **Configure your runtime.** Pick a serving framework (vLLM, SGLang, NIM), set the maximum context length, and choose a throughput- or latency-optimized profile.
1. **Select a GPU family.** Pick an accelerator family — A100, H100, H200, or MI300X. You don't need to know specific VM SKUs; Foundry uses the deployment template's `accelerator_maps` block to size each model instance for the family you choose.
1. **Configure scaling.** Set auto-scale or manual scale and choose the scale-to-zero idle timeout. With manual scaling, total GPUs equal the number of model instances times the GPUs-per-instance for the selected accelerator family.
1. **Deploy.** Submit the deployment by using the SDK or CLI. The deployment exposes a standard Foundry endpoint when provisioning completes.

   # [Python SDK](#tab/python)

   ```python
   from azure.mgmt.cognitiveservices.models import (
       AcceleratorDeployment,
       AcceleratorDeploymentProperties,
       Sku,
   )

   deployment = AcceleratorDeployment(
       properties=AcceleratorDeploymentProperties(
           model="azureai://registries/azureml-openai-oss/models/gpt-oss-120b/versions/4",
           deployment_template="azureai://registries/azureml-openai-oss/deploymenttemplates/gpt-oss-120b-short-context/versions/1",
           accelerator_type="H100_80GB",
           version_upgrade_option="OnceNewDefaultVersionAvailable",
       ),
       sku=Sku(name="GlobalManagedCompute", capacity=1),  # 1 model instance
   )

   poller = cog.accelerator_deployments.begin_create_or_update(
       resource_group_name="my-rg",
       account_name="my-foundry-account",
       deployment_name="gpt-oss-120b-gpu",
       accelerator_deployment=deployment,
   )

   result = poller.result()  # blocks ~10-15 min

   print(f"State: {result.properties.provisioning_state}")      # Succeeded
   print(f"GPUs:  {result.properties.total_accelerators}")       # 4
   print(f"Route: {result.properties.routes.chat_completions_scoring_path}")  # /v1/chat/completions
   ```

   # [Azure CLI](#tab/azure-cli)

   ```bash
   az cognitiveservices account accelerator-deployment create \
     --name $ACCOUNT -g $RG \
     --deployment-name gpt-oss-120b-gpu \
     --model "azureai://registries/azureml-openai-oss/models/gpt-oss-120b/versions/4" \
     --deployment-template "azureai://registries/azureml-openai-oss/deploymenttemplates/gpt-oss-120b-short-context/versions/1" \
     --accelerator-type H100_80GB \
     --sku-name GlobalManagedCompute \
     --sku-capacity 1 \
     --no-wait
   ```

   ---

#### Verify the deployment

The create operation typically takes 10–15 minutes. Poll the deployment until `provisioning_state` is `Succeeded`, and then read the assigned GPU count and the scoring route to confirm the endpoint is ready:

- `properties.provisioning_state` — `Succeeded` when the deployment is live.
- `properties.total_accelerators` — total GPUs assigned to the deployment.
- `properties.routes.chat_completions_scoring_path` — the route exposed by the runtime, for example `/v1/chat/completions`.

### Deploy a custom model (BYOW)

Bring-your-own-weights deployment lets you serve a model you trained or fine-tuned yourself. The flow differs from a catalog deployment only in how the model asset is sourced:

1. **Import your model.** Upload from local storage, register from an Azure Machine Learning training job, or import directly from Hugging Face.
1. **Map to a base model.** Foundry maps your model's base lineage to compatible GPU and runtime configurations automatically using catalog metadata.

For GPU selection, scaling, and deployment, follow steps 3–5 in [Deploy a catalog model](#deploy-a-catalog-model).

## Send inference requests to the deployment

Managed compute deployments share the same endpoint, authentication, and SDK surface as pay-per-token and PTU deployments. You can call them with existing Foundry API keys or identities and reuse your client code.

Managed compute deployments expose inference routes under the following endpoint pattern:

```
<endpoint>/managed-deployments/<deployment-name>/<route>/
```

How you call the deployment depends on the runtime:

- **For models with chat-completions–compatible runtimes**, you can also use the OpenAI-compatible route `<endpoint>/openai/v1/` with the same OpenAI SDK code you use for first-party Foundry models. Foundry routes the request to your managed compute deployment based on the `deployment-name` in the payload, so the client experience is identical to calling a first-party model.
- **For bespoke models** such as rerankers, embedding models, or speech models, call the model provider's SDK against the `<endpoint>/managed-deployments/<deployment-name>/` route. This pattern preserves Foundry authentication and networking while letting the provider SDK speak its native protocol.

### Chat completions

The same inference code works across pay-per-token, PTU, and managed compute for any model whose runtime supports chat completions.

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```python
from azure.ai.inference import (
    ChatCompletionsClient
)
from azure.core.credentials import (
    AzureKeyCredential
)

client = ChatCompletionsClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(KEY)
)

response = client.complete(
    model="<deployment-name>",
    messages=[
        {"role": "user",
         "content": "Hello!"}
    ]
)
```

# [OpenAI SDK](#tab/openai)

```python
from openai import OpenAI

endpoint = "https://<your-foundry-resource>.openai.azure.com/openai/v1/"
deployment_name = "<deployment-name>"
api_key = "<your-api-key>"

client = OpenAI(base_url=endpoint, api_key=api_key)

completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ],
    temperature=0.7,
)

print(completion.choices[0].message)
```

---

### Custom routes (rerankers, embeddings, speech)

For models that don't expose chat completions, call the provider SDK against the `managed-deployments` custom route:

```
<endpoint>/managed-deployments/<deployment-name>/<custom-route>/
```

This pattern preserves Foundry authentication and networking while letting the provider SDK speak its native protocol for reranking, embedding, or speech workloads.

## Manage and scale a deployment

Managed compute deployments are model-centric: you scale by model instance rather than by VM or node.

- **Auto vs. manual scaling.** Choose auto-scale to size the deployment from live traffic, or manual scale to pin a fixed number of model instances.
- **Scale to zero.** Configure an idle timeout. When no traffic arrives within the window, the deployment scales to zero and billing stops immediately. The next request after scale-to-zero pays a cold-start cost while the model is reloaded.
- **Manual sizing.** With manual scaling, total GPUs equal model instances multiplied by GPUs-per-model-instance from the deployment template's `accelerator_maps` entry.
- **Microsoft-managed runtimes.** Serving runtimes, base container images, and security patches are owned and applied by Microsoft. Patches are applied to live customer deployments automatically — you don't operate or rebuild containers.
- **Version upgrades.** Set `version_upgrade_option="OnceNewDefaultVersionAvailable"` on the deployment to opt the deployment into picking up new default model or runtime versions when they're published.
- **Health probes.** Deployment templates include liveness and readiness probes that Foundry uses to monitor instance health and gate traffic during rollouts.
- **Delete a deployment.** Remove a deployment from the Foundry portal, by running `az cognitiveservices account deployment delete`, or by calling the management SDK.

## Pricing and billing

Managed compute is billed hourly, metered per accelerator SKU.

- **Billing model.** Pay-as-you-go hourly metering. Each model instance consumes GPUs of the accelerator family you select (A100, H100, H200, or MI300X).
- **Billing unit.** Throughput per GPU, aligned with parameter count and industry benchmarks so you can compare against alternatives.
- **Cost alignment.** Auto-scale and scale-to-zero align cost with actual traffic — you pay only for GPUs that are serving traffic or warm-reserved.
- **Quota.** Quota is requested through the Foundry quota process and granted per SKU per region. Managed compute quota is **separate from Azure VM quota** because Azure VMs are an IaaS offering with regional SKUs, while managed compute is a PaaS offering that leads with Global and Data Zone deployments. You can't apply existing VM quota to a managed compute deployment.
- **Regions.** Global at launch. Data Zone and additional region offerings are planned (TBD).
- **Per-hour rates and commitment discounts.** Per-hour rates by SKU and region, 1-year reserved capacity, and commitment discounts are **(under consideration)**. Final rates will be published when the service reaches general availability.

For current pricing, see the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/).

## Troubleshooting

### Deployment provisioning failures

If `provisioning_state` returns `Failed`, confirm that the requested accelerator SKU has approved quota in the region you targeted, and that the chosen deployment template lists that accelerator family in its `accelerator_maps` block. Mismatched model and deployment-template versions are a common cause of provisioning failures — verify both references resolve to valid registry assets.

### Quota exceeded

A "quota exceeded" error means the Foundry account doesn't have enough managed compute quota in the region for the requested SKU. Request additional quota through the Foundry quota process. Quota is granted per accelerator SKU per region, and Azure VM quota doesn't apply.

### Insufficient capacity in region

If the region returns no capacity for the requested SKU, try a different accelerator family (for example, deploy on H200 instead of H100), or target a different region. Larger memory SKUs such as H200 and MI300X often have capacity for models that don't fit on A100.

### Cold-start latency after scale-to-zero

The first request after a scale-to-zero idle window pays a cold-start cost while the model is reloaded onto GPUs. If you need predictable first-token latency, increase the idle timeout window so the deployment stays warm longer, or set a minimum instance count greater than zero.

### 404 from the `openai/v1/` route

If a request to `<endpoint>/openai/v1/` returns 404, the underlying runtime for that deployment doesn't expose chat completions. Use the `<endpoint>/managed-deployments/<deployment-name>/` route together with the model provider's SDK instead.

### Inference 429 (throttling)

A 429 response indicates that requests are exceeding the per-instance concurrency limit. Increase `maxConcurrentRequestsPerInstance` in the deployment template (if your runtime supports the higher value), or scale out by adding more model instances.

## Related content

- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Deployment templates reference](../foundry-models/reference/deployment-templates.md)
- [Managed compute pay-as-you-go](../../../foundry-classic/how-to/deploy-models-managed-pay-go.md)
