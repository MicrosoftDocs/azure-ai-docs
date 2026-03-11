---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: include
ms.date: 01/22/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## JavaScript SDK Reference

### Project setup

The high-level architecture of the Foundry Local SDK is as follows:

:::image type="content" source="../../media/architecture/new-sdk-architecture.png" alt-text="Diagram of the new architecture for Foundry Local." lightbox="../../media/architecture/new-sdk-architecture.png":::

The SDK is a light-weight wrapper around a Foundry Local Core C API (`.dll`/`.so`/`.dylib`) that provides a more user-friendly interface for JavaScript developers. The SDK handles loading the native library, managing memory, and converting data types between JavaScript and C. The Foundry Local Core C API has two flavors but the *same* API surface:

- **WindowsML (WinML)** - Windows specific that uses WindowsML to acquire the necessary drivers and execution providers for the available hardware. This is the recommended option for Windows users as it provides better performance and compatibility with a wide range of hardware.
- **Cross-platform** - can be used on Windows, macOS, and Linux. It should be noted that on macOS devices with Apple Silicon the Cross-platform SDK will use Apple's Metal framework for hardware acceleration via the ONNX runtime WebGPU execution provider.

When you install the Foundry Local SDK package into your project, you can choose to install the WinML or cross-platform version.

[!INCLUDE [project-setup](./../javascript-project-setup.md)]

### Quickstart

Use this snippet to verify that the SDK can initialize and access the local model catalog.

```js
import { FoundryLocalManager } from 'foundry-local-sdk';

console.log('Initializing Foundry Local SDK...');

const manager = FoundryLocalManager.create({
    appName: 'foundry_local_samples',
    logLevel: 'info'
});
console.log('✓ SDK initialized successfully');

// Explore available models
console.log('\nFetching available models...');
const catalog = manager.catalog;
const models = await catalog.getModels();

console.log(`Found ${models.length} models:`);
for (const model of models) {
    console.log(`  - ${model.alias}`);
}
```

This example outputs the list of available models for your hardware.

### Samples

- For sample applications that demonstrate how to use the Foundry Local JavaScript SDK, see the [Foundry Local JavaScript SDK Samples GitHub repository](https://aka.ms/fl-js-samples).

### API reference

- For more details on the Foundry Local JavaScript SDK read [Foundry Local JavaScript SDK API Reference](https://aka.ms/fl-js-api-ref).

### References

- [Integrate with inference SDKs](../../how-to/how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local native chat completions API](../../how-to/how-to-use-native-chat-completions.md)
