---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 11/06/2025
ms.custom: include
---


# [Python](#tab/python)

Install these packages, including the preview version of `azure-ai-projects`. This version uses the **Foundry projects (new) API** (preview).

```
pip install azure-ai-projects --pre
pip install openai azure-identity python-dotenv
```

# [C#](#tab/csharp)

Add NuGet packages using the .NET CLI in the integrated terminal: These packages use the **Foundry projects (new) API** (preview).
    
```bash
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.AI.Projects.OpenAI --prerelease
dotnet add package Azure.Identity
```


# [TypeScript](#tab/typescript)

Install these packages, including the preview version of `@azure/ai-projects`. This version uses the **Foundry projects (new) API** (preview).:

```bash
npm install @azure/ai-projects@beta @azure/identity dotenv
```

# [Java](#tab/java)

No installation needed.

# [REST API](#tab/rest)

1. Get a temporary access token. It will expire in 60-90 minutes, you'll need to refresh after that.

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```
    
1. Save the results as the environment variable `AZURE_AI_AUTH_TOKEN`.  

# [Foundry portal](#tab/portal)

No installation is necessary to use the Foundry portal.

---

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]