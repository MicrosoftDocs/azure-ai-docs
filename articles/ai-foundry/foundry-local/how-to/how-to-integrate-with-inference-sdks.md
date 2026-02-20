---
title: Integrate with inference SDKs
titleSuffix: Foundry Local
description: This article provides instructions on how to integrate Foundry Local with common Inferencing SDKs.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 10/06/2023
zone_pivot_groups: foundry-local-sdk
author: jonburchel
reviewer: samuel100
ai-usage: ai-assisted
---

# Integrate inference SDKs with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local integrates with OpenAI-compatible SDKs and HTTP clients through a local REST server. This article shows you how to connect your app to local AI models by using popular SDKs.

::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/integrate-examples/python.md)]
::: zone-end
::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/integrate-examples/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/integrate-examples/javascript.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/integrate-examples/rust.md)]
::: zone-end

## Foundry Local CLI Updates

### Chat Completion Command

The `chat-completion` command enables streaming chat completions using OpenAI's Chat API. This command supports specifying a model, prompt message, optional image file path, and maximum tokens for the response.

#### Arguments
- `model`: The name of the model to use for chat completion.
- `promptMessage`: The input prompt message for the chat.

#### Options
- `--imageFilePath`: (Optional) Path to an image file to include in the chat context.
- `--maxTokens`: (Optional) Maximum number of tokens to generate in the response.

#### Example Usage
```bash
foundry-local chat-completion --model gpt-4 --promptMessage "What is the weather today?" --maxTokens 100
```
```bash
foundry-local chat-completion --model gpt-4 --promptMessage "Describe this image." --imageFilePath ./images/sample.jpg
```

### Download Model Command

The `download-model` command allows downloading models using various providers. It supports specifying a URI, output directory, and additional options for revision, path, token, buffer size, and provider.

#### Arguments
- `uri`: The URI of the model to download.
- `outputDirectory`: The directory where the downloaded model will be stored.

#### Options
- `--revision`: (Optional) Specify the revision of the model to download.
- `--path`: (Optional) Path within the model repository.
- `--token`: (Optional) Authentication token for accessing the model.
- `--bufferSize`: (Optional) Buffer size for downloading the model.
- `--provider`: (Optional) Specify the provider for the model download (e.g., Hugging Face).

#### Example Usage
```bash
foundry-local download-model --uri https://models.example.com/model.zip --outputDirectory ./models
```
```bash
foundry-local download-model --uri https://models.example.com/model.zip --outputDirectory ./models --provider huggingface --revision v1.0
```

### Download Model Catalog Command

The `download-model-catalog` command supports downloading models from a catalog using the model name and output directory. Additional options include buffer size and provider.

#### Arguments
- `modelName`: The name of the model to download from the catalog.
- `outputDirectory`: The directory where the downloaded model will be stored.

#### Options
- `--bufferSize`: (Optional) Buffer size for downloading the model.
- `--provider`: (Optional) Specify the provider for the model download (e.g., Hugging Face).

#### Example Usage
```bash
foundry-local download-model-catalog --modelName bert-base-uncased --outputDirectory ./models
```
```bash
foundry-local download-model-catalog --modelName bert-base-uncased --outputDirectory ./models --provider huggingface --bufferSize 4096
```

## Related content

- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)