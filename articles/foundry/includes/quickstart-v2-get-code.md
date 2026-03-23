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

## Set environment variables and get the code

# [Python](#tab/python)

Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) as an environment variable. Also set these values for use in your scripts.

```
PROJECT_ENDPOINT=<endpoint copied from welcome screen>
AGENT_NAME="MyAgent"
```

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/python/quickstart)


Sign in using the CLI `az login` command to authenticate before running your Python scripts.

# [C#](#tab/csharp)

Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) as an environment variable. Also set these values for use in your scripts.

```
ProjectEndpoint = <endpoint copied from welcome screen>
AgentName = "MyAgent"
```

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/csharp/quickstart)

Sign in using the CLI `az login` command to authenticate before running your C# scripts.

# [TypeScript](#tab/typescript)

Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) as an environment variable. Also set these values for use in your scripts.

```
PROJECT_ENDPOINT=<endpoint copied from welcome screen>
AGENT_NAME="MyAgent"
```
Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/typescript/quickstart/src)

Sign in using the CLI `az login` command to authenticate before running your TypeScript scripts.

Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) as an environment variable. Also set these values for use in your scripts.

```
PROJECT_ENDPOINT=<endpoint copied from welcome screen>
AGENT_NAME="MyAgent"
```

# [Java](#tab/java)

Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) as an environment variable. Also set these values for use in your scripts.

```
ProjectEndpoint = <endpoint copied from welcome screen>
AgentName = "MyAgent"
```

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/java/quickstart/src/main/java/com/microsoft/foundry/samples/)

Sign in using the CLI `az login` command to authenticate before running your Java scripts.

# [REST API](#tab/rest)

Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) as an environment variable. 

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/REST/quickstart).

1. Sign in using the CLI `az login` command to authenticate before running the next command.
1. Get a temporary access token. It will expire in 60-90 minutes, you'll need to refresh after that.

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default
    ```
    
1. Save the results as the environment variable `AZURE_AI_AUTH_TOKEN`.  

# [Foundry portal](#tab/portal)

No code is necessary when using the Foundry portal.

---
