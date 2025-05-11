---
title: 'Quickstart: Use the OpenAI Service to make your first completions call with the REST API'
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the REST API. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/26/2025
---

## Prerequisites

- An Azure subscription - <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">Create one for free</a>
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>
- The following Python libraries: os, requests, json
- An Azure OpenAI resource with a model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

## Set up

### Retrieve key and endpoint

To successfully make a call against Azure OpenAI, you'll need the following:

|Variable name | Value |
|--------------------------|-------------|
| `ENDPOINT`               | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can also find the endpoint via the **Deployments** page in Azure AI Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`.|
| `API-KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|
| `DEPLOYMENT-NAME` | This value will correspond to the custom name you chose for your deployment when you deployed a model. This value can be found under **Resource Management** > **Deployments** in the Azure portal or via the **Deployments** page in Azure AI Foundry portal.|

Go to your resource in the Azure portal. The **Endpoint and Keys** can be found in the **Resource Management** section. Copy your endpoint and access key as you'll need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot of the overview blade for an Azure OpenAI resource in the Azure portal with the endpoint & access keys location circled in red." lightbox="../media/quickstarts/endpoint.png":::

[!INCLUDE [environment-variables](environment-variables.md)]


## REST API

In a bash shell, run the following command. You will need to replace `gpt-35-turbo-instruct` with the deployment name you chose when you deployed the `gpt-35-turbo-instruct` model. Entering the model name will result in an error unless you chose a deployment name that is identical to the underlying model name.

# [Microsoft Entra ID](#tab/entra)

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/deployments/gpt-35-turbo-instruct/completions?api-version=2024-10-21 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d "{\"prompt\": \"Once upon a time\"}"
```

# [API Key](#tab/key)

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/deployments/gpt-35-turbo-instruct/completions?api-version=2024-10-21 \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -d "{\"prompt\": \"Once upon a time\"}"
```

---

The format of your first line of the command with an example endpoint would appear as follows `curl https://docs-test-001.openai.azure.com/openai/deployments/{YOUR-DEPLOYMENT_NAME_HERE}/completions?api-version=2024-10-21 \`. If you encounter an error double check to make sure that you don't have a doubling of the `/` at the separation between your endpoint and `/openai/deployments`.

If you want to run this command in a normal Windows command prompt you would need to alter the text to remove the `\` and line breaks.

> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see the Azure AI services [security](../../security-features.md) article.

## Output

The output from the completions API will look as follows.

```json
{
    "id": "ID of your call",
    "object": "text_completion",
    "created": 1675444965,
    "model": "gpt-35-turbo-instruct",
    "choices": [
        {
            "text": " there lived in a little village a woman who was known as the meanest",
            "index": 0,
            "finish_reason": "length",
            "logprobs": null
        }
    ],
    "usage": {
        "completion_tokens": 16,
        "prompt_tokens": 3,
        "total_tokens": 19
    }
}
```


The Azure OpenAI in Azure AI Foundry Models also performs content moderation on the prompt inputs and generated outputs. The prompts or responses may be filtered if harmful content is detected. For more information, see the [content filter](../concepts/content-filter.md) article.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Learn more about how to generate the best completion in our [How-to guide on completions](../how-to/completions.md).
* For more examples check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
