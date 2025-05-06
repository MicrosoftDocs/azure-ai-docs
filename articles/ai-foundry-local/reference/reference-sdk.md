<!-- filepath: reference/reference-sdk.md -->
---
title: Foundry Local Control Plane SDK Reference
titleSuffix: AI Foundry Local
description: Reference for Foundry Local Control Plane SDK.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: conceptual
ms.date: 05/06/2025
ms.author: maanavdalal
author: maanavd
---

# Foundry Local Control Plane SDK Reference

The Foundry Local Control Plane SDK simplifies management of AI models in local environments by providing control-plane operations that are decoupled from data-plane inferencing code. This reference covers the SDK for Python, JavaScript, and C#.

## CLI Primitives Refresher

The SDK leverages the following Foundry Local CLI primitives:

- `foundry model ls`: List available models to download
- `foundry model run`: Run a model
- `foundry model load`: Load a model into the model server
- `foundry model unload`: Unload a model from the model server
- `foundry model info`: Show the model information
- `foundry model download`: Download a model to local disk
- `foundry cache ls`: List models available on local disk
- `foundry cache location`: Show the directory path of the model cache
- `foundry cache remove`: Delete a model from the cache
- `foundry cache cd`: Change directory of the cache
- `foundry service ps`: Show the loaded models in service
- `foundry server start`: Start the service
- `foundry server stop`: Stop the service
- `foundry server restart`: Restart the service
- `foundry service status`: Check the status of the service

::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/sdk-examples/python.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/sdk-examples/javascript.md)]
::: zone-end
::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/sdk-examples/csharp.md)]
::: zone-end
