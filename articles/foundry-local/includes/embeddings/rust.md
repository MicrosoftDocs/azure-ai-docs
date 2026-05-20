---
title: Include file
description: Include file
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/24/2026
ms.author: natke
author: natke
ai-usage: ai-assisted
---

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed (Rust 1.70.0 or later).


## Samples repository

The complete sample code for this article is available in the [Foundry Local GitHub repository](https://github.com/microsoft/Foundry-Local). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft/Foundry-Local.git
cd Foundry-Local/samples/rust/embeddings
```

## Install packages

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Generate text embeddings

Replace the contents of `main.rs` with the following code:

:::code language="rust" source="~/foundry-local-main/samples/rust/embeddings/src/main.rs" id="complete_code":::

Run the code by using the following command:

```bash
cargo run
```

## Troubleshooting

- **Build errors**: Ensure you have Rust 1.70.0 or later installed. Run `rustup update` to get the latest version.
- **`Model not found`**: Verify the model alias is correct. Use `manager.catalog().get_models().await?` to list available models.
- **Slow first run**: Model downloads can take time the first time you run the app.
