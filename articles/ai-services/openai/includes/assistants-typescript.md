---
title: 'Quickstart: Use the Azure OpenAI Service via the JavaScript SDK'
titleSuffix: Azure OpenAI Service
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the JavaScript SDK. 
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-openai
ms.topic: include
ms.date: 10/09/2024
ms.custom: passwordless-js, devex-track-typescript
---

<a href="/javascript/api/@azure/openai-assistants" target="_blank">Reference documentation</a> | <a href="https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai" target="_blank">Library source code</a> | <a href="https://www.npmjs.com/package/@azure/openai-assistants" target="_blank">Package (npm)</a> |

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- <a href="https://nodejs.org/" target="_blank">Node.js LTS or ESM support.</a>
- [TypeScript](https://www.typescriptlang.org/download/) installed globally
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI. 
- An Azure OpenAI resource with a [compatible model in a supported region](../concepts/models.md#assistants-preview).
- We recommend reviewing the [Responsible AI transparency note](/legal/cognitive-services/openai/transparency-note?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext&tabs=text) and other [Responsible AI resources](/legal/cognitive-services/openai/overview?context=%2Fazure%2Fai-services%2Fopenai%2Fcontext%2Fcontext) to familiarize yourself with the capabilities and limitations of the Azure OpenAI Service.
- An Azure OpenAI resource with the `gpt-4 (1106-preview)` model deployed was used testing this example. 

## Passwordless authentication is recommended

For passwordless authentication, you need to 

1. Use the `@azure/identity` package.
1. Assign the `Cognitive Services User` role to your user account. This can be done in the Azure portal under **Access control (IAM)** > **Add role assignment**.
1. Sign in with the Azure CLI such as `az login`.

## Set up

1. Create a new folder `assistants-quickstart` to contain the application and open Visual Studio Code in that folder with the following command:

    ```shell
    mkdir assistants-quickstart && code assistants-quickstart
    ```
    

1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Update the `package.json` to ECMAScript with the following command: 

    ```shell
    npm pkg set type=module
    ```
    

1. Install the OpenAI Assistants client library for JavaScript with:

    ```console
    npm install openai
    ```

1. For the **recommended** passwordless authentication:

    ```console
    npm install @azure/identity
    ```

## Retrieve resource information


#### [Microsoft Entra ID](#tab/typescript-keyless)

[!INCLUDE [assistants-keyless-environment-variables](assistants-env-var-without-key.md)]


#### [API key](#tab/typescript-key)

[!INCLUDE [assistants-key-environment-variables](assistants-env-var-key.md)]

---

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 


## Create an assistant

In our code we're going to specify the following values:

| **Name** | **Description** |
|:---|:---|
| **Assistant name** | Your deployment name that is associated with a specific model. |
| **Instructions** | Instructions are similar to system messages this is where you give the model guidance about how it should behave and any context it should reference when generating a response. You can describe the assistant's personality, tell it what it should and shouldn't answer, and tell it how to format responses. You can also provide examples of the steps it should take when answering responses. |
| **Model** | This is the deployment name. |
| **Code interpreter** | Code interpreter provides access to a sandboxed Python environment that can be used to allow the model to test and execute code. |

### Tools

An individual assistant can access up to 128 tools including `code interpreter`, and any custom tools you create via [functions](../how-to/assistant-functions.md).

    
## Create a new TypeScript application

#### [Microsoft Entra ID](#tab/typescript-keyless)

1. Create the `index.ts` file with the following code:

    ```typescript
    import { AzureOpenAI } from "openai";
    import {
      Assistant,
      AssistantCreateParams,
      AssistantTool,
    } from "openai/resources/beta/assistants";
    import { Message, MessagesPage } from "openai/resources/beta/threads/messages";
    import { Run } from "openai/resources/beta/threads/runs/runs";
    import { Thread } from "openai/resources/beta/threads/threads";
    
    // Add `Cognitive Services User` to identity for Azure OpenAI resource
    import {
      DefaultAzureCredential,
      getBearerTokenProvider,
    } from "@azure/identity";
    
    // Get environment variables
    const azureOpenAIEndpoint = process.env.AZURE_OPENAI_ENDPOINT as string;
    const azureOpenAIDeployment = process.env
      .AZURE_OPENAI_DEPLOYMENT_NAME as string;
    const openAIVersion = process.env.OPENAI_API_VERSION as string;
    
    // Check env variables
    if (!azureOpenAIEndpoint || !azureOpenAIDeployment || !openAIVersion) {
      throw new Error(
        "Please ensure to set AZURE_OPENAI_DEPLOYMENT_NAME and AZURE_OPENAI_ENDPOINT in your environment variables."
      );
    }
    
    // Get Azure SDK client
    const getClient = (): AzureOpenAI => {
      const credential = new DefaultAzureCredential();
      const scope = "https://cognitiveservices.azure.com/.default";
      const azureADTokenProvider = getBearerTokenProvider(credential, scope);
      const assistantsClient = new AzureOpenAI({
        endpoint: azureOpenAIEndpoint,
        apiVersion: openAIVersion,
        azureADTokenProvider,
      });
      return assistantsClient;
    };
    
    const assistantsClient = getClient();
    
    const options: AssistantCreateParams = {
      model: azureOpenAIDeployment, // Deployment name seen in Azure AI Foundry portal
      name: "Math Tutor",
      instructions:
        "You are a personal math tutor. Write and run JavaScript code to answer math questions.",
      tools: [{ type: "code_interpreter" } as AssistantTool],
    };
    const role = "user";
    const message = "I need to solve the equation `3x + 11 = 14`. Can you help me?";
    
    // Create an assistant
    const assistantResponse: Assistant =
      await assistantsClient.beta.assistants.create(options);
    console.log(`Assistant created: ${JSON.stringify(assistantResponse)}`);
    
    // Create a thread
    const assistantThread: Thread = await assistantsClient.beta.threads.create({});
    console.log(`Thread created: ${JSON.stringify(assistantThread)}`);
    
    // Add a user question to the thread
    const threadResponse: Message =
      await assistantsClient.beta.threads.messages.create(assistantThread.id, {
        role,
        content: message,
      });
    console.log(`Message created:  ${JSON.stringify(threadResponse)}`);
    
    // Run the thread and poll it until it is in a terminal state
    const runResponse: Run = await assistantsClient.beta.threads.runs.createAndPoll(
      assistantThread.id,
      {
        assistant_id: assistantResponse.id,
      },
      { pollIntervalMs: 500 }
    );
    console.log(`Run created:  ${JSON.stringify(runResponse)}`);
    
    // Get the messages
    const runMessages: MessagesPage =
      await assistantsClient.beta.threads.messages.list(assistantThread.id);
    for await (const runMessageDatum of runMessages) {
      for (const item of runMessageDatum.content) {
        // types are: "image_file" or "text"
        if (item.type === "text") {
          console.log(`Message content: ${JSON.stringify(item.text?.value)}`);
        }
      }
    }
    ```
    


1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```
    
1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the code with the following command:

    ```shell
    node index.js
    ```



#### [API key](#tab/typescript-key)

1. Create the `index.ts` file with the following code:

    ```typescript
    import { AzureOpenAI } from "openai";
    import {
      Assistant,
      AssistantCreateParams,
      AssistantTool,
    } from "openai/resources/beta/assistants";
    import { Message, MessagesPage } from "openai/resources/beta/threads/messages";
    import { Run } from "openai/resources/beta/threads/runs/runs";
    import { Thread } from "openai/resources/beta/threads/threads";
    
    // Get environment variables
    const azureOpenAIKey = process.env.AZURE_OPENAI_KEY as string;
    const azureOpenAIEndpoint = process.env.AZURE_OPENAI_ENDPOINT as string;
    const azureOpenAIDeployment = process.env
      .AZURE_OPENAI_DEPLOYMENT_NAME as string;
    const openAIVersion = process.env.OPENAI_API_VERSION as string;
    
    // Check env variables
    if (!azureOpenAIKey || !azureOpenAIEndpoint || !azureOpenAIDeployment || !openAIVersion) {
      throw new Error(
        "Please set AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT_NAME in your environment variables."
      );
    }
    
    // Get Azure SDK client
    const getClient = (): AzureOpenAI => {
      const assistantsClient = new AzureOpenAI({
        endpoint: azureOpenAIEndpoint,
        apiVersion: openAIVersion,
        apiKey: azureOpenAIKey,
      });
      return assistantsClient;
    };
    
    const assistantsClient = getClient();
    
    const options: AssistantCreateParams = {
      model: azureOpenAIDeployment, // Deployment name seen in Azure AI Foundry portal
      name: "Math Tutor",
      instructions:
        "You are a personal math tutor. Write and run JavaScript code to answer math questions.",
      tools: [{ type: "code_interpreter" } as AssistantTool],
    };
    const role = "user";
    const message = "I need to solve the equation `3x + 11 = 14`. Can you help me?";
    
    // Create an assistant
    const assistantResponse: Assistant =
      await assistantsClient.beta.assistants.create(options);
    console.log(`Assistant created: ${JSON.stringify(assistantResponse)}`);
    
    // Create a thread
    const assistantThread: Thread = await assistantsClient.beta.threads.create({});
    console.log(`Thread created: ${JSON.stringify(assistantThread)}`);
    
    // Add a user question to the thread
    const threadResponse: Message =
      await assistantsClient.beta.threads.messages.create(assistantThread.id, {
        role,
        content: message,
      });
    console.log(`Message created:  ${JSON.stringify(threadResponse)}`);
    
    // Run the thread and poll it until it is in a terminal state
    const runResponse: Run = await assistantsClient.beta.threads.runs.createAndPoll(
      assistantThread.id,
      {
        assistant_id: assistantResponse.id,
      },
      { pollIntervalMs: 500 }
    );
    console.log(`Run created:  ${JSON.stringify(runResponse)}`);
    
    // Get the messages
    const runMessages: MessagesPage =
      await assistantsClient.beta.threads.messages.list(assistantThread.id);
    for await (const runMessageDatum of runMessages) {
      for (const item of runMessageDatum.content) {
        // types are: "image_file" or "text"
        if (item.type === "text") {
          console.log(`Message content: ${JSON.stringify(item.text?.value)}`);
        }
      }
    }
    ```
    

1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```

1. Run the code with the following command:

    ```shell
    node index.js
    ```

---

## Output

```console
Assistant created: {"id":"asst_zXaZ5usTjdD0JGcNViJM2M6N","createdAt":"2024-04-08T19:26:38.000Z","name":"Math Tutor","description":null,"model":"daisy","instructions":"You are a personal math tutor. Write and run JavaScript code to answer math questions.","tools":[{"type":"code_interpreter"}],"fileIds":[],"metadata":{}}
Thread created: {"id":"thread_KJuyrB7hynun4rvxWdfKLIqy","createdAt":"2024-04-08T19:26:38.000Z","metadata":{}}
Message created:  {"id":"msg_o0VkXnQj3juOXXRCnlZ686ff","createdAt":"2024-04-08T19:26:38.000Z","threadId":"thread_KJuyrB7hynun4rvxWdfKLIqy","role":"user","content":[{"type":"text","text":{"value":"I need to solve the equation `3x + 11 = 14`. Can you help me?","annotations":[]},"imageFile":{}}],"assistantId":null,"runId":null,"fileIds":[],"metadata":{}}
Created run
Run created:  {"id":"run_P8CvlouB8V9ZWxYiiVdL0FND","object":"thread.run","status":"queued","model":"daisy","instructions":"You are a personal math tutor. Write and run JavaScript code to answer math questions.","tools":[{"type":"code_interpreter"}],"metadata":{},"usage":null,"assistantId":"asst_zXaZ5usTjdD0JGcNViJM2M6N","threadId":"thread_KJuyrB7hynun4rvxWdfKLIqy","fileIds":[],"createdAt":"2024-04-08T19:26:39.000Z","expiresAt":"2024-04-08T19:36:39.000Z","startedAt":null,"completedAt":null,"cancelledAt":null,"failedAt":null}
Message content: "The solution to the equation \\(3x + 11 = 14\\) is \\(x = 1\\)."
Message content: "Yes, of course! To solve the equation \\( 3x + 11 = 14 \\), we can follow these steps:\n\n1. Subtract 11 from both sides of the equation to isolate the term with x.\n2. Then, divide by 3 to find the value of x.\n\nLet me calculate that for you."
Message content: "I need to solve the equation `3x + 11 = 14`. Can you help me?"
```

It's important to remember that while the code interpreter gives the model the capability to respond to more complex queries by converting the questions into code and running that code iteratively in JavaScript until it reaches a solution, you still need to validate the response to confirm that the model correctly translated your question into a valid representation in code.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Sample code

* [Quickstart sample code](https://github.com/Azure-Samples/azure-typescript-e2e-apps/tree/main/quickstarts/azure-openai-assistants)

## See also

* Learn more about how to use Assistants with our [How-to guide on Assistants](../how-to/assistant.md).
* [Azure OpenAI Assistants API samples](https://github.com/Azure-Samples/azureai-samples/tree/main/scenarios/Assistants)

