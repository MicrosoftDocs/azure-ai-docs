---
title: Compile Hugging Face models for Foundry Local
titleSuffix: AI Foundry Local
description: This article provides instructions on how to compile Hugging Face models for Foundry Local.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: how-to
ms.date: 02/12/2025
ms.author: samkemp
author: samuel100
---

# Compile Hugging Face models for Foundry Local

The Foundry Local model catalog contains [ONNX](https://onnx.ai/) models that are capable of running on-device with quality and performance. The models are published in accordance with Microsoft Responsible AI Guidelines.

With Foundry Local, you aren't limited to models available in the catalog - you can run any model that is in the ONNX format.

In this article you learn how to:

> [!div class="checklist"]
> - **Compile** a model from Hugging Face into the ONNX format using Olive so that it can run efficiently on your local device.
> - **Run** the optimized and quantized in the Foundry Local CLI and REST server.

## Prerequisites

* Python version 3.10 or greater.

## Install Olive

Olive is a cutting-edge model optimization toolkit that enables you to ship ONNX models with quality and performance.

To install Olive, use Python pip:

### [Bash](#tab/Bash)
```bash
pip install olive-ai[auto-opt]
```
### [PowerShell](#tab/PowerShell)
```powershell
pip install olive-ai[auto-opt]
```
---

> [!TIP]
> We recommend installing Olive in a Python virtual environment using either [venv](https://docs.python.org/3/library/venv.html) or [conda](https://www.anaconda.com/docs/getting-started/miniconda/main).

## Sign in to Hugging Face

In this article, you're optimizing [Llama-3.2-1B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct/tree/main) from Hugging Face. Llama 3.2 is a gated model and therefore you need to be signed into Hugging-Face to get access.

### [Bash](#tab/Bash)
```bash
huggingface-cli login
```
### [PowerShell](#tab/PowerShell)
```powershell
huggingface-cli login
```
---

> [!NOTE]
> You're prompted for a user token to sign-in. Follow the [Hugging Face documentation for setting up User Access Tokens](https://huggingface.co/docs/hub/security-tokens)


## Compile model using Olive
Next you run the `auto-opt` Olive command that automatically downloads and optimizes Llama-3.2-1B-Instruct. After the model is downloaded, Olive will convert it into ONNX format, quantize (int4), and optimizing the graph.


### [Bash](#tab/Bash)
```bash
olive auto-opt \
    --model_name_or_path meta-llama/Llama-3.2-1B-Instruct \
    --trust_remote_code \
    --output_path models/llama \
    --device cpu \
    --provider CPUExecutionProvider \
    --use_ort_genai \
    --precision int4 \
    --log_level 1
```

### [PowerShell](#tab/PowerShell)
```powershell
olive auto-opt `
    --model_name_or_path meta-llama/Llama-3.2-1B-Instruct `
    --trust_remote_code `
    --output_path models/llama `
    --device cpu `
    --provider CPUExecutionProvider `
    --use_ort_genai `
    --precision int4 `
    --log_level 1
```
---

> [!NOTE]
> It takes around 60 seconds **plus model download time** (which depends on your network bandwidth) to complete model compilation.

### More details on `auto-opt`

- The `model_name_or_path` can be either (a) the Hugging Face Repo ID for the model {username}/{repo-name} or (b) a path on local disk to the model or (c) an Azure AI Model registry ID.
- `output_path` is the path on local disk to store the optimized model.
- `device` is the device the model executes on - CPU/NPU/GPU.
- `provider` is the hardware provider of the device to inference the model on. For example, Nvidia CUDA (`CUDAExecutionProvider`), DirectML (`DmlExecutionProvider`), AMD (`MIGraphXExecutionProvider`, `ROCMExecutionProvider`), OpenVINO (`OpenVINOExecutionProvider`), Qualcomm (`QNNExecutionProvider`), TensorRT (`TensorrtExecutionProvider`).
- `precision` is the precision for the optimized model (`fp16`, `fp32`, `int4`, `int8`).
- `use_ort_genai` creates extra configuration files for inference

With the `auto-opt` command, you can change the input model to one that is available on Hugging Face - for example, to `HuggingFaceTB/SmolLM-360M-Instruct` - or a model that resides on local disk. Olive, goes through the same process of automatically converting (to ONNX), optimizing the graph and quantizing the weights. The model can be optimized for different providers and devices.

### Change model directory name
Olive outputs the compiled ONNX model and configuration files into a `model` directory in the `models/llama` output path. Foundry Local uses the directory name of the compiled model as the ID to run the model (`foundry model run model`). By renaming the directory to `llama-3.2`, you can run the model with a more specific name (`foundry model run llama-3.2`). To rename use:

### [Bash](#tab/Bash)
```bash
cd models/llama
mv model llama-3.2
```

### [PowerShell](#tab/PowerShell)
```powershell
cd models/llama
Rename-Item -Path "model" -NewName "llama-3.2"
```
---

## Run the model in Foundry Local
First, change the Foundry Local cache to the `models` output directory of the Olive compilation:

### [Bash](#tab/Bash)
```bash
# change directory of cache
foundry cache cd models
# list models in cache (you should see llama-3.2)
foundry cache ls
# run the model
foundry model run llama-3.2 --verbose
```

### [PowerShell](#tab/PowerShell)
```powershell
# change directory of cache
foundry cache cd models
# list models in cache (you should see llama-3.2)
foundry cache ls
# run the model
foundry model run llama-3.2 --verbose
```
---


## Next step

- [Learn more about Olive](https://microsoft.github.io/Olive/)