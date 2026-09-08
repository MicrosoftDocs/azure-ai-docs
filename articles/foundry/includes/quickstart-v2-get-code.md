---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/03/2026
ms.custom: include
ai-usage: ai-assisted
---

## Set environment variables and get the code

# [Python](#tab/python)

1. Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) and model name as environment variables. The `quickstart-responses.py` sample reads these values:

    ```
    AZURE_AI_PROJECT_ENDPOINT=https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
    MODEL_DEPLOYMENT=gpt-5-mini
    ```

1. The `quickstart-create-agent.py` and `quickstart-chat-with-agent.py` samples don't read environment variables. In each file, replace the `PROJECT_ENDPOINT` and `AGENT_NAME` values with your endpoint and an agent name such as `MyAgent`.

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the model name in the sample code.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/quickstart)

# [C#](#tab/csharp)

1. Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) and model name as environment variables. The `quickstart-responses.cs` sample reads these values:

    ```
    AZURE_AI_PROJECT_ENDPOINT=https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
    MODEL_DEPLOYMENT=gpt-5-mini
    ```

1. The `quickstart-create-agent.cs` and `quickstart-chat-with-agent.cs` samples don't read environment variables. In each file, replace the `ProjectEndpoint` and `AgentName` values with your endpoint and an agent name such as `MyAgent`.

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the model name in the sample code.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/quickstart)

# [TypeScript](#tab/typescript)

The TypeScript samples don't read environment variables. In each file, replace these values with [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) and an agent name such as `MyAgent`:

```typescript
const PROJECT_ENDPOINT = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
const AGENT_NAME = "MyAgent";
```

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the model name in the sample code.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/typescript/quickstart/)

# [Java](#tab/java)

The Java samples don't read environment variables. In each file, replace these values with [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) and an agent name such as `MyAgent`:

```java
String ProjectEndpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
String AgentName = "MyAgent";
```

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the model name in the sample code.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/java/quickstart/)

# [REST API](#tab/rest)

1. In each request URL, replace `YOUR-FOUNDRY-RESOURCE-NAME` and `YOUR-PROJECT-NAME` with the values from [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details), which has the form `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`.

1. The chat-with-agent request reads the agent name from an environment variable:

    ```
    AGENT_NAME=MyAgent
    ```

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the `model` value in the request body.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/REST/quickstart).

# [Foundry portal](#tab/portal)

No code is necessary when using the Foundry portal.

---
