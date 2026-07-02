---
title: Include file
description: Include file
author: msakande
ms.reviewer: ambadal
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/23/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---


## Call the Claude Messages API

After you deploy a Claude model, interact with it to generate text responses:

- Use the [Anthropic SDKs](https://docs.claude.com/en/api/client-sdks) and the Claude APIs, such as:

    - [Messages API](https://docs.claude.com/en/api/messages): Send a structured list of input messages with text or image content. The model generates the next message in the conversation.
    - [Token Count API](https://docs.claude.com/en/api/messages-count-tokens): Count the number of tokens in a message.
    
To learn more about the supported APIs, see [Claude models in Microsoft Foundry](../concepts/claude-models.md).

### Send messages with authentication

The following examples show how to send requests to Claude Sonnet 4.6 using Microsoft Entra ID or API key authentication. To work with your deployed model, you need:

- Your base URL, which is of the form `https://<resource name>.services.ai.azure.com/anthropic`.
- Your target URI from your deployment details, which is of the form `https://<resource name>.services.ai.azure.com/anthropic/v1/messages`.
- Microsoft Entra ID for keyless authentication or your deployment's API key for API authentication.
- Deployment name you chose during deployment creation. This name can be different from the model ID.

For advanced features and capabilities of Claude models, see [Claude models in Microsoft Foundry](../concepts/claude-models.md).

# [Python](#tab/python)

#### Use Microsoft Entra ID authentication

For Messages API endpoints, use your base URL with Microsoft Entra ID authentication.

1. **Install the Azure Identity client library**: Install this library to use the `DefaultAzureCredential`. Authorization is easiest when you use `DefaultAzureCredential` because it finds the best credential to use in its running environment.

    ```bash
    pip install azure-identity
    ```

    Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra ID application as environment variables: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`.

    ```bash
    export AZURE_CLIENT_ID="<AZURE_CLIENT_ID>"
    export AZURE_TENANT_ID="<AZURE_TENANT_ID>"
    export AZURE_CLIENT_SECRET="<AZURE_CLIENT_SECRET>"
    ```

1. **Install dependencies**: Install the Anthropic SDK by using pip (requires Python 3.8 or later).

    ```bash
    pip install -U "anthropic"
    ```

1. **Run a basic code sample** to complete the following tasks:

    1. Create a client with the Anthropic SDK, using Microsoft Entra ID authentication.
    1. Make a basic call to the Messages API. The call is synchronous.

    ```python
    from anthropic import AnthropicFoundry
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
    baseURL = "https://<resource-name>.services.ai.azure.com/anthropic" # Your base URL. Replace <resource-name> with your resource name
    deploymentName = "claude-sonnet-4-6" # Replace with your deployment name
    
    # Create token provider for Entra ID authentication
    tokenProvider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.cognitiveservices.com/.default"
    )
    
    # Create client with Entra ID authentication
    client = AnthropicFoundry(
        azure_ad_token_provider=tokenProvider,
        base_url=baseURL
    )
    
    # Send request
    message = client.messages.create(
        model=deploymentName,
        messages=[
            {"role": "user", "content": "What are 3 things to visit in Seattle?"}
        ],
        max_tokens=1048,
        temperature=1,
        thinking={"type":"adaptive"},
        output_config={"effort": "max"},
        stream=False
    )
    
    print(message.content)
    ```

    **Expected output:** A JSON response containing the model's text completion with three Seattle recommendations.

    **Reference:** [Anthropic Client SDK](https://docs.claude.com/en/api/client-sdks), [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

#### Use API key authentication

> [!IMPORTANT]
> Claude **Mythos 5** and **Mythos Preview** support Microsoft Entra ID authentication only.

For Messages API endpoints, use your base URL and API key to authenticate against the service.

1. **Install dependencies**: Install the Anthropic SDK by using pip (requires Python 3.8 or later):

    ```bash
    pip install -U "anthropic"
    ```

1. **Run a basic code sample** to complete the following tasks:

    1. Create a client with the Anthropic SDK by passing your API key to the SDK's configuration. This authentication method lets you interact seamlessly with the service.
    1. Make a basic call to the Messages API. The call is synchronous.

    ```python
    from anthropic import AnthropicFoundry
    
    baseURL = "https://<resource-name>.services.ai.azure.com/anthropic" # Your base URL. Replace <resource-name> with your resource name
    deploymentName = "claude-sonnet-4-6" # Replace with your deployment name
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
            {"role": "user", "content": "What are 3 things to visit in Seattle?"}
        ],
        max_tokens=1048,
        temperature=1,
        thinking={"type":"adaptive"},
        output_config={"effort": "max"},
        stream=False
    )
    
    print(message.content)
    ```

    **Expected output:** A JSON response containing the model's text completion with three Seattle recommendations.

    **Reference:** [Anthropic Client SDK](https://docs.claude.com/en/api/client-sdks)

# [JavaScript](#tab/javascript)

#### Use Microsoft Entra ID authentication

For Messages API endpoints, use your base URL with Microsoft Entra ID authentication.

1. **Install the Azure Identity client library**: Install the `@azure/identity` package to use the `DefaultAzureCredential`. Authorization is easiest when you use `DefaultAzureCredential` because it finds the best credential to use in its running environment.

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
            "@anthropic-ai/foundry-sdk": "latest",
            "@azure/identity": "latest"
          }
        }
        ```

    1. Open a terminal window in this folder and run `npm install`.

    1. For each of the code snippets that follow, copy the content into a file `sample.js` and run with `node sample.js`.

1. **Run a basic code sample** to complete the following tasks:

    1. Creates a client with the Anthropic SDK, using Microsoft Entra ID authentication.
    1. Makes a basic call to the Messages API. The call is synchronous.

    ```javascript
    import AnthropicFoundry from '@anthropic-ai/foundry-sdk';
    import { getBearerTokenProvider, DefaultAzureCredential } from "@azure/identity";
    
    const baseURL = "https://<resource-name>.services.ai.azure.com/anthropic"; // Your base URL. Replace <resource-name> with your resource name
    const deploymentName = "claude-sonnet-4-6" // Replace with your deployment name
    
    // Create token provider for Entra ID authentication
    const tokenProvider = getBearerTokenProvider(
        new DefaultAzureCredential(),
        'https://ai.cognitiveservices.com/.default');
    
    // Create client with Entra ID authentication
    const client = new AnthropicFoundry({
        azureADTokenProvider: tokenProvider,
        baseURL: baseURL,
        apiVersion: "2023-06-01"
    });
    
    // Send request
    const message = await client.messages.create({
        model: deploymentName,
        messages: [{ role: "user", content: "What are 3 things to visit in Seattle?" }],
        max_tokens: 1048,
        temperature: 1,
        thinking: {"type": "adaptive"},
        output_config: {"effort": "max"},
        stream: false
    });
    console.log(message);
    ```

    **Expected output:** A JSON response containing the model's text completion with three Seattle recommendations.

    **Reference:** [Anthropic Client SDK](https://docs.claude.com/en/api/client-sdks), [DefaultAzureCredential](/javascript/api/@azure/identity/defaultazurecredential)

#### Use API key authentication

> [!IMPORTANT]
> Claude **Mythos 5** and **Mythos Preview** support Microsoft Entra ID authentication only.

For Messages API endpoints, use your base URL and API key to authenticate against the service.

1. **Install dependencies**

    1. Install [Node.js](https://nodejs.org/) 20 LTS or later ([non-EOL](https://endoflife.date/nodejs)) versions.

    1. Copy the following lines of text and save them as a file `package.json` inside your folder.

        ```json
        {
          "type": "module",
          "dependencies": {
            "@anthropic-ai/foundry-sdk": "latest"
          }
        }
        ```

    1. Open a terminal window in this folder and run `npm install`.

    1. For each of the code snippets that follow, copy the content into a file `sample.js` and run with `node sample.js`.

1. **Run a basic code sample.** This sample completes the following tasks:

    1. Creates a client with the Anthropic SDK by passing your API key to the SDK's configuration. This authentication method lets you interact seamlessly with the service.
    1. Makes a basic call to the Messages API. The call is synchronous.

    ```javascript
    import AnthropicFoundry from '@anthropic-ai/foundry-sdk';
    
    const baseURL = "https://<resource-name>.services.ai.azure.com/anthropic"; // Your base URL. Replace <resource-name> with your resource name
    const deploymentName = "claude-sonnet-4-6" // Replace with your deployment name
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
        messages: [{ role: "user", content: "What are 3 things to visit in Seattle?" }],
        max_tokens: 1048,
        temperature: 1,
        thinking: {"type": "adaptive"},
        output_config: {"effort": "max"},
        stream: false
    });
    console.log(message);
    ```

    **Expected output:** A JSON response containing the model's text completion with three Seattle recommendations.

    **Reference:** [AnthropicFoundry SDK](https://docs.claude.com/en/api/client-sdks)

For a list of supported runtimes, see [Requirements to use Anthropic TypeScript API Library](https://github.com/anthropics/anthropic-sdk-typescript#requirements).

# [REST API](#tab/rest-api)

#### Use Microsoft Entra ID authentication

For Messages API endpoints, use the deployed model's endpoint URI `https://<resource-name>.services.ai.azure.com/anthropic/v1/messages` with Microsoft Entra ID authentication.

If you configure the resource with Microsoft Entra ID support, pass your token in the Authorization header with the format `Bearer $AZURE_AUTH_TOKEN`. Use scope `https://ai.cognitiveservices.com/.default`. Using Microsoft Entra ID might require additional configuration in your resource to grant access. For more information, see [Configure authentication with Microsoft Entra ID](/azure/ai-foundry/foundry-models/how-to/configure-entra-id?tabs=rest#use-microsoft-entra-id-in-your-code).

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
            "role": "user", "content": "You are a helpful assistant."
          },
          {
            "role": "user", "content": "What are 3 things to visit in Seattle?"
          }
        ],
        "max_tokens": 1048,
        "temperature": 1,
        "model": "claude-sonnet-4-6",
        "thinking": {"type":"adaptive"},
        "output_config": {"effort": "max"},
        "stream": false
        }'
    ```

    **Expected output:** A JSON response containing the model's text completion with three Seattle recommendations.

    **Reference:** [Claude Messages API](https://docs.claude.com/en/api/messages)

#### Use API key authentication

> [!IMPORTANT]
> Claude **Mythos 5** and **Mythos Preview** support Microsoft Entra ID authentication only.

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
            "role": "user", "content": "You are a helpful assistant."
          },
          {
            "role": "user", "content": "What are 3 things to visit in Seattle?"
          }
        ],
        "max_tokens": 1048,
        "temperature": 1,
        "model": "claude-sonnet-4-6",
        "thinking": {"type":"adaptive"},
        "output_config": {"effort": "max"},
        "stream": false
        }'
    ```

    **Expected output:** A JSON response containing the model's text completion with three Seattle recommendations.

    **Reference:** [Claude Messages API](https://docs.claude.com/en/api/messages)

---

## Troubleshooting

The following table lists common errors when you work with Claude models in Foundry and their solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid or expired API key, or incorrect Entra ID token scope. | Verify your API key is correct. For Entra ID, confirm you use scope `https://ai.cognitiveservices.com/.default`. |
| 403 Forbidden | Insufficient permissions on the resource or subscription. | Verify you have **Contributor** or **Owner** role on the resource group. For Entra ID, ensure the **Cognitive Services User** role is assigned. |
| 404 Not Found | Incorrect endpoint URL or deployment name. | Confirm your base URL follows the pattern `https://<resource-name>.services.ai.azure.com/anthropic` and the deployment name matches your configuration. |
| 429 Too Many Requests | Rate limit exceeded for your subscription tier. | Implement exponential backoff with retry logic. Consider reducing request frequency or requesting a [quota increase](https://aka.ms/oai/stuquotarequest). |
| Subscription eligibility error | Your Azure subscription type or billing region isn't supported, or your subscription tier has a default quota of 0 for the model. | Confirm your subscription has an active pay-as-you-go billing method and a supported billing country/region. See [Subscription type and region support](#subscription-type-and-region-support). For tier-specific default limits, see [Quotas, rate limits, and regions](../concepts/claude-models.md). |
| Region not available | Deployment attempted in an unsupported region. | For Global Standard deployments, deploy to **East US2** or **Sweden Central**. For `claude-opus-4-8` (Hosted on Azure) Data Zone Standard (US), deploy to a supported US data zone location. |

## Related content

- [Claude models in Microsoft Foundry](../concepts/claude-models.md)
- [Data, privacy, and security for Claude models in Microsoft Foundry (preview)](../../responsible-ai/claude-models/data-privacy.md)
- [Claude Consumption Units (CCU) billing in Microsoft Foundry](../concepts/claude-models-billing.md)
- [Claude on Foundry starter kit](https://github.com/Azure-Samples/claude#readme)
- [How to generate text responses with Microsoft Foundry Models](../how-to/generate-responses.md)
- [Explore Microsoft Foundry Models](../../../foundry-classic/concepts/foundry-models-overview.md)
- [Claude Docs: Claude in Microsoft Foundry](https://docs.claude.com/en/docs/build-with-claude/claude-in-microsoft-foundry)
