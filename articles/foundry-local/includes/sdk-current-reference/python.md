---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 07/17/2025
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Python SDK Reference

### Project setup

Install the Python package:

```bash
pip install foundry-local-sdk
```

> [!NOTE]
> The `foundry-local-sdk` package requires Python 3.11 or later.

[!INCLUDE [project-setup](../python-project-setup.md)]

### Quickstart

Use this snippet to verify that the SDK can initialize and access the local model catalog.

```python
import asyncio
from foundry_local_sdk import Configuration, FoundryLocalManager


async def main():
    config = Configuration(app_name="app-name")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    models = manager.catalog.list_models()
    print(f"Models available: {len(models)}")


if __name__ == "__main__":
    asyncio.run(main())
```

This example prints the number of models available for your hardware.

### Samples

- For sample applications that demonstrate how to use the Foundry Local Python SDK, see the [Foundry Local SDK Samples GitHub repository](https://aka.ms/foundrylocalSDK).

### Configuration

The `Configuration` class allows you to customize the SDK behavior:

```python
from foundry_local_sdk import Configuration

config = Configuration(
    app_name="app-name",
    log_level="info",
    model_cache_dir="./foundry_local_data/model_cache",
    web={"urls": "http://127.0.0.1:55588"},
)
```

| Parameter | Type | Description |
| --- | --- | --- |
| `app_name` | `str` | Name of your application. |
| `log_level` | `str` | Logging level (for example, `"info"`, `"debug"`). |
| `model_cache_dir` | `str` | Directory for cached models. |
| `web` | `dict` | Web service configuration with `urls` key. |

### Core API

| Method | Description |
| --- | --- |
| `FoundryLocalManager.initialize(config)` | Initialize the singleton manager with a `Configuration`. |
| `FoundryLocalManager.instance` | Access the initialized manager instance. |
| `manager.catalog.list_models()` | List all available models in the catalog. |
| `manager.catalog.get_model(alias)` | Get a model by alias. |
| `manager.catalog.get_cached_models()` | List models in the local cache. |
| `manager.catalog.get_loaded_models()` | List models currently loaded. |
| `model.download(progress_callback)` | Download the model (skips if cached). |
| `model.load()` | Load the model for inference. |
| `model.unload()` | Unload the model. |
| `model.is_cached` | Check if the model is cached locally. |
| `model.is_loaded` | Check if the model is loaded. |

### Native Chat Completions API

After loading a model, get a chat client:

```python
client = model.get_chat_client()
```

| Method | Description |
| --- | --- |
| `client.complete_chat(messages)` | Generate a complete chat response. |
| `client.complete_streaming_chat(messages)` | Stream chat response chunks. |

### Native Audio Transcription API

After loading a Whisper model, get an audio client:

```python
audio_client = model.get_audio_client()
```

| Method | Description |
| --- | --- |
| `audio_client.transcribe(file_path)` | Transcribe an audio file. Returns an object with a `text` property. |

References:

- [Transcribe audio files with Foundry Local](../../how-to/how-to-transcribe-audio.md)
- [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md)
- [Use chat completions via REST server](../../how-to/how-to-integrate-with-inference-sdks.md)
