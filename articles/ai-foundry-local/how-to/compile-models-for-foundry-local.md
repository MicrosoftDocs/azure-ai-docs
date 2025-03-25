---
title: Run Hugging Face models on Foundry Local
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

# Run Hugging Face models on Foundry Local

Foundry Local lets you run ONNX models on your local device with high performance. While the model catalog includes pre-compiled models, you can also use any ONNX-formatted model.

In this guide, you'll learn to:

> [!div class="checklist"]
> - **Compile** a Hugging Face model to the ONNX format using Olive
> - **Run** the optimized model using Foundry Local

## Prerequisites

* Python 3.10 or later

## Install Olive

[Olive](https://github.com/microsoft/olive) is a toolkit for optimizing models to ONNX format.

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
> Install Olive in a virtual environment using [venv](https://docs.python.org/3/library/venv.html) or [conda](https://www.anaconda.com/docs/getting-started/miniconda/main).

## Sign in to Hugging Face

We'll optimize Llama-3.2-1B-Instruct, which requires Hugging Face authentication:

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
> You'll need to [create a Hugging Face token](https://huggingface.co/docs/hub/security-tokens) and [directly request access](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) to the model.

## Compile the model

Run the Olive `auto-opt` command to download, convert to ONNX, quantize, and optimize the model:

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
> Compilation takes ~60 seconds plus download time.

### Key parameters

| Parameter | Description |
|-----------|-------------|
| `model_name_or_path` | Model source: Hugging Face ID, local path, or Azure AI Model registry ID |
| `output_path` | Where to save the optimized model |
| `device` | Target hardware: `cpu`, `gpu`, or `npu` |
| `provider` | Execution provider (e.g., `CPUExecutionProvider`, `CUDAExecutionProvider`) |
| `precision` | Model precision: `fp16`, `fp32`, `int4`, or `int8` |
| `use_ort_genai` | Creates inference configuration files |

You can substitute any model from Hugging Face or a local path - Olive handles the conversion, optimization, and quantization automatically.

## Rename the output model

Olive places files in a generic `model` directory. Rename it to make it easier to use:

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

## Run the model

You can run your compiled model through:

### Using the Foundry Local CLI

First, point Foundry Local to your models directory:

### [Bash](#tab/Bash)
```bash
foundry cache cd models
foundry cache ls  # should show llama-3.2
foundry model run llama-3.2 --verbose
```

### [PowerShell](#tab/PowerShell)
```powershell
foundry cache cd models
foundry cache ls  # should show llama-3.2
foundry model run llama-3.2 --verbose
```
---

### Using the REST API

### [Bash](#tab/Bash)
```bash
curl -X POST http://localhost:5272/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "llama-3.2",
    "messages": [{"role": "user", "content": "What is the capital of France?"}],
    "temperature": 0.7,
    "max_tokens": 50,
    "stream": true
}'
```

### [PowerShell](#tab/PowerShell)
```powershell
Invoke-RestMethod -Uri http://localhost:5272/v1/chat/completions `
    -Method Post `
    -ContentType "application/json" `
    -Body '{
        "model": "llama-3.2",
        "messages": [{"role": "user", "content": "What is the capital of France?"}],
        "temperature": 0.7,
        "max_tokens": 50,
        "stream": true
    }'
```
---

### Using the OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:5272/v1",
    api_key="none",  # required but not used
)

stream = client.chat.completions.create(
    model="llama-3.2",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    temperature=0.7,
    max_tokens=50,
    stream=True,
)

for event in stream:
    print(event.choices[0].delta.content, end="", flush=True)
print("\n\n")
```

> [!TIP]
> You can use any language that supports HTTP requests. See [Integrate with Inferencing SDKs](integrate-with-inference-sdks.md) for more options.

## Next steps

- [Learn more about Olive](https://microsoft.github.io/Olive/)
- [Integrate Foundry Local with Inferencing SDKs](integrate-with-inference-sdks.md)