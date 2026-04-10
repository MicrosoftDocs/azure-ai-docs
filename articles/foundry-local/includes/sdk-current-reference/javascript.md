---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.custom: build-2025, dev-focus
ms.topic: include
ms.date: 01/22/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## JavaScript SDK Reference

### Install packages

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
