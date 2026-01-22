---
title: Foundry Local REST API Reference
titleSuffix: Foundry Local
description: Complete reference guide for the Foundry Local REST API.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.author: nakersha
ms.reviewer: jonburchel
author: natke
reviewer: jonburchel
ms.topic: reference
ms.date: 11/24/2025
---

# Foundry Local REST API Reference

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

> [!CAUTION]
> This API refers to the REST API available in the Foundry Local CLI. This API is under active development and may include breaking changes without notice. We strongly recommend monitoring the changelog before building production applications.

## POST /v1/chat/completions

This endpoint processes chat completion requests.  
It's fully compatible with the [OpenAI Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create).

**Request Body:**

_---Standard OpenAI Properties---_

- `model` (string)  
  The specific model to use for completion.
- `messages` (array)  
  The conversation history as a list of messages.
  - Each message requires:
    - `role` (string)  
      The message sender's role. Must be `system`, `user`, or `assistant`.
    - `content` (string)  
      The actual message text.
- `temperature` (number, optional)  
  Controls randomness, ranging from 0 to 2. Higher values (0.8) create varied outputs, while lower values (0.2) create focused, consistent outputs.
- `top_p` (number, optional)  
  Controls token selection diversity from 0 to 1. A value of 0.1 means only the tokens in the top 10% probability are considered.
- `n` (integer, optional)  
  Number of alternative completions to generate for each input message.
- `stream` (boolean, optional)  
  When true, sends partial message responses as server-sent events, ending with a `data: [DONE]` message.
- `stop` (string or array, optional)  
  Up to 4 sequences that will cause the model to stop generating further tokens.
- `max_tokens` (integer, optional)  
  Maximum number of tokens to generate. For newer models, use `max_completion_tokens` instead.
- `max_completion_tokens` (integer, optional)  
  Maximum number of tokens the model can generate, including visible output and reasoning tokens.
- `presence_penalty` (number, optional)  
  Value between -2.0 and 2.0. Positive values encourage the model to discuss new topics by penalizing tokens that have already appeared.
- `frequency_penalty` (number, optional)  
  Value between -2.0 and 2.0. Positive values discourage repetition by penalizing tokens based on their frequency in the text.
- `logit_bias` (map, optional)  
  Adjusts the probability of specific tokens appearing in the completion.
- `user` (string, optional)  
  A unique identifier for your end-user that helps with monitoring and abuse prevention.
- `functions` (array, optional)  
  Available functions for which the model can generate JSON inputs.
  - Each function must include:
    - `name` (string)  
      Function name.
    - `description` (string)  
      Function description.
    - `parameters` (object)  
      Function parameters described as a JSON Schema object.
- `function_call` (string or object, optional)  
  Controls how the model responds to function calls.
  - If object, can include:
    - `name` (string, optional)  
      The name of the function to call.
    - `arguments` (object, optional)  
      The arguments to pass to the function.
- `metadata` (object, optional)  
  A dictionary of metadata key-value pairs.
- `top_k` (number, optional)  
  The number of highest probability vocabulary tokens to keep for top-k-filtering.
- `random_seed` (integer, optional)  
  Seed for reproducible random number generation.
- `ep` (string, optional)  
  Overwrite the provider for ONNX models. Supports: `"dml"`, `"cuda"`, `"qnn"`, `"cpu"`, `"webgpu"`.
- `ttl` (integer, optional)  
  Time to live in seconds for the model in memory.
- `tools` (object, optional)  
  Tools calculated for the request.

**Response body:**

- `id` (string)  
  Unique identifier for the chat completion.
- `object` (string)  
  The object type, always `"chat.completion"`.
- `created` (integer)  
  Creation timestamp in epoch seconds.
- `model` (string)  
  The model used for completion.
- `choices` (array)  
  List of completion choices, each containing:
  - `index` (integer)  
    The index of this choice.
  - `message` (object)  
    The generated message with:
    - `role` (string)  
      Always `"assistant"` for responses.
    - `content` (string)  
      The actual generated text.
  - `finish_reason` (string)  
    Why generation stopped (e.g., `"stop"`, `"length"`, `"function_call"`).
- `usage` (object)  
  Token usage statistics:
  - `prompt_tokens` (integer)  
    Tokens in the prompt.
  - `completion_tokens` (integer)  
    Tokens in the completion.
  - `total_tokens` (integer)  
    Total tokens used.

**Example:**

Request body
```json
  {
    "model": "qwen2.5-0.5b-instruct-generic-cpu",
    "messages": [
      {
        "role": "user",
        "content": "Hello, how are you?"
      }
    ],
    "temperature": 0.7,
    "top_p": 1,
    "n": 1,
    "stream": false,
    "stop": null,
    "max_tokens": 100,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "logit_bias": {},
    "user": "user_id_123",
    "functions": [],
    "function_call": null,
    "metadata": {}
  }
```

Response body

```json
  {
    "id": "chatcmpl-1234567890",
    "object": "chat.completion",
    "created": 1677851234,
    "model": "qwen2.5-0.5b-instruct-generic-cpu",
    "choices": [
      {
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "I'm doing well, thank you! How can I assist you today?"
        },
        "finish_reason": "stop"
      }
    ],
    "usage": {
      "prompt_tokens": 10,
      "completion_tokens": 20,
      "total_tokens": 30
    }
  }
```


## GET /openai/status

Get server status information.

**Response body:**

- `Endpoints` (array of strings)  
  The HTTP server binding endpoints.
- `ModelDirPath` (string)  
  Directory where local models are stored.
- `PipeName` (string)  
  The current NamedPipe server name.

**Example:**

Response body
```json
  {
    "Endpoints": ["http://localhost:5272"],
    "ModelDirPath": "/path/to/models",
    "PipeName": "inference_agent"
  }
```

## GET /foundry/list

Get a list of available Foundry Local models in the catalog.

**Response:**

- `models` (array)  
  Array of model objects. Each model includes:
  - `name`: The unique identifier for the model.
  - `displayName`: A human-readable name for the model, often the same as the name.
  - `providerType`: The type of provider hosting the model (for example, AzureFoundry).
  - `uri`: The resource URI pointing to the model's location in the registry.
  - `version`: The version number of the model.
  - `modelType`: The format or type of the model (for example, ONNX).
  - `promptTemplate`:
    - `assistant`: The template for the assistant's response.
    - `prompt`: The template for the user-assistant interaction.
  - `publisher`: The entity or organization that published the model.
  - `task`: The primary task the model is designed to perform (for example, chat completion).
  - `runtime`:
    - `deviceType`: The type of hardware the model is designed to run on (for example, CPU).
    - `executionProvider`: The execution provider used for running the model.
  - `fileSizeMb`: The size of the model file in megabytes.
  - `modelSettings`:
    - `parameters`: A list of configurable parameters for the model.
  - `alias`: An alternative name or shorthand for the model
  - `supportsToolCalling`: Indicates whether the model supports tool-calling functionality.
  - `license`: The license type under which the model is distributed.
  - `licenseDescription`: A detailed description or link to the license terms.
  - `parentModelUri`: The URI of the parent model from which this model is derived.


## GET /openai/models

Get a list of cached models, including local and registered external models.

**Response:**

- 200 OK  
  An array of model names as strings.

**Example:**

Response body

```json
  ["Phi-4-mini-instruct-generic-cpu", "phi-3.5-mini-instruct-generic-cpu"]
```

## POST /openai/download

Download a model from the catalog to local storage.

> [!NOTE]
> Large model downloads can take a long time. Set a high timeout for this request to avoid early termination.

**Request Body:**

- `model` (`WorkspaceInferenceModel` object)
  - `Uri` (string)  
    The model URI to download.
  - `Name` (string)
    The model name.
  - `ProviderType` (string, optional)  
    The provider type (for example, `"AzureFoundryLocal"`, `"HuggingFace"`).
  - `Path` (string, optional)  
    Remote path to the model files. For example, in a Hugging Face repository, this is the path to the model files.
  - `PromptTemplate` (`Dictionary<string, string>`, optional)  
    Includes:
    - `system` (string, optional)  
      The template for the system message.
    - `user` (string, optional)
      The template for the user's message.
    - `assistant` (string, optional)  
      The template for the assistant's response.
    - `prompt` (string, optional)  
      The template for the user-assistant interaction.
  - `Publisher` (string, optional)  
     The publisher of the model.
- `token` (string, optional)  
  Authentication token for protected models (GitHub or Hugging Face).
- `progressToken` (object, optional)  
  For AITK only. Token to track download progress.
- `customDirPath` (string, optional)  
  Custom download directory (used for CLI, not needed for AITK).
- `bufferSize` (integer, optional)  
  HTTP download buffer size in KB. No effect on NIM or Azure Foundry models.
- `ignorePipeReport` (boolean, optional)  
  If `true`, forces progress reporting via HTTP stream instead of pipe.
  Defaults to `false` for AITK and `true` for Foundry Local.

**Streaming Response:**

During download, the server streams progress updates in the format:

```text
("file name", percentage_complete)
```

**Final Response body:**

- `Success` (boolean)  
  Whether the download completed successfully.
- `ErrorMessage` (string, optional)  
  Error details if download failed.

**Example:**

Request URI

```http
POST /openai/download
```

Request body

Note that the version suffix must be supplied in the model name.

```json
{
  "model": {
    "Uri": "azureml://registries/azureml/models/Phi-4-mini-instruct-generic-cpu/versions/4",
    "ProviderType": "AzureFoundryLocal",
    "Name": "Phi-4-mini-instruct-generic-cpu:4",
    "Publisher": "",
    "PromptTemplate": {
      "system": "<|system|>{Content}<|end|>",
      "user": "<|user|>{Content}<|end|>",
      "assistant": "<|assistant|>{Content}<|end|>",
      "prompt": "<|user|>{Content}<|end|><|assistant|>"
    }
  }
}
```

Response stream

```text
  ("genai_config.json", 0.01)
  ("genai_config.json", 0.2)
  ("model.onnx.data", 0.5)
  ("model.onnx.data", 0.78)
  ...
  ("", 1)
```

Final response
```json
  {
    "Success": true,
    "ErrorMessage": null
  }
```

## GET /openai/load/{name}

Load a model into memory for faster inference.

**URI Parameters:**

- `name` (string)  
  The model name to load.

**Query Parameters:**

- `unload` (boolean, optional)  
  Whether to automatically unload the model after idle time. Defaults to `true`.
- `ttl` (integer, optional)  
  Time to live in seconds. If it's greater than 0, this value overrides the `unload` parameter.
- `ep` (string, optional)  
  Execution provider to run this model. Supports: `"dml"`, `"cuda"`, `"qnn"`, `"cpu"`, `"webgpu"`.  
  If not specified, uses settings from `genai_config.json`.

**Response:**

- 200 OK  
  Empty response body

**Example:**

Request URI

```http
  GET /openai/load/Phi-4-mini-instruct-generic-cpu?ttl=3600&ep=dml
```

## GET /openai/unload/{name}

Unload a model from memory.

**URI Parameters:**

- `name` (string)
  The model name to unload.

**Query Parameters:**

- `force` (boolean, optional)
  If `true`, ignores TTL settings and unloads immediately.

**Response:**

- 200 OK
  Empty response body

**Example:**

Request URI

```http
GET /openai/unload/Phi-4-mini-instruct-generic-cpu?force=true
````

## GET /openai/unloadall

Unloads all models from memory.

**Response:**

- 200 OK  
  Empty response body

## GET /openai/loadedmodels

Get the list of currently loaded models.

**Response:**

- 200 OK  
  An array of model names as strings.

**Example:**

Response body

```json
["Phi-4-mini-instruct-generic-cpu", "phi-3.5-mini-instruct-generic-cpu"]
```

## GET /openai/getgpudevice

Get the current GPU device ID.

**Response:**

- 200 OK  
  An integer representing the current GPU device ID.

## GET /openai/setgpudevice/{deviceId}

Set the active GPU device.

**URI Parameters:**

- `deviceId` (integer)  
  The GPU device ID to use.

**Response:**

- 200 OK  
  Empty response body

**Example:**

- Request URI
  ```http
  GET /openai/setgpudevice/1
  ```

## POST /v1/chat/completions/tokenizer/encode/count

Counts tokens for a given chat completion request without performing inference.

**Request Body:**

- Content-Type: application/json
- JSON object in `ChatCompletionCreateRequest` format with:
  - `model` (string)  
    Model to use for tokenization.
  - `messages` (array)  
    Array of message objects with `role` and `content`.

**Response Body:**

- Content-Type: application/json
- JSON object with token count:
  - `tokenCount` (integer)  
    Number of tokens in the request.

**Example:**

Request body

```json
  {
    "messages": [
      {
        "role": "system",
        "content": "This is a system message"
      },
      {
        "role": "user",
        "content": "Hello, what is Microsoft?"
      }
    ],
    "model": "Phi-4-mini-instruct-cuda-gpu"
  }
```

Response body

```json
  {
    "tokenCount": 23
  }
```
