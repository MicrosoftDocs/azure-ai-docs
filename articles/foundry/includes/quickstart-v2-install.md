---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 02/23/2026
ms.custom: include
---

Make sure you install the correct preview/prerelease version of the packages as shown here.

# [Python](#tab/python)

1. Install these packages, including the preview version of `azure-ai-projects`. This version uses the **Foundry projects (new) API** (preview).

    ```
    pip install azure-ai-projects>=2.0.0
    ```

1. Sign in using the CLI `az login` command to authenticate before running your Python scripts.

# [C#](#tab/csharp)

1. Install packages:

    Add NuGet packages using the .NET CLI in the integrated terminal: These packages use the **Foundry projects (new) API** (preview).
        
    ```bash
    dotnet add package Azure.AI.Projects --prerelease
    dotnet add package Azure.AI.Projects.OpenAI --prerelease
    dotnet add package Azure.Identity
    ```

1. Sign in using the CLI `az login` command to authenticate before running your C# scripts.


# [TypeScript](#tab/typescript)

1. Install these packages, including the preview version of `@azure/ai-projects`. This version uses the **Foundry projects (new) API** (preview).:

    ```bash
    npm install @azure/ai-projects
    ```

1. Sign in using the CLI `az login` command to authenticate before running your TypeScript scripts.

# [Java](#tab/java)

1. Sign in using the CLI `az login` command to authenticate before running your Java scripts.

# [REST API](#tab/rest)

1. Sign in using the CLI `az login` command to authenticate before running the next command.
1. Get a temporary access token. It will expire in 60-90 minutes, you'll need to refresh after that.

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```
    
1. Save the results as the environment variable `AZURE_AI_AUTH_TOKEN`.  


# [Foundry portal](#tab/portal)

No installation is necessary to use the Foundry portal.

---

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]