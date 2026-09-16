---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/09/2026
ms.custom: include
ai-usage: ai-assisted
---

## Get the code and set your values

# [Python](#tab/python)

The Python samples don't read environment variables. In each file, replace these placeholder values:

* `your_project_endpoint`: [Your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details), in the format `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`.
* `your_agent_name`: A name for your agent, such as `MyAgent`.

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the model name in the sample code.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/quickstart)

# [C#](#tab/csharp)

The C# samples don't read environment variables. In each file, replace these placeholder values:

* `your_project_endpoint`: [Your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details), in the format `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`.
* `your_agent_name`: A name for your agent, such as `MyAgent`.

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the model name in the sample code.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/quickstart)

# [TypeScript](#tab/typescript)

The TypeScript samples don't read environment variables. In each file, replace these values with [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) and an agent name such as `MyAgent`:

```typescript
const FOUNDRY_PROJECT_ENDPOINT = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
const FOUNDRY_AGENT_NAME = "MyAgent";
```

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the model name in the sample code.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/typescript/quickstart/)

# [Java](#tab/java)

The Java samples don't read environment variables. In each file, replace these values with [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) and an agent name such as `MyAgent`:

```java
String foundryProjectEndpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
String foundryAgentName = "MyAgent";
```

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the model name in the sample code.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/java/quickstart/)

# [REST API](#tab/rest)

1. In each request URL, replace `YOUR-FOUNDRY-RESOURCE-NAME` and `YOUR-PROJECT-NAME` with the values from [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details), which has the form `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>`.

1. The chat-with-agent request reads the agent name from an environment variable:

    ```
    FOUNDRY_AGENT_NAME=MyAgent
    ```

The samples use the `gpt-5-mini` deployment you created in [Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md). If you deployed a model under a different name, update the `model` value in the request body.

Follow along below or get the code:
> [!div class="nextstepaction"]
> [Get the code](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/REST/quickstart).

# [Foundry portal](#tab/portal)

No code is necessary when using the Foundry portal.

---
