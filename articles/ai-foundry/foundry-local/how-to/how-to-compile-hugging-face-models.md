---
title: Compile Hugging Face models to run on Foundry Local
titleSuffix: Foundry Local
description: Learn Compile and run Hugging Face models with Foundry Local.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.date: 10/01/2025
ai-usage: ai-assisted
---

# Compile Hugging Face models to run on Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local runs ONNX models on your device with high performance. Although the model catalog offers precompiled options out of the box, any model in the ONNX format works.

Use [Olive](https://microsoft.github.io/Olive) to compile models in Safetensor or PyTorch format to ONNX. Olive optimizes models for ONNX, making them suitable for deployment in Foundry Local. It uses techniques like quantization and graph optimization to improve performance.

This guide shows how to:

> [!div class="checklist"]
>
> - Convert and optimize models from Hugging Face to run in Foundry Local. The examples use the `Llama-3.2-1B-Instruct` model, but any generative AI model from Hugging Face works.
> - Run your optimized models with Foundry Local.

## Prerequisites

- Python 3.10 or later

## Install Olive

[Olive](https://github.com/microsoft/olive) optimizes models and converts them to the ONNX format.

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
> Install Olive in a virtual environment with [venv](https://docs.python.org/3/library/venv.html) or [conda](https://www.anaconda.com/docs/getting-started/miniconda/main).

## Sign in to Hugging Face

The `Llama-3.2-1B-Instruct` model requires Hugging Face authentication.

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
> [Create a Hugging Face token](https://huggingface.co/docs/hub/security-tokens) and [request model access](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) before proceeding.

## Compile the model

### Step 1: Run the Olive auto-opt command

Use the Olive `auto-opt` command to download, convert, quantize, and optimize the model:

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
> The compilation process takes about 60 seconds, plus download time.

The command uses the following parameters:

| Parameter            | Description                                                                       |
| -------------------- | --------------------------------------------------------------------------------- |
| `model_name_or_path` | Model source: Hugging Face ID, local path, or Azure AI Model registry ID           |
| `output_path`        | Where to save the optimized model                                                 |
| `device`             | Target hardware: `cpu`, `gpu`, or `npu`                                           |
| `provider`           | Execution provider (for example, `CPUExecutionProvider`, `CUDAExecutionProvider`) |
| `precision`          | Model precision: `fp16`, `fp32`, `int4`, or `int8`                                |
| `use_ort_genai`      | Creates inference configuration files                                             |

> [!TIP]
> If you have a local copy of the model, you can use a local path instead of the Hugging Face ID. For example, `--model_name_or_path models/llama-3.2-1B-Instruct`. Olive handles the conversion, optimization, and quantization automatically.

### Step 2: Rename the output model

Olive creates a generic `model` directory. Rename it for easier reuse:

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

### Step 3: Create chat template file

A chat template is a structured format that defines how input and output messages are processed for a conversational AI model. It specifies the roles (for example, system, user, assistant) and the structure of the conversation, ensuring that the model understands the context and generates appropriate responses.

Foundry Local requires a chat template JSON file named `inference_model.json` to generate responses. The template includes the model name and a `PromptTemplate` object. The object contains a `{Content}` placeholder that Foundry Local injects at runtime with the user prompt.

```json
{
  "Name": "llama-3.2",
  "PromptTemplate": {
    "assistant": "{Content}",
    "prompt": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nCutting Knowledge Date: December 2023\nToday Date: 26 Jul 2024\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{Content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
  }
}
```

Create the chat template file with the `apply_chat_template` method from the Hugging Face library:

> [!NOTE]
> This example uses the Hugging Face library (a dependency of Olive) to create a chat template. If you're using the same Python virtual environment, you don't need to install it. In a different environment, install it with `pip install transformers`.

```python
# generate_inference_model.py
# This script generates the inference_model.json file for the Llama-3.2 model.
import json
import os
from transformers import AutoTokenizer

model_path = "models/llama/llama-3.2"

tokenizer = AutoTokenizer.from_pretrained(model_path)
chat = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "{Content}"},
]


template = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

json_template = {
  "Name": "llama-3.2",
  "PromptTemplate": {
    "assistant": "{Content}",
    "prompt": template
  }
}

json_file = os.path.join(model_path, "inference_model.json")

with open(json_file, "w") as f:
    json.dump(json_template, f, indent=2)
```

Run the script using:

```bash
python generate_inference_model.py
```

## Run the model

Run your compiled model with the Foundry Local CLI, REST API, or OpenAI Python SDK. First, change the model cache directory to the models directory you created in the previous step:

### [Bash](#tab/Bash)

```bash
foundry cache cd models
foundry cache ls  # should show llama-3.2
```

### [PowerShell](#tab/PowerShell)

```powershell
foundry cache cd models
foundry cache ls  # should show llama-3.2
```
---

> [!CAUTION]
> Change the model cache back to the default directory when you're done:
> 
> ```bash
> foundry cache cd ./foundry/cache/models
> ```


### Using the Foundry Local CLI

### [Bash](#tab/Bash)

```bash
foundry model run llama-3.2 --verbose
```

### [PowerShell](#tab/PowerShell)

```powershell
foundry model run llama-3.2 --verbose
```
---

### Using the OpenAI Python SDK

Use the OpenAI Python SDK to interact with the Foundry Local REST API. Install it with:

```bash
pip install openai
pip install foundry-local-sdk
```

Then run the model with the following code:

```python
import openai
from foundry_local import FoundryLocalManager

modelId = "llama-3.2"

# Create a FoundryLocalManager instance. This starts the Foundry Local service if it's not already running and loads the specified model.
manager = FoundryLocalManager(modelId)

# The remaining code uses the OpenAI Python SDK to interact with the local model.

# Configure the client to use the local Foundry service
client = openai.OpenAI(
    base_url=manager.endpoint,
    api_key=manager.api_key  # API key is not required for local usage
)

# Set the model to use and generate a streaming response
stream = client.chat.completions.create(
    model=manager.get_model_info(modelId).id,
    messages=[{"role": "user", "content": "What is the golden ratio?"}],
    stream=True
)

# Print the streaming response
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

> [!TIP]
> Use any language that supports HTTP requests. For more information, see [Integrated inferencing SDKs with Foundry Local](../how-to/how-to-integrate-with-inference-sdks.md).

## Reset the model cache

After you finish using the custom model, reset the model cache to the default directory:

```bash
foundry cache cd ./foundry/cache/models
```

## Related content

- [Olive documentation](https://microsoft.github.io/Olive/)
- [Integrate inferencing SDKs with Foundry Local](how-to-integrate-with-inference-sdks.md)
