---
title: Compile custom models for Foundry Local using Olive AI
description: Learn how to optimize and compile your own models for Foundry Local using Olive AI and ONNX Runtime.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 04/21/2025
ms.author: samkemp
author: samuel100
---

# Compile custom models for Foundry Local using Olive AI

Foundry Local enables you to run large language models (LLMs) directly on your device for privacy, cost savings, and low-latency inference. To use your own models with Foundry Local, you need to convert and optimize them into the ONNX format. Olive AI is the recommended tool for this process.

This guide walks you through optimizing a PyTorch model for Foundry Local using Olive’s auto-opt command.

## Prerequisites

- Python 3.8+
- Olive AI installed (`pip install olive-ai`)
- ONNX Runtime installed (`pip install onnxruntime-genai`)

## 1. Optimize Your Model with Olive

Use Olive’s `auto-opt` command to download, convert, and optimize your model. For example, to optimize the Llama-3.2-1B-Instruct model:

```sh
olive auto-opt \
  --model_name_or_path ./Qwen3 \
  --trust_remote_code \
  --output_path models/qwen/ao \
  --device cpu \
  --provider CPUExecutionProvider \
  --use_ort_genai \
  --precision int4 \
  --log_level 1
```

### Key Arguments

- `--model_name_or_path`: local path
- `--output_path`: Where to save the optimized ONNX model.
- `--device`: Target device (`cpu`, `gpu`, etc.).
- `--provider`: Hardware provider (e.g., `CPUExecutionProvider`, `CUDAExecutionProvider`).
- `--precision`: Model precision (`fp16`, `fp32`, `int4`, `int8`). Lower precision reduces size and increases speed.
- `--use_ort_genai`: Prepares the model for ONNX Runtime’s Generate API (required for Foundry Local).

## 2. Run Inference with Foundry Local

You can run your compiled model using the Foundry Local CLI, REST API, or OpenAI Python SDK. First, change the model cache directory to the models directory you created in the previous step (or move the model to the default cache directory, found with `foundry cache location`).:

### [Bash](#tab/Bash)
```bash
foundry cache cd models
foundry cache ls  # should show Qwen3
```

### [PowerShell](#tab/PowerShell)
```powershell
foundry cache cd models
foundry cache ls  # should show Qwen3
```
---

### Using the Foundry Local CLI

### [Bash](#tab/Bash)
```bash
foundry model run Qwen3 --verbose
```

### [PowerShell](#tab/PowerShell)
```powershell
foundry model run Qwen3 --verbose
```
---

### Using the REST API

### [Bash](#tab/Bash)
```bash
curl -X POST http://localhost:5272/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
    "model": "Qwen3",
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
        "model": "Qwen3",
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
    model="Qwen3",
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



## 3. Next steps

- Integrate your ONNX model with Foundry Local’s CLI or REST API (see [Get started with Foundry Local](../get-started.md)).
- Experiment with different models, devices, and providers for optimal performance.

---

**Note:** Since Foundry Local is not yet public, some integration details may change. This guide uses current Olive and ONNX Runtime best practices, which are expected to be compatible with Foundry Local upon release. For updates, refer to the official documentation as it becomes available.
