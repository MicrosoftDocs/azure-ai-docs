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

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd rust/foundry-local-webserver
```

## Install packages

[!INCLUDE [project-setup](../rust-project-setup.md)]

## Update the `main.rs` file

The following example demonstrates how to run inference by sending a request to the Foundry Local web service. The code includes the following steps:

1. Initializes a `FoundryLocalManager` instance with a configuration.
1. Gets a model from the catalog using an alias.
1. Downloads and loads the model variant.
1. Starts the web service to expose an OpenAI-compatible REST endpoint.
1. Uses `reqwest` to send a streaming chat completion request.
1. Parses Server-Sent Events (SSE) chunks and prints the response.
1. Cleans up by stopping the web service and unloading the model.

Copy-and-paste the following code into the Rust file named `main.rs`:

:::code language="rust" source="~/foundry-local-main/samples/rust/foundry-local-webserver/src/main.rs" id="complete_code":::

Reference: [Foundry Local SDK reference](../../reference/reference-sdk-current.md)
Reference: [Foundry Local REST API reference](../../reference/reference-rest.md)

Run the code using the following command:

```bash
cargo run
```

You should see a streaming response printed in your terminal. On the first run, Foundry Local might download execution providers and the model, which can take a few minutes.

