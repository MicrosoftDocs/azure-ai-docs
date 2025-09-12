---
title: "Quickstart: Get started with Azure AI Foundry (Hub projects)"
titleSuffix: Azure AI Foundry
description: Set up SDK, deploy a model, and build a simple chat app for hub-based projects.
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 09/12/2025 
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-2025
ai-usage: ai-assisted
---

# Quickstart: Get started with Azure AI Foundry (Hub projects)

> [!NOTE]
> An alternate Foundry (fdp) project quickstart is available: [Quickstart: Get started with Azure AI Foundry (Foundry projects)](get-started-code.md).
> [!NOTE]
> An alternate Foundry (fdp) project quickstart is available: [Quickstart: Get started with Azure AI Foundry (Foundry projects)](get-started-code.md).

This quickstart sets up your local environment for hub-based projects, deploys a model, and builds a simple traced/evaluable chat script.

## Prerequisites

- Azure subscription.
- Existing hub project (or create one via hub-create-projects.md). If not, consider using a Foundry project quickstart.

## Set up your development environment

1. Install prerequisites (Python, Azure CLI, login).
2. Install packages:
```bash
pip install azure-ai-inference azure-identity azure-ai-projects==1.0.0b10
```
> Different project types need distinct azure-ai-projects versions; isolate environments.

## Deploy a model

1. Portal: Sign in, open hub project.
2. Model catalog: select gpt-4o-mini.
3. Use this model > accept default deployment name > Deploy.
4. After success: Open in playground to verify.

## Build your chat app

Create chat.py with sample code:
```python
# minimal outline referencing deployed model
# (Full sample in azureai-samples repository path scenarios/projects/basic/chat-simple.py)
```

Insert your project connection string from the project Overview page (copy, replace placeholder in code).

Run:
```bash
python chat.py
```

## Add prompt templating

Add get_chat_response using mustache template (see chat-template.py sample) then invoke with user/context messages.

Run again to view templated response.

## Clean up resources

Delete deployment or project when done to avoid charges.

## Next step

> [!div class="nextstepaction"]
> Add data and use RAG (tutorial link)
