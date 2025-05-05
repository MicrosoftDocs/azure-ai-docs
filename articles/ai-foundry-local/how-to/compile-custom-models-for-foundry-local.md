---
title: Compile custom models for Foundry Local using Olive AI
description: Learn how to optimize and compile your own models for AI Foundry Local using Olive AI and ONNX Runtime.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 04/21/2025
ms.author: samkemp
author: samuel100
---

# Compile custom models for Foundry Local using Olive AI

AI Foundry Local enables you to run large language models (LLMs) directly on your device for privacy, cost savings, and low-latency inference. To use your own models with Foundry Local, you need to convert and optimize them into the ONNX format. Olive AI is the recommended tool for this process.

This guide walks you through optimizing a Hugging Face or PyTorch model for Foundry Local using Olive’s auto-opt command.

## Prerequisites

- Python 3.8+
- Olive AI installed (`pip install olive-ai`)
- ONNX Runtime installed (`pip install onnxruntime-genai`)
- (Optional) Hugging Face account and access token for gated models

## 1. Authenticate with Hugging Face (if needed)

If your model is gated (e.g., Llama 3.2), you must log in to Hugging Face:

```sh
huggingface-cli login --token {YOUR_HF_TOKEN}
```

Refer to [Hugging Face documentation](https://huggingface.co/docs/hub/security-tokens) for details on obtaining a token.

## 2. Optimize Your Model with Olive

Use Olive’s `auto-opt` command to download, convert, and optimize your model. For example, to optimize the Llama-3.2-1B-Instruct model:

```sh
olive auto-opt \
  --model_name_or_path meta-llama/Llama-3.2-1B-Instruct \
  --trust_remote_code \
  --output_path models/llama/ao \
  --device cpu \
  --provider CPUExecutionProvider \
  --use_ort_genai \
  --precision int4 \
  --log_level 1
```

### Key Arguments

- `--model_name_or_path`: Hugging Face repo ID, local path, or Azure Model Catalog ID.
- `--output_path`: Where to save the optimized ONNX model.
- `--device`: Target device (`cpu`, `gpu`, etc.).
- `--provider`: Hardware provider (e.g., `CPUExecutionProvider`, `CUDAExecutionProvider`).
- `--precision`: Model precision (`fp16`, `fp32`, `int4`, `int8`). Lower precision reduces size and increases speed.
- `--use_ort_genai`: Prepares the model for ONNX Runtime’s Generate API.

You can substitute any compatible Hugging Face model or a local model path for `--model_name_or_path`.

## 3. Run Inference with ONNX Runtime

After optimization, you can run inference using ONNX Runtime. Here’s a sample Python script for a simple chat interface:

```python
import onnxruntime_genai as og

model_folder = "models/llama/ao/model"

model = og.Model(model_folder)
tokenizer = og.Tokenizer(model)
tokenizer_stream = tokenizer.create_stream()

search_options = {'max_length': 200}
system_prompt = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a helpful assistant<|eot_id|>"
system_tokens = tokenizer.encode(system_prompt)
chat_template = "<|start_header_id|>user<|end_header_id|>{input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

while True:
    text = input("Prompt (Use quit() to exit): ")
    if not text:
        print("Error, input cannot be empty")
        continue
    if text == "quit()":
        break
    prompt = f'{chat_template.format(input=text)}'
    input_tokens = tokenizer.encode(prompt)
    params = og.GeneratorParams(model)
    params.set_search_options(**search_options)
    generator = og.Generator(model, params)
    generator.append_tokens(system_tokens + input_tokens)
    print("\nOutput: ", end='', flush=True)
    try:
        while not generator.is_done():
            generator.generate_next_token()
            new_token = generator.get_next_tokens()[0]
            print(tokenizer_stream.decode(new_token), end='', flush=True)
    except KeyboardInterrupt:
        print("  --control+c pressed, aborting generation--")
    print("\n")
    del generator
```

Run the script with:

```sh
python app.py
```

## 4. Next steps

- Integrate your ONNX model with AI Foundry Local’s CLI or REST API (see [Get started with AI Foundry Local](../get-started.md)).
- Experiment with different models, devices, and providers for optimal performance.

---

**Note:** Since AI Foundry Local is not yet public, some integration details may change. This guide uses current Olive and ONNX Runtime best practices, which are expected to be compatible with Foundry Local upon release. For updates, refer to the official documentation as it becomes available.
