---
title: "Compile Hugging Face models to run on Foundry Local"
titleSuffix: Foundry Local
description: "Learn how to compile and run Hugging Face models with Foundry Local."
ms.service: microsoft-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
author: jonburchel
reviewer: samuel100
ms.date: 01/06/2026
ai-usage: ai-assisted
zone_pivot_groups: foundry-local-sdk
---

# Compile Hugging Face models to run on Foundry Local

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

- Python 3.10 or later (required for Olive compilation)
- A Hugging Face account and token with access to `meta-llama/Llama-3.2-1B-Instruct`

## Install Olive

[Olive](https://github.com/microsoft/olive) optimizes models and converts them to the ONNX format.

```bash
pip install olive-ai[auto-opt]
```

> [!TIP]
> Install Olive in a virtual environment by using [venv](https://docs.python.org/3/library/venv.html) or [conda](https://www.anaconda.com/docs/getting-started/miniconda/main).

Verify the installation: `olive auto-opt --help` prints usage information.

## Sign in to Hugging Face

The `Llama-3.2-1B-Instruct` model requires Hugging Face authentication.

```bash
hf auth login
```

> [!NOTE]
> [Create a Hugging Face token](https://huggingface.co/docs/hub/security-tokens) and [request model access](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct) before proceeding.

> [!TIP]
> If `hf` isn't found, install it by running `pip install -U huggingface_hub`.

## Compile the model

This section walks through a manual compilation. The Olive `auto-opt` command downloads, converts, quantizes, and optimizes the model.

> [!NOTE]
> This is a manual example that might require adjustments for different models or hardware targets.

1. Run the Olive `auto-opt` command:

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

    > [!NOTE]
    > The compilation process takes about 60 seconds, plus download time.

1. Rename the output directory. Olive creates a generic `model` directory — rename it for easier reuse:

    ```bash
    cd models/llama
    mv model llama-3.2
    ```

1. Create the chat template file. Foundry Local requires a chat template JSON file named `inference_model.json` in the model directory. The `{Content}` placeholder is injected with the user prompt at runtime.

    > [!NOTE]
    > This example uses the Hugging Face `transformers` library (a dependency of Olive) to create the template. In a different environment, install it by running `pip install transformers`.

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
      "Name": "llama-3.2:1",
      "PromptTemplate": {
        "assistant": "{Content}",
        "prompt": template
      }
    }

    json_file = os.path.join(model_path, "inference_model.json")

    with open(json_file, "w") as f:
        json.dump(json_template, f, indent=2)
    ```

    Run the script:

    ```bash
    python generate_inference_model.py
    ```

    Verify the file exists: `models/llama/llama-3.2/inference_model.json`.

## Run the compiled model

::: zone pivot="programming-language-csharp"

Use the Foundry Local C# SDK to load and run your compiled model with the native chat completions API. This approach doesn't require a REST server — the SDK communicates directly with the runtime.

### Prerequisites

- [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0) or later

### Set up the project

[!INCLUDE [project-setup](../includes/csharp-project-setup.md)]

### Run inference on the compiled model

Replace the contents of `Program.cs` with the following code:

```csharp
using Microsoft.AI.Foundry.Local;
using Betalgo.Ranul.OpenAI.ObjectModels.RequestModels;
using Microsoft.Extensions.Logging;

CancellationToken ct = CancellationToken.None;

// Point ModelCacheDir at the directory containing your compiled model
var config = new Configuration
{
    AppName = "run-compiled-model",
    LogLevel = Microsoft.AI.Foundry.Local.LogLevel.Information,
    ModelCacheDir = "../models/llama"
};

using var loggerFactory = LoggerFactory.Create(builder =>
{
    builder.SetMinimumLevel(Microsoft.Extensions.Logging.LogLevel.Information);
});
var logger = loggerFactory.CreateLogger<Program>();

await FoundryLocalManager.CreateAsync(config, logger);
var mgr = FoundryLocalManager.Instance;

var catalog = await mgr.GetCatalogAsync();

// List cached models to find your compiled model
var cachedModels = await catalog.GetCachedModelsAsync();
Console.WriteLine("Cached models:");
foreach (var m in cachedModels)
{
    Console.WriteLine($"  {m.Id}");
}

// Select your compiled model from the cached list
var model = cachedModels.FirstOrDefault(m => m.Id.Contains("llama-3.2:1"))
    ?? throw new Exception("Compiled model not found. Verify the ModelCacheDir path.");

await model.LoadAsync();

// Use native chat completions
var chatClient = await model.GetChatClientAsync();

List<ChatMessage> messages = new()
{
    new ChatMessage { Role = "user", Content = "What is the golden ratio?" }
};

var streamingResponse = chatClient.CompleteChatStreamingAsync(messages, ct);
await foreach (var chunk in streamingResponse)
{
    Console.Write(chunk.Choices[0].Message.Content);
    Console.Out.Flush();
}
Console.WriteLine();

await model.UnloadAsync();
```

Run the application:

```bash
dotnet run
```

::: zone-end

::: zone pivot="programming-language-javascript"

Use the Foundry Local JavaScript SDK to load and run your compiled model with the native chat completions API.

### Prerequisites

- [Node.js 20](https://nodejs.org/en/download/) or later installed.

### Set up the project

[!INCLUDE [project-setup](../includes/javascript-project-setup.md)]

### Run inference on the compiled model

Copy and paste the following code into a JavaScript file named `app.js`:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';

// Initialize the Foundry Local SDK with custom model cache directory
const manager = FoundryLocalManager.create({
    appName: 'run-compiled-model',
    logLevel: 'info',
    modelCacheDir: '../models/llama'
});

// List cached models to find your compiled model
const cachedModels = await manager.catalog.getCachedModels();
console.log('Cached models:');
for (const m of cachedModels) {
    console.log(`  ${m.id}`);
}

// Select your compiled model from the cached list
const model = cachedModels.find(m => m.id.includes('llama-3.2:1'));
if (!model) {
    throw new Error('Compiled model not found. Verify the modelCacheDir path.');
}

// Load the model
await model.load();

// Create a chat client
const chatClient = model.createChatClient();

// Generate a response
const completion = await chatClient.completeChat([
    { role: 'user', content: 'What is the golden ratio?' }
]);

console.log(completion.choices[0]?.message?.content);

// Unload the model
await model.unload();
```

Run the application:

```bash
node app.js
```

::: zone-end

::: zone pivot="programming-language-python"

Use the Foundry Local Python SDK to load and run your compiled model with the native chat completions API.

### Prerequisites

- [Python 3.11](https://www.python.org/downloads/) or later installed.
- `foundry-local-sdk` package installed (`pip install foundry-local-sdk`).

### Run inference on the compiled model

Copy and paste the following code into a Python file named `app.py`:

```python
import asyncio
from foundry_local_sdk import Configuration, FoundryLocalManager


async def main():
    # Point model_cache_dir at the directory containing your compiled model
    config = Configuration(
        app_name="run-compiled-model",
        model_cache_dir="../models/llama",
    )
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    # List cached models to find your compiled model
    cached_models = manager.catalog.get_cached_models()
    print("Cached models:")
    for m in cached_models:
        print(f"  {m.id}")

    # Select your compiled model from the cached list
    model = next((m for m in cached_models if "llama-3.2:1" in m.id), None)
    if model is None:
        raise Exception("Compiled model not found. Verify the model_cache_dir path.")

    # Load the model
    model.load()

    # Get a chat client
    client = model.get_chat_client()

    # Stream the response
    messages = [{"role": "user", "content": "What is the golden ratio?"}]
    for chunk in client.complete_streaming_chat(messages):
        content = chunk.choices[0].message.content
        if content:
            print(content, end="", flush=True)
    print()

    # Tidy up - unload the model
    model.unload()


if __name__ == "__main__":
    asyncio.run(main())
```

Run the application:

```bash
python app.py
```

::: zone-end

::: zone pivot="programming-language-rust"

Use the Foundry Local Rust SDK to load and run your compiled model with the native chat completions API.

### Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).

### Set up the project

[!INCLUDE [project-setup](../includes/rust-project-setup.md)]

### Run inference on the compiled model

Replace the contents of `src/main.rs` with the following code:

```rust
use foundry_local_sdk::{
    ChatCompletionRequestMessage, ChatCompletionRequestUserMessage,
    FoundryLocalConfig, FoundryLocalManager,
};
use std::io::Write;
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Point model_cache_dir at the directory containing your compiled model
    let config = FoundryLocalConfig::new("run-compiled-model")
        .with_model_cache_dir("../models/llama");
    let manager = FoundryLocalManager::create(config)?;

    // List cached models to find your compiled model
    let cached_models = manager.catalog().get_cached_models().await?;
    println!("Cached models:");
    for m in &cached_models {
        println!("  {}", m.id());
    }

    // Select your compiled model from the cached list
    let model = cached_models
        .iter()
        .find(|m| m.id().contains("llama-3.2:1"))
        .ok_or_else(|| anyhow::anyhow!("Compiled model not found. Verify the model_cache_dir path."))?;

    // Load the model
    model.load().await?;

    // Create a chat client
    let client = model.create_chat_client().temperature(0.7).max_tokens(256);

    // Stream the response
    let messages: Vec<ChatCompletionRequestMessage> = vec![
        ChatCompletionRequestUserMessage::new("What is the golden ratio?").into(),
    ];

    let mut stream = client.complete_streaming_chat(&messages, None).await?;
    while let Some(chunk) = stream.next().await {
        let chunk = chunk?;
        if let Some(content) = &chunk.choices[0].message.content {
            print!("{}", content);
            std::io::stdout().flush()?;
        }
    }
    println!();

    // Tidy up - unload the model
    model.unload().await?;

    Ok(())
}
```

Run the application:

```bash
cargo run
```

::: zone-end

## Troubleshooting

- If `olive auto-opt` fails with an authentication or access error, confirm your Hugging Face token and that the model access request is approved.
- If the `hf` command isn't found, install it by running `pip install -U huggingface_hub`.
- If the compiled model isn't found in the cached models list, verify the `ModelCacheDir` path in your `Configuration` points to the parent directory that contains the model folder.
- If you encounter .NET build errors referencing `net9.0`, install the [.NET 9.0 SDK](https://dotnet.microsoft.com/download/dotnet/9.0).

## Related content

- [Olive documentation](https://microsoft.github.io/Olive/)
- [Olive Recipes repository](https://github.com/microsoft/olive-recipes)
- [Use native chat completions API with Foundry Local](../how-to/how-to-use-native-chat-completions.md)
- [Foundry Local SDK reference](../reference/reference-sdk-current.md)
- [Get started with Foundry Local](../get-started.md)
