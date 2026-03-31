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

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd rust/native-chat-completions
```

## Install packages

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Use native chat completions API    

The following example demonstrates how to use the native chat completions API in Foundry Local. The code includes the following steps:

1. Creates a `FoundryLocalManager` instance with a `FoundryLocalConfig`.
1. Gets a `Model` object from the model catalog using an alias.
   
   > [!NOTE]
   > Foundry Local automatically selects the best variant for the model based on the available hardware of the host machine.

1. Downloads and loads the model variant.
1. Uses the native chat completions API to generate a streaming response.
1. Unloads the model.

Replace the contents of `src/main.rs` with the following code:

:::code language="rust" source="~/foundry-local-main/samples/rust/native-chat-completions/src/main.rs" id="complete_code":::

Run the code by using the following command:

```bash
cargo run
```

## Troubleshooting

- **Build errors**: Ensure you have Rust 1.70.0 or later installed. Run `rustup update` to get the latest version.
- **`Model not found`**: Verify the model alias is correct. Use `manager.catalog().get_models().await?` to list available models.
- **Slow first run**: Model downloads can take time the first time you run the app.
