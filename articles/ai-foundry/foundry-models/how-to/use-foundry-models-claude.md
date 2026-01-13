---
title: Deploy and use Claude models in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how to deploy and use Anthropic's Claude models including  Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, and Claude Opus 4.1 in Microsoft Foundry
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 01/07/2026
ms.custom: ignite-2024
author: msakande
ms.author: mopeakande
ms.reviewer: keijik
reviewer: gojira
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy and use Claude models in Microsoft Foundry so I can integrate advanced conversational AI capabilities into my applications. 
---

# Deploy and use Claude models in Microsoft Foundry (preview)

[!INCLUDE [version-banner](../../includes/version-banner.md)]

This article explains how to deploy and use the latest Claude models in Foundry, including Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, and Claude Opus 4.1. Anthropic's flagship product is Claude, a frontier AI model useful for complex tasks such as coding, agents, financial analysis, research, and office tasks. Claude delivers exceptional performance while maintaining high safety standards.

[!INCLUDE [claude-usage-restriction](../includes/claude-usage-restriction.md)]

## Available Claude models

Foundry supports  Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, and Claude Opus 4.1 models through global standard deployment. These models have key capabilities that include:

- **Extended thinking**: Extended thinking gives Claude enhanced reasoning capabilities for complex tasks.
- **Image and text input**: Strong vision capabilities that enable the models to process images and return text outputs for analyzing and understanding charts, graphs, technical diagrams, reports, and other visual assets.
- **Code generation**: Advanced thinking that includes code generation, analysis, and debugging for Claude Sonnet 4.5 and Claude Opus 4.1.

For more details about the model capabilities, see [capabilities of Claude models](../concepts/models-from-partners.md#anthropic).

#### Claude Opus 4.5 (preview)

Claude Opus 4.5 is Anthropic's most intelligent model, and an industry leader across coding, agents, computer use, and enterprise workflows. With a 200K token context window and 64K max output, Opus 4.5 is ideal for production code, sophisticated agents, office tasks, financial analysis, cybersecurity, and computer use.

#### Claude Sonnet 4.5 (preview)

Claude Sonnet 4.5 is a highly capable model designed for building real-world agents and handling complex, long-horizon tasks. It offers a strong balance of speed and cost for high-volume use cases. Sonnet 4.5 also provides advanced accuracy for computer use, enabling developers to direct Claude to use computers the way people do.

#### Claude Haiku 4.5 (preview)

Claude Haiku 4.5 delivers near-frontier performance for a wide range of use cases. It stands out as one of the best coding and agent models, with the right speed and cost to power free products and scaled sub-agents.

#### Claude Opus 4.1 (preview)

Claude Opus 4.1 is an industry leader for coding. It delivers sustained performance on long-running tasks that require focused effort and thousands of steps, significantly expanding what AI agents can solve.

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../how-to/create-projects.md) created in one of the supported regions: **East US2** and **Sweden Central**.
- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace** to create subscriptions. Ensure you have the [permissions required to subscribe to model offerings](configure-marketplace.md).

## Deploy Claude models

Claude models in Foundry are available for [global standard deployment](../concepts/deployment-types.md#global-standard). To deploy a Claude model, follow the instructions in [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md).

After deployment, you can use the [Foundry playground](../../concepts/concept-playgrounds.md) to interactively test the model.

## Work with Claude models

Once deployed, you have some options for interacting with Claude models to generate text responses:

- Use the [Anthropic SDKs](https://docs.claude.com/en/api/client-sdks) and the following Claude APIs:

    - [Messages API](https://docs.claude.com/en/api/messages) to send a structured list of input messages with text and/or image content, and the model generates the next message in the conversation.
    - [Token Count API](https://docs.claude.com/en/api/messages-count-tokens) to count the number of tokens in a message.
    - [Files API](https://docs.claude.com/en/api/files-create) to upload and manage files to use with the Claude API without having to re-upload content with each request.
    - [Skills API](https://docs.claude.com/en/api/skills/create-skill) to create custom skills for Claude AI.

### Use the Messages API to work with Claude models

The following examples show how to **use the Messages API** to send requests to Claude Sonnet 4.5, by using both Microsoft Entra ID authentication and API key authentication methods. To work with your deployed model, you need these items:

- Your base URL, which is of the form `https://<resource name>.services.ai.azure.com/anthropic`.
- Your target URI from your deployment details, which is of the form `https://<resource name>.services.ai.azure.com/anthropic/v1/messages`.
- Microsoft Entra ID for keyless authentication or your deployment's API key for API authentication.
- Deployment name you chose during deployment creation. This name can be different from the model ID.

# [Python](#tab/python)

#### Use Microsoft Entra ID authentication

For Messages API endpoints, use your base URL with Microsoft Entra ID authentication.

1. **Install the Azure Identity client library**: You need to install this library to use the `DefaultAzureCredential`. Authorization is easiest when you use `DefaultAzureCredential`, as it finds the best credential to use in its running environment.

    ```bash
    pip install azure.identity
    ```

    Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra ID application as environment variables: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`.

    ```bash
    export AZURE_CLIENT_ID="<AZURE_CLIENT_ID>"
    export AZURE_TENANT_ID="<AZURE_TENANT_ID>"
    export AZURE_CLIENT_SECRET="<AZURE_CLIENT_SECRET>"
    ```

1. **Install dependencies:** Install the Anthropic SDK by using pip (requires: Python >=3.8).

    ```bash
    pip install -U "anthropic"
    ```

1. **Run a basic code sample:** This sample completes the following tasks:

    1. Creates a client with the Anthropic SDK, using Microsoft Entra ID authentication.
    1. Makes a basic call to the Messages API. The call is synchronous.

    ```python
    from anthropic import AnthropicFoundry
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
    baseURL = "https://<resource-name>.services.ai.azure.com/anthropic" # Your base URL. Replace <resource-name> with your resource name
    deploymentName = "claude-sonnet-4-5" # Replace with your deployment name
    
    # Create token provider for Entra ID authentication
    tokenProvider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    
    # Create client with Entra ID authentication
    client = AnthropicFoundry(
        azure_ad_token_provider=tokenProvider,
        base_url=baseURL
    )
    
    # Send request
    message = client.messages.create(
        model=deployment_name,
        messages=[
            {"role": "user", "content": "What is the capital/major city of France?"}
        ],
        max_tokens=1024,
    )
    
    print(message.content)
    ```

#### Use API key authentication

For Messages API endpoints, use your base URL and API key to authenticate against the service.

1. **Install dependencies:** Install the Anthropic SDK by using pip (requires: Python >=3.8):

    ```bash
    pip install -U "anthropic"
    ```

1. **Run a basic code sample:** This sample completes the following tasks:

    1. Creates a client with the Anthropic SDK by passing your API key to the SDK's configuration. This authentication method lets you interact seamlessly with the service.
    1. Makes a basic call to the Messages API. The call is synchronous.

    ```python
    from anthropic import AnthropicFoundry
    
    baseURL = "https://<resource-name>.services.ai.azure.com/anthropic" # Your base URL. Replace <resource-name> with your resource name
    deploymentName = "claude-sonnet-4-5" # Replace with your deployment name
    apiKey = "YOUR_API_KEY" # Replace YOUR_API_KEY with your API key
    
    # Create client with API key authentication
    client = AnthropicFoundry(
        api_key=apiKey,
        base_url=baseURL
    )
    
    # Send request
    message = client.messages.create(
        model=deploymentName,
        messages=[
            {"role": "user", "content": "What is the capital/major city of France?"}
        ],
        max_tokens=1024,
    )
    
    print(message.content)
    ```

# [JavaScript](#tab/javascript)

#### Use Microsoft Entra ID authentication

For Messages API endpoints, use your base URL with Microsoft Entra ID authentication.

1. **Install the Azure Identity client library**: Install the `@azure/identity` package to use the `DefaultAzureCredential`. Authorization is easiest when you use `DefaultAzureCredential`, as it finds the best credential to use in its running environment.

    ```bash
    npm install @azure/identity
    ```

    Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra ID application as environment variables: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`.

    ```bash
    export AZURE_CLIENT_ID="<AZURE_CLIENT_ID>"
    export AZURE_TENANT_ID="<AZURE_TENANT_ID>"
    export AZURE_CLIENT_SECRET="<AZURE_CLIENT_SECRET>"
    ```

1. **Install dependencies**

    1. Install [Node.js](https://nodejs.org/) 20 LTS or later ([non-EOL](https://endoflife.date/nodejs)) versions.

    1. Copy the following lines of text and save them as a file `package.json` inside your folder.

        ```json
        {
          "type": "module",
          "dependencies": {
            "@anthropic-ai/sdk": "latest",
            "@azure/identity": "latest"
          }
        }
        ```

        > [!NOTE]
        > @azure/core-sse is only needed when you stream the response.

    1. Open a terminal window in this folder and run `npm install`.

    1. For each of the code snippets that follow, copy the content into a file `sample.js` and run with `node sample.js`.

1. **Run a basic code sample.** This sample completes the following tasks:

    1. Creates a client with the Anthropic SDK, using Microsoft Entra ID authentication.
    1. Makes a basic call to the Messages API. The call is synchronous.

    ```javascript
    import AnthropicFoundry from '@anthropic-ai/foundry-sdk';
    import { getBearerTokenProvider, DefaultAzureCredential } from "@azure/identity";
    
    const baseURL = "https://<resource-name>.services.ai.azure.com/anthropic"; // Your base URL. Replace <resource-name> with your resource name
    const deploymentName = "claude-sonnet-4-5" // Replace with your deployment name
    
    // Create token provider for Entra ID authentication
    const tokenProvider = getBearerTokenProvider(
        new DefaultAzureCredential(),
        'https://cognitiveservices.azure.com/.default');
    
    // Create client with Entra ID authentication
    const client = new AnthropicFoundry({
        azureADTokenProvider: tokenProvider,
        baseURL: baseURL,
        apiVersion: "2023-06-01"
    });
    
    // Send request
    const message = await client.messages.create({
        model: deploymentName,
        messages: [{ role: "user", content: "What is the capital/major city of France?" }],
        max_tokens: 1024,
    });
    console.log(message);
    ```

#### Use API key authentication

For Messages API endpoints, use your base URL and API key to authenticate against the service.

1. **Install dependencies**

    1. Install [Node.js](https://nodejs.org/) 20 LTS or later ([non-EOL](https://endoflife.date/nodejs)) versions.

    1. Copy the following lines of text and save them as a file `package.json` inside your folder.

        ```json
        {
          "type": "module",
          "dependencies": {
            "@anthropic-ai/sdk": "latest"
          }
        }
        ```

        > [!NOTE]
        > @azure/core-sse is only needed when you stream the response.

    1. Open a terminal window in this folder and run `npm install`.

    1. For each of the code snippets that follow, copy the content into a file `sample.js` and run with `node sample.js`.

1. **Run a basic code sample.** This sample completes the following tasks:

    1. Creates a client with the Anthropic SDK by passing your API key to the SDK's configuration. This authentication method lets you interact seamlessly with the service.
    1. Makes a basic call to the Messages API. The call is synchronous.

    ```javascript
    import AnthropicFoundry from '@anthropic-ai/foundry-sdk';
    
    const baseURL = "https://<resource-name>.services.ai.azure.com/anthropic"; // Your base URL. Replace <resource-name> with your resource name
    const deploymentName = "claude-sonnet-4-5" // Replace with your deployment name
    const apiKey = "<your-api-key>"; // Your API key
    
    // Create client with API key
    const client = new AnthropicFoundry({
        apiKey: apiKey,
        baseURL: baseURL,
        apiVersion: "2023-06-01"
    });
    
    // Send request
    const message = await client.messages.create({
        model: deploymentName,
        messages: [{ role: "user", content: "What is the capital/major city of France?" }],
        max_tokens: 1024,
    });
    console.log(message);
    ```

For a list of supported runtimes, see [Requirements to use Anthropic TypeScript API Library](https://github.com/anthropics/anthropic-sdk-typescript#requirements).

# [REST API](#tab/rest-api)

#### Use Microsoft Entra ID authentication

For Messages API endpoints, use the deployed model's endpoint URI `https://<resource-name>.services.ai.azure.com/anthropic/v1/messages` with Microsoft Entra ID authentication.

If you configure the resource with Microsoft Entra ID support, pass your token in the Authorization header with the format `Bearer $AZURE_AUTH_TOKEN`. Use scope `https://cognitiveservices.azure.com/.default`. Using Microsoft Entra ID might require additional configuration in your resource to grant access. For more information, see [configure authentication with Microsoft Entra ID](/azure/ai-foundry/foundry-models/how-to/configure-entra-id?tabs=rest#use-microsoft-entra-id-in-your-code).

1. Export your Microsoft Entra ID token to an environment variable:

    If you're using bash:

    ```bash
    export AZURE_AUTH_TOKEN="<your-entra-id-key>"
    ```

    If you're in PowerShell:

    ```powershell
    $Env:AZURE_AUTH_TOKEN = "<your-entra-id-key>"
    ```

    If you're using Windows command prompt:

    ```
    set AZURE_AUTH_TOKEN = <your-entra-id-key>
    ```

1. Run the following cURL command. For cURL, use your deployment's target URI `https://<resource-name>.services.ai.azure.com/anthropic/v1/messages`.

    ```sh
    curl -X POST https://<resource-name>.services.ai.azure.com/anthropic/v1/messages \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $AZURE_AUTH_TOKEN" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "messages": [
          {
            "role": "system", "content": "You are a helpful assistant."
          },
          {
            "role": "user", "content": "What are 3 things to visit in Seattle?"
          }
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
        "model": "claude-sonnet-4-5"
        }'
    ```

#### Use API key authentication

For Messages API endpoints, use the deployed model's endpoint URI `https://<resource-name>.services.ai.azure.com/anthropic/v1/messages` and API key to authenticate against the service.

1. Export your API key to an environment variable:

    If you're using bash:

    ```bash
    export AZURE_API_KEY="<your-api-key>"
    ```

    If you're in PowerShell:

    ```powershell
    $Env:AZURE_API_KEY = "<your-api-key>"
    ```

    If you're using Windows command prompt:

    ```
    set AZURE_API_KEY = <your-api-key>
    ```

1. Run the following cURL command:

    ```sh
    curl -X POST https://<resource-name>.services.ai.azure.com/anthropic/v1/messages \
      -H "Content-Type: application/json" \
      -H "x-api-key: $AZURE_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "messages": [
          {
            "role": "system", "content": "You are a helpful assistant."
          },
          {
            "role": "user", "content": "What are 3 things to visit in Seattle?"
          }
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
        "model": "claude-sonnet-4-5"
        }'
    ```

---

## Agent support

- [Microsoft Agent Framework](/agent-framework/user-guide/agents/agent-types/anthropic-agent) supports creating agents that use Claude models.
- You can build custom AI agents with the [Claude Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview).

## Claude advanced features and capabilities

Claude in Foundry Models supports advanced features and capabilities. 
**Core capabilities** enhance Claude's fundamental abilities for processing, analyzing, and generating content across various formats and use cases. **Tools** enable Claude to interact with external systems, execute code, and perform automated tasks through various tool interfaces. 

Some of the **Core capabilities** that Foundry supports are:

- **1 million token context window:** An extended context window.
- **Agent skills:** Extend Claude's capabilities with Skills.
- **Citations:** Ground Claude's responses in source documents.
- **Context editing:** Automatically manage conversation context with configurable strategies.
- **Extended thinking:** Enhanced reasoning capabilities for complex tasks.
- **PDF support:** Process and analyze text and visual content from PDF documents.
- **Prompt caching:** Provide Claude with more background knowledge and example outputs to reduce costs and latency.

Some of the **Tools** that Foundry supports are:

- **MCP connector:** Connect to remote MCP servers directly from the Messages API without a separate MCP client.
- **Memory:** Store and retrieve information across conversations. Build knowledge bases over time, maintain project context, and learn from past interactions.
- **Web fetch:** Retrieve full content from specified web pages and PDF documents for in-depth analysis.

For a full list of the supported capabilities and tools, see [Claude's features overview](https://docs.claude.com/en/docs/build-with-claude/overview).

## API quotas and limits

> [!IMPORTANT]
> At this time, only Enterprise and MCA-E subscriptions are eligible for Claude model usage in Foundry.

Claude models in Foundry have the following rate limits, measured in Tokens Per Minute (TPM) and Requests Per Minute (RPM):

| Model        |   Deployment Type       | Default RPM   | Default TPM   |Enterprise and MCA-E RPM   |Enterprise and MCA-E TPM   |
|:------------------|:----------------|:--------------|:--------------|:-----------|:-----------|
| claude-haiku-4-5  | [Global Standard](../concepts/deployment-types.md#global-standard)  | 0         | 0     | 4,000      | 4,000,000  |
| claude-opus-4-1   | Global Standard  |0        | 0    | 2,000      | 2,000,000  |
| claude-sonnet-4-5 | Global Standard  |0        | 0    | 4,000      | 2,000,000  |
| claude-opus-4-5   | Global Standard |0        | 0    | 2,000      | 2,000,000  |

To increase your quota beyond the default limits, submit a request through the [quota increase request form](https://aka.ms/oai/stuquotarequest).


### Rate limit best practices

To optimize your usage and avoid rate limiting:

- **Implement retry logic**: Handle 429 responses with exponential backoff
- **Batch requests**: Combine multiple prompts when possible
- **Monitor usage**: Track your token consumption and request patterns
- **Use appropriate models**: Choose the right Claude model for your use case

## Responsible AI considerations

When using Claude models in Foundry, consider these responsible AI practices:

::: moniker range="foundry-classic"

- Configure AI content safety during model inference, as Foundry doesn't provide built-in content filtering for Claude models at deployment time. To learn how to create and use content filters, see [Configure content filtering for Foundry Models](configure-content-filters.md).

- Ensure your applications comply with [Anthropic's Acceptable Use Policy](https://www.anthropic.com/legal/aup). Also, see details of safety evaluations for [Claude Opus 4.5](http://www.anthropic.com/claude-opus-4-5-system-card), [Claude Haiku 4.5](https://assets.anthropic.com/m/99128ddd009bdcb/Claude-Haiku-4-5-System-Card.pdf), [Claude Opus 4.1](https://assets.anthropic.com/m/4c024b86c698d3d4/original/Claude-4-1-System-Card.pdf), and [Claude Sonnet 4.5](https://assets.anthropic.com/m/12f214efcc2f457a/original/Claude-Sonnet-4-5-System-Card.pdf).

::: moniker-end

::: moniker range="foundry"

- Configure AI content safety during model inference, as Foundry doesn't provide built-in content filtering for Claude models at deployment time.

- Ensure your applications comply with [Anthropic's Acceptable Use Policy](https://www.anthropic.com/legal/aup). Also, see details of safety evaluations for [Claude Opus 4.5](http://www.anthropic.com/claude-opus-4-5-system-card), [Claude Haiku 4.5](https://assets.anthropic.com/m/99128ddd009bdcb/Claude-Haiku-4-5-System-Card.pdf), [Claude Opus 4.1](https://assets.anthropic.com/m/4c024b86c698d3d4/original/Claude-4-1-System-Card.pdf), and [Claude Sonnet 4.5](https://assets.anthropic.com/m/12f214efcc2f457a/original/Claude-Sonnet-4-5-System-Card.pdf).

::: moniker-end

## Best practices

Follow these best practices when working with Claude models in Foundry:

#### Model selection

Choose the appropriate Claude model based on your specific requirements:

- **Claude Opus 4.5**: For best performance across coding, agents, computer use, and enterprise workflows
- **Claude Sonnet 4.5**: For balanced performance and capabilities, production workflows
- **Claude Haiku 4.5**: For speed and cost optimization, high-volume processing
- **Claude Opus 4.1**: For complex reasoning and enterprise applications

#### Prompt engineering

- **Clear instructions**: Provide specific and detailed prompts
- **Context management**: Effectively use the available context window
- **Role definitions**: Use system messages to define the assistant's role and behavior
- **Structured prompts**: Use consistent formatting for better results

#### Cost optimization

- **Token management**: Monitor and optimize token usage
- **Model selection**: Use the most cost-effective model for your use case
- **Caching**: Implement [explicit prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching#continuing-a-multi-turn-conversation) where appropriate
- **Request batching**: Combine multiple requests when possible

## Related content

- [Data, privacy, and security for Claude models in Microsoft Foundry (preview)](../../responsible-ai/claude-models/data-privacy.md)
- [Monitor model usage and costs](../../how-to/costs-plan-manage.md)
- [How to generate text responses with Microsoft Foundry Models](generate-responses.md)
- [Explore Microsoft Foundry Models](../../concepts/foundry-models-overview.md)
- [Claude Docs: Claude in Microsoft Foundry](https://docs.claude.com/en/docs/build-with-claude/claude-in-microsoft-foundry)
