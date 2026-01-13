---
title: "Quickstart: Get started with Microsoft Foundry (Hub projects)"
titleSuffix: Microsoft Foundry
description: Set up SDK, deploy a model, and build a simple chat app for hub-based projects.
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 09/22/2025 
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-2025
  - hub-only
ai-usage: ai-assisted
---

# Quickstart: Get started with Microsoft Foundry (Hub projects)

> [!TIP]
> An alternate Foundry project quickstart is available: [Quickstart: Get started with Microsoft Foundry (Foundry projects)](get-started-code.md).

This quickstart sets up your local environment for hub-based projects, deploys a model, and builds a simple traced/evaluable chat script.

## Prerequisites

- Azure subscription.
- Existing hub project (or [create one](../how-to/hub-create-projects.md)). If not, consider using a Foundry project quickstart.

## Set up your development environment

1. Install prerequisites (Python, Azure CLI, login).
2. Install packages:
```bash
pip install azure-ai-inference azure-identity azure-ai-projects==1.0.0b10
```
> Different project types need distinct azure-ai-projects versions. Keep each project in its own isolated environment to avoid conflicts.

## Deploy a model

1. Portal: Sign in, open hub project.
2. Model catalog: select gpt-4o-mini.
3. Use this model > accept default deployment name > Deploy.
4. After success: Open in playground to verify.

## Build your chat app

Create chat.py with sample code:

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_connection_string = "<your-connection-string-goes-here>"

project = AIProjectClient.from_connection_string(
    conn_str=project_connection_string, credential=DefaultAzureCredential()
)

chat = project.inference.get_chat_completions_client()
response = chat.complete(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant that speaks like a techno punk rocker from 2350. Be cool but not too cool. Ya dig?",
        },
        {"role": "user", "content": "Hey, can you help me with my taxes? I'm a freelancer."},
    ],
)

print(response.choices[0].message.content)
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
> [Microsoft Foundry client library overview](../how-to/develop/sdk-overview.md)

## Related content

[Quickstart: Get started with Foundry (Foundry projects)](get-started-code.md).
