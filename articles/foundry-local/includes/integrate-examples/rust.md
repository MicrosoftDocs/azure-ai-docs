---
title: Include file
description: Include file
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/06/2026
ms.author: samkemp
author: samuel100
ai-usage: ai-assisted
---

## Prerequisites

- [Rust and Cargo](https://www.rust-lang.org/tools/install) installed.


## Samples repository

The complete sample code for this article is available in the [Foundry Local GitHub repository](https://github.com/microsoft/Foundry-Local). To clone the repository and navigate to the sample use:

```bash
git clone https://github.com/microsoft/Foundry-Local.git
cd Foundry-Local/samples/rust/foundry-local-webserver
```

## Install packages

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Update the `main.rs` file

Copy-and-paste the following code into the Rust file named `main.rs`:

:::code language="rust" source="~/foundry-local-main/samples/rust/foundry-local-webserver/src/main.rs" id="complete_code":::

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

```bash
cargo run
```

You should see a streaming response printed in your terminal. On the first run, Foundry Local might download execution providers and the model, which can take a few minutes.

