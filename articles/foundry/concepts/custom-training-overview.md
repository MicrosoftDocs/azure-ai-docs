---
title: Custom code training in Microsoft Foundry
description: Learn how custom code training in Microsoft Foundry lets you bring your own code, frameworks, and techniques to post-train any open-weight or proprietary model.
author: soumyapatro
ms.author: soumyapatro
ms.service: microsoft-foundry
ms.topic: concept-article
ms.date: 05/19/2026
ms.custom: training, custom-code
ai-usage: ai-assisted
#CustomerIntent: As a data scientist, I want to understand what custom code training is in Foundry so that I can decide when to use it versus managed fine-tuning.
---

# Custom code training in Microsoft Foundry

Custom code training in Microsoft Foundry lets you bring your own training scripts to post-train any open-weight or proprietary foundation model on GPU compute. Because you bring your own code, you have full control over the training framework, technique, and model architecture. Run supervised fine-tuning (SFT), direct preference optimization (DPO), reinforcement learning (RL), continued pretraining, distillation, or any other technique - on any model you have access to.

Custom code training runs as command jobs in your Foundry project. You submit a training script, specify compute resources and a Docker environment, attach data and model inputs, and Foundry orchestrates the job on GPU clusters. When the job completes, you can save the trained model as an asset in your project and deploy it for inference.

## Why custom code training?

Custom code training offers capabilities that managed fine-tuning doesn't:

- **Any framework**: Use HuggingFace TRL, Accelerate, Unsloth, VERL, Slime, native PyTorch, or any framework that runs on GPU.
- **Any technique**: Apply SFT, DPO, GRPO, RFT, continued pretraining, distillation, quantization, or any custom training loop.
- **Any open-weight model**: Train Llama, Mistral, Phi, DeepSeek, Qwen, or any model available in the Foundry model catalog or your own storage.
- **Multinode distributed training**: Scale across multiple GPU nodes with PyTorch or Ray distribution.
- **Custom environments**: Package your dependencies in a Docker image from Azure Container Registry (ACR) or use curated environments like Azure Container for PyTorch (ACPT).
- **Experiment tracking**: Log metrics with MLflow, group runs under experiments, and compare results.
- **End-to-end workflow**: Train, save, and deploy models within a single Foundry project. Use trained models with agents.

## When to use custom code training vs. managed fine-tuning

Foundry offers two approaches to model customization. Choose the one that fits your scenario.

| Capability | Managed fine-tuning | Custom code training |
|------------|--------------------|--------------------|
| **Models supported** | Specific models with fine-tuning support (Azure OpenAI, select catalog models) | Any open-weight or proprietary model you have access to |
| **Techniques** | LoRA SFT, DPO, reinforcement fine-tuning (model-dependent) | Any technique - SFT, DPO, GRPO, RL, distillation, quantization, continued pretraining |
| **Code required** | No - configure through portal or API | Yes - bring your own training script |
| **Framework** | Managed by Foundry | Your choice - TRL, Accelerate, Unsloth, VERL, PyTorch |
| **Compute** | Managed by Foundry | You specify GPU cluster, node count, and distribution |
| **Environment** | Managed by Foundry | Custom Docker image (ACR) or curated environments |
| **Best for** | Quick customization of supported models with minimal setup | Full control over training, advanced techniques, unsupported models |

**Use managed fine-tuning** when you want to quickly customize a supported model without writing training code. For more information, see [Customize a model with fine-tuning](../openai/how-to/fine-tuning.md).

**Use custom code training** when you need full control over the training process, want to use a framework or technique that managed fine-tuning doesn't support, or need to train a model that isn't available through managed fine-tuning.

## Supported frameworks and techniques

Because you bring your own code, you're not limited to a fixed set of frameworks or techniques. Any training loop that runs on PyTorch or Ray works with custom code training.

Common frameworks and techniques include:

| Framework | Description |
|-----------|-------------|
| HuggingFace TRL | Transformer Reinforcement Learning library for SFT, DPO, GRPO, and other techniques |
| HuggingFace Accelerate | Distributed training and mixed precision for any PyTorch model |
| Unsloth | Optimized fine-tuning with reduced memory usage |
| VERL | Versatile RL training framework for LLMs |
| Slime | Lightweight RL training for foundation models |
| Native PyTorch | Direct PyTorch training loops |

| Technique | Description |
|-----------|-------------|
| Supervised fine-tuning (SFT) | Train on instruction-response pairs to align model behavior |
| Direct preference optimization (DPO) | Train on preference data to align outputs with human preferences |
| Group relative policy optimization (GRPO) | RL technique for reasoning model improvement |
| Reinforcement fine-tuning (RFT) | RL for tool use and agent behavior |
| Continued pretraining | Extend a model's knowledge with domain-specific data |
| Distillation | Transfer capabilities from a larger model to a smaller one |
| Quantization | Reduce model precision for efficient inference |

## How custom code training works

A custom code training job follows this lifecycle:

1. **Write training code**: Create a training script (`train.py`) using your preferred framework. Use MLflow to log metrics.
1. **Prepare resources**: Set up a GPU compute cluster, configure a Docker environment, and upload training data.
1. **Submit a command job**: Use the Microsoft Foundry SDK or Foundry CLI to submit the job. Pass your training code as an input (along with data and model inputs), specify compute, environment, and outputs.
1. **Monitor progress**: View logs, training metrics, and infrastructure metrics (GPU, memory, disk) in the Foundry portal or through the SDK.
1. **Save the model**: When the job completes, model outputs (safetensor format) are automatically registered as model assets in your project.
1. **Deploy for inference**: Map the trained model to a supported base model architecture and deploy it on a managed inferencing cluster.

## Key concepts

| Concept | Description |
|---------|-------------|
| **Command job** | A unit of work that runs your training script on a GPU compute cluster. Defined by a command string, compute, environment, inputs (including code, data, and models), and outputs. |
| **Experiment** | A named grouping for related job runs. Use experiments to organize and compare training runs with different hyperparameters. |
| **Compute cluster** | A set of GPU virtual machines that run your training jobs. You specify the cluster, number of nodes, and processes per node. |
| **Distribution** | The distributed training strategy. Foundry supports PyTorch and Ray distribution, setting up the required environment variables and rendezvous points. |
| **Environment** | A Docker image that contains the dependencies for your training script. Use a curated environment (ACPT) or a custom image from ACR. |
| **Model asset** | A packaged set of model weights, configuration, and metadata registered in your Foundry project. Model assets of type `SAFETENSOR_MODEL` or `CUSTOM_MODEL` are deployable. |
| **Inputs** | Data, models, or scalar values passed to the job. Data and model inputs support mount or download access modes. |
| **Outputs** | Data or model artifacts produced by the job. Model outputs are automatically registered as model assets. |

## Limitations

Custom code training in Foundry has the following limitations:

- **Generative AI training only**: Custom code training supports generative AI model training. Traditional machine learning workloads aren't supported.
- **No pipeline orchestration**: Multi-step training pipelines aren't available. Submit individual command jobs.
- **No hyperparameter search**: Automated hyperparameter tuning isn't supported. Submit separate jobs with different hyperparameters and compare results.
- **Deployment constraints**: Only full-weight safetensor models can be deployed. LoRA adapter deployment isn't yet supported.
- **No job migration**: Existing Azure Machine Learning job histories aren't migrated to Foundry.

## Related content

- [Quickstart: Submit a training job](../quickstarts/training-job-quickstart.md)
- [Set up compute for training](../training/setup-compute.md)
- [Submit a training job](../training/submit-training-job.md)
- [Monitor training jobs](../training/monitor-training-jobs.md)
- [Save and deploy trained models](../training/save-deploy-trained-model.md)
- [Customize a model with fine-tuning](../openai/how-to/fine-tuning.md)
