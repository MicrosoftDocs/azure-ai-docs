---
title: Use the Foundry Local CLI (preview)
titleSuffix: Foundry Local
description: Learn how to use the Foundry Local command-line interface to browse models, run interactive chat sessions, and manage your local model cache.
ms.service: microsoft-foundry
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: lajanuar
reviewer: wayne-ch
ms.reviewer: waynechuang
author: laujan
ms.date: 08/06/2026
ai-usage: ai-assisted
---

# Use the Foundry Local CLI (preview)
[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

The Foundry Local command-line interface (CLI) lets you browse the model catalog, run models interactively, and manage your local cache directly from the terminal. The CLI is useful for exploring available models, testing prompts, and preparing your environment before writing application code.

> [!NOTE]
> The CLI is a companion tool for exploration and management. For building applications, use the [Foundry Local SDK](../reference/reference-sdk-current.md), which embeds the runtime directly in your app.

## Prerequisites

- A terminal (PowerShell, Terminal, or similar).
- Internet access for first-time model and execution provider downloads.

## Install the Foundry Local CLI

Install Foundry Local by using the package manager or installer for your operating system.

### [Windows](#tab/windows)

```bash
winget install Microsoft.FoundryLocal
```

### [macOS Apple Silicon](#tab/macos)

Install Foundry Local by using Homebrew:

```bash
brew tap microsoft/foundrylocal
brew install foundrylocal
```

If you're upgrading from Foundry Local 0.8.x, stop the old service before upgrading:

```bash
foundry service stop
brew update
brew upgrade microsoft/foundrylocal/foundrylocal
```

For later upgrades, run `brew update` and `brew upgrade microsoft/foundrylocal/foundrylocal`.

Alternatively, download the current macOS `.pkg` or `.zip` from the [Foundry Local CLI release assets](https://aka.ms/foundry-local-installer). If you download the `.pkg`, open it with macOS Installer.

---

Verify the installation:

```bash
foundry --version
```

> [!TIP]
> If you see a server connection error after installation (for example, `Request to local service failed`), run `foundry server restart`.

## Browse the model catalog

List all models available for local inference:

```bash
foundry model list
```

On first run, Foundry Local downloads execution providers for your hardware before displaying the catalog.

Filter the list by hardware device or model type:

```bash
foundry model list --device gpu
foundry model list --type chat
```

Get detailed information about a specific model:

```bash
foundry model info phi-4-mini
```

> [!TIP]
> Use a model alias (like `phi-4-mini`) to let Foundry Local automatically select the best variant for your hardware. Use a full model ID to target a specific variant.

## Run a model interactively

Start an interactive chat session with a model:

```bash
foundry chat phi-4-mini
```

Foundry Local downloads the model on first run, loads it into memory, and opens a chat prompt. Type a message and press Enter to get a response:

```text
> What is the golden ratio?
```

Type `/exit` to end the session.

## Download a model without running it

Pre-download a model to the local cache for later use:

```bash
foundry model download phi-4-mini
```

This step is useful for preparing models in advance, especially when you expect to be offline later.

## Manage the model cache

View models stored locally:

```bash
foundry cache list
```

Check the current cache location:

```bash
foundry cache location
```

Remove a model you no longer need:

```bash
foundry cache remove phi-4-mini
```

Change the cache directory (for example, to move models to a larger disk):

```bash
foundry cache cd /path/to/new/cache
```

## Check server status

Verify the Foundry Local daemon is running and get the local endpoint URL:

```bash
foundry server status
```

If the local server isn't responding, restart the daemon:

```bash
foundry server restart
```

## Related content

- [Foundry Local CLI reference](../reference/reference-cli.md)
- [Get started with Foundry Local](../get-started.md)
- [Foundry Local architecture overview](../concepts/foundry-local-architecture.md)
