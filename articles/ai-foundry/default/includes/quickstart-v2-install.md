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

[!INCLUDE [agent-v2-switch](agent-v2-switch.md)]

# [Python](#tab/python)

1. Install these packages, including the preview version of `azure-ai-projects`. This version uses the **Foundry projects (new) API** (preview).

    ```
    pip install azure-ai-projects --pre
    pip install openai azure-identity python-dotenv
    ```

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Python scripts.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/python/quickstart)

# [C#](#tab/csharp)

1. Install packages:

    Add NuGet packages using the .NET CLI in the integrated terminal: These packages use the **Foundry projects (new) API** (preview).
        
    ```bash
    dotnet add package Azure.AI.Agents --prerelease
    dotnet add package Azure.AI.Projects --prerelease
    dotnet add package Azure.Identity
    dotnet add package OpenAI --version 2.6.*
    ```

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your C# scripts.

> Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/csharp/quickstart)


# [TypeScript](#tab/typescript)

1. Install these packages, including the preview version of `@azure/ai-projects`. This version uses the **Foundry projects (new) API** (preview).:

    ```bash
    npm install @azure/ai-projects@beta @azure/identity dotenv
    ```

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your TypeScript scripts.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/typescript/quickstart/src)

# [Java](#tab/java)

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running your Java scripts.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/java/quickstart/src/main/java/com/microsoft/foundry/samples/)

# [REST API](#tab/rest)

1. Make sure to sign in using the CLI `az login` (or `az login --use-device-code`) command to authenticate before running the next command.
1. Get a temporary access token. It will expire in 60-90 minutes, you'll need to refresh after that.

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```
    
1. Save the results as the environment variable `AZURE_AI_AUTH_TOKEN`.  

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/microsoft/REST/mslearn-resources/quickstart).


# [Microsoft Foundry portal](#tab/portal)

No installation is necessary to use the Foundry portal.

---
