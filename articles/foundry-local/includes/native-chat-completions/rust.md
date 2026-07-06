---
title: Include file
description: Include file
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/15/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).


## Samples repository

The complete sample code for this article is available in the [foundry-samples GitHub repository](https://github.com/microsoft-foundry/foundry-samples). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/rust/foundry-local/native-chat-completions
```

## Install packages

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Use native chat completions API    

Replace the contents of `main.rs` with the following code:

:::code language="rust" source="~/foundry-local-main/samples/rust/foundry-local/native-chat-completions/src/main.rs" id="complete_code":::

Run the code by using the following command:

```bash
cargo run
```

## Troubleshooting

- **Build errors**: Ensure you have Rust 1.70.0 or later installed. Run `rustup update` to get the latest version.
- **`Model not found`**: Verify the model alias is correct. Use `manager.catalog().get_models().await?` to list available models.
- **Slow first run**: Model downloads can take time the first time you run the app.
