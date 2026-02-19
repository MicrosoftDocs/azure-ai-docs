---
title: Compile Hugging Face models to run on Foundry Local
titleSuffix: Foundry Local
description: Learn how to compile and run Hugging Face models with Foundry Local.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.date: 01/06/2026
ai-usage: ai-assisted
---

# Compile Hugging Face models to run on Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local runs ONNX models on your device. Use [Olive](https://microsoft.github.io/Olive/) to convert and optimize models from Hugging Face (Safetensors or PyTorch) into ONNX so you can run them with Foundry Local.

> [!IMPORTANT]
> The Olive CLI and optimization settings change over time, and a single command line example might not work for every model, device, or execution provider.
>
> For the most reliable, up-to-date examples, start with the [Olive Recipes repository](https://github.com/microsoft/olive-recipes). It includes a dedicated recipe for [`meta-llama/Llama-3.2-1B-Instruct`](https://github.com/microsoft/olive-recipes/tree/main/meta-llama-Llama-3.2-1B-Instruct).
>
> - For Olive CLI configs for this model, see the recipe folder: <https://github.com/microsoft/olive-recipes/tree/main/meta-llama-Llama-3.2-1B-Instruct/olive>.
> - For a Foundry Local-oriented artifact layout (for example, an `inference_model.json` you can reuse), see: <https://github.com/microsoft/olive-recipes/tree/main/meta-llama-Llama-3.2-1B-Instruct/aitk>.

This guide shows how to:

> [!div class="checklist"]
>
> - Convert and optimize models from Hugging Face to run in Foundry Local. The examples use the `Llama-3.2-1B-Instruct` model, but many Hugging Face models can work.
> - Run your optimized models with Foundry Local.

## Prerequisites

- Foundry Local installed. For installation instructions, see [Get started with Foundry Local](../get-started.md).
- Python 3.10 or later
- A Hugging Face account and token with access to `meta-llama/Llama-3.2-1B-Instruct`

Verify your tools:

### [Bash](#tab/Bash)

```bash
python --version
foundry --version
olive --help
huggingface-cli --help
```

### [PowerShell](#tab/PowerShell)

```powershell
python --version
foundry --version
olive --help
huggingface-cli --help
```

---

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
> Install Olive in a virtual environment by using [venv](https://docs.python.org/3/library/venv.html) or [conda](https://www.anaconda.com/docs/getting-started/miniconda/main).

Expected result: `olive auto-opt --help` prints usage information.

References:

- Reference: [Olive documentation](https://microsoft.github.io/Olive/)
- Reference: [Olive repository](https://github.com/microsoft/olive)

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

> [!TIP]
> If `huggingface-cli` isn't found, install it by running `pip install -U huggingface_hub`.

Expected result: The authentication command finishes without errors.

References:

- Reference: [Hugging Face user access tokens](https://huggingface.co/docs/hub/security-tokens)

## Compile the model

### Manual example (might require adjustments)

#### Step 1: Run the Olive auto-opt command

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

Expected result: The command creates the `models/llama/model` directory.

The command uses the following parameters:

| Parameter | Description |
| --- | --- |
| `model_name_or_path` | Model source: Hugging Face ID, local path, or Azure AI Model registry ID |
| `output_path` | Where to save the optimized model |
| `device` | Target hardware: `cpu`, `gpu`, or `npu` |
| `provider` | Execution provider (for example, `CPUExecutionProvider`, `CUDAExecutionProvider`) |
| `precision` | Model precision: `fp16`, `fp32`, `int4`, or `int8` |
| `use_ort_genai` | Creates inference configuration files |

> [!TIP]
> If you have a local copy of the model, use a local path instead of the Hugging Face ID. For example, `--model_name_or_path models/llama-3.2-1B-Instruct`. Olive handles the conversion, optimization, and quantization automatically.

References:

- Reference: [Olive documentation](https://microsoft.github.io/Olive/)

#### Step 2: Rename the output model

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

Expected result: The `models/llama/llama-3.2` directory exists.

#### Step 3: Create chat template file

Foundry Local requires a chat template JSON file named `inference_model.json` in the model directory. Foundry Local injects the user prompt into the template using the `{Content}` placeholder at runtime.

Create the chat template file by using the `apply_chat_template` method from the Hugging Face library:

> [!NOTE]
> This example uses the Hugging Face library (a dependency of Olive) to create a chat template. If you're using the same Python virtual environment, you don't need to install it. In a different environment, install it by running `pip install transformers`.

```python
# generate_inference_model.py
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

Run the script by using the following command:

```bash
python generate_inference_model.py
```

Expected result: `models/llama/llama-3.2/inference_model.json` exists.

References:

- Reference: [Transformers documentation](https://huggingface.co/docs/transformers/index)

## Run the model

Run your compiled model by using the Foundry Local CLI, REST API, or OpenAI Python SDK. First, change the model cache directory to the models directory you created in the previous step:

### [Bash](#tab/Bash)

```bash
foundry cache cd models
foundry cache list  # should show llama-3.2
```

### [PowerShell](#tab/PowerShell)

```powershell
foundry cache cd models
foundry cache list  # should show llama-3.2
```
---

> [!CAUTION]
> Change the model cache back to the default directory when you're done:
> 
> ```bash
> foundry cache cd ./foundry/cache/models
> ```
>
> If you're not sure what your current cache directory is, run `foundry cache location`.

Expected result: `foundry cache list` shows `llama-3.2`.

References:

- Reference: [Get started with Foundry Local](../get-started.md)
- Reference: [Foundry Local CLI reference](../reference/reference-cli.md)


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

Expected result: Foundry Local starts (if needed) and you can interact with the model in your terminal.

References:

- Reference: [Foundry Local CLI reference](../reference/reference-cli.md)

### Using the OpenAI Python SDK

Use the OpenAI Python SDK to interact with the Foundry Local REST API. Install it by using the following command:

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

Expected result: The script prints a streamed response from the local model.

> [!TIP]
> Use any language that supports HTTP requests. For more information, see [Integrated inferencing SDKs with Foundry Local](../how-to/how-to-integrate-with-inference-sdks.md).

References:

- Reference: [Foundry Local SDK reference](../reference/reference-sdk.md)
- Reference: [Use chat completions via REST server with Foundry Local](../how-to/how-to-integrate-with-inference-sdks.md)

## Reset the model cache

After you finish using the custom model, reset the model cache to the default directory:

```bash
foundry cache cd ./foundry/cache/models
```

References:

- Reference: [Foundry Local CLI reference](../reference/reference-cli.md)

## Troubleshooting

- If the `foundry` command isn't found, install Foundry Local. See [Get started with Foundry Local](../get-started.md).
- If Foundry Local starts but requests fail, run `foundry service restart`. For an example error and fix, see the troubleshooting section in [Get started with Foundry Local](../get-started.md).
- If the `huggingface-cli` command isn't found, install it by running `pip install -U huggingface_hub`, and then run `huggingface-cli login`.
- If `olive auto-opt` fails with an authentication or access error, confirm your token and model access request is approved.

## Related content

- [Olive documentation](https://microsoft.github.io/Olive/)
- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Get started with Foundry Local](../get-started.md)
- [Foundry Local CLI reference](../reference/reference-cli.md)
