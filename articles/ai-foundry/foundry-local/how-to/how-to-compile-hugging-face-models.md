---
title: Compile Hugging Face models to run on Foundry Local
titleSuffix: Foundry Local
description: Learn Compile and run Hugging Face models with Foundry Local.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: how-to
ms.date: 02/12/2025
ms.author: samkemp
author: samuel100
---

# Compile Hugging Face models to run on Foundry Local

Foundry Local runs ONNX models on your device with high performance. While the model catalog offers _out-of-the-box_ precompiled options, you can use any model in the ONNX format.

To compile existing models in Safetensor or PyTorch format into the ONNX format, you can use [Olive](https://microsoft.github.io/Olive). Olive is a tool that optimizes models to ONNX format, making them suitable for deployment in Foundry Local. It uses techniques like _quantization_ and _graph optimization_ to improve performance.

This guide shows you how to:

> [!div class="checklist"]
>
> - **Convert and optimize** models from Hugging Face to run in Foundry Local. You'll use the `Llama-3.2-1B-Instruct` model as an example, but you can use any generative AI model from Hugging Face.
> - **Run** your optimized models with Foundry Local

## Prerequisites

- Python 3.10 or later

## Install Olive

[Olive](https://github.com/microsoft/olive) is a tool that optimizes models to ONNX format.

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
> For best results, install Olive in a virtual environment using [venv](https://docs.python.org/3/library/venv.html) or [conda](https://www.anaconda.com/docs/getting-started/miniconda/main).

## Sign in to Hugging Face

You optimize the `Llama-3.2-1B-Instruct` model, which requires Hugging Face authentication:

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
> You must first [create a Hugging Face token](https://huggingface.co/docs/hub/security-tokens) and [request model access](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) before proceeding.

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
> The compilation process takes approximately 60 seconds, plus extra time for model download.

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

### Step 3: Create chat template file

A chat template is a structured format that defines how input and output messages are processed for a conversational AI model. It specifies the roles (for example, system, user, assistant) and the structure of the conversation, ensuring that the model understands the context and generates appropriate responses.

Foundry Local requires a chat template JSON file called `inference_model.json` in order to generate the appropriate responses. The template properties are the model name and a `PromptTemplate` object, which contains a `{Content}` placeholder that Foundry Local injects at runtime with the user prompt.

```json
{
  "Name": "llama-3.2",
  "PromptTemplate": {
    "assistant": "{Content}",
    "prompt": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nCutting Knowledge Date: December 2023\nToday Date: 26 Jul 2024\n\nYou are a helpful assistant.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{Content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
  }
}
```

To create the chat template file, you can use the `apply_chat_template` method from the Hugging Face library:

> [!NOTE]
> The following example uses the Python Hugging Face library to create a chat template. The Hugging Face library is a dependency for Olive, so if you're using the same Python virtual environment you don't need to install. If you're using a different environment, install the library with `pip install transformers`.

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

You can run your compiled model using the Foundry Local CLI, REST API, or OpenAI Python SDK. First, change the model cache directory to the models directory you created in the previous step:

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
> Remember to change the model cache back to the default directory when you're done by running:
> 
> ```bash 
> foundry cache cd ./foundry/cache/models.
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

The OpenAI Python SDK is a convenient way to interact with the Foundry Local REST API. You can install it using:

```bash
pip install openai
pip install foundry-local-sdk
```

Then, you can use the following code to run the model:

```python
import openai
from foundry_local import FoundryLocalManager

modelId = "llama-3.2"

# Create a FoundryLocalManager instance. This will start the Foundry 
# Local service if it is not already running and load the specified model.
manager = FoundryLocalManager(modelId)

# The remaining code us es the OpenAI Python SDK to interact with the local model.

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
> You can use any language that supports HTTP requests. For more information, read the [Integrated inferencing SDKs with Foundry Local](../how-to/how-to-integrate-with-inference-sdks.md) article.

## Finishing up

After you're done using the custom model, you should reset the model cache to the default directory using:

```bash
foundry cache cd ./foundry/cache/models
```

## Next steps

- [Learn more about Olive](https://microsoft.github.io/Olive/)
- [Integrate inferencing SDKs with Foundry Local](how-to-integrate-with-inference-sdks.md)
