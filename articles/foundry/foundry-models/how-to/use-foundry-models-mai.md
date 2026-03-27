---
title: "Deploy and use MAI-image-2 model in Microsoft Foundry"
description: "Deploy MAI-image-2, a Microsoft AI-owned text-to-image generation model in Microsoft Foundry, to generate high-quality photorealistic images from text prompts."
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/25/2026
ms.custom:
  - doc-kit-assisted
  - classic-and-new
author: msakande
ms.author: mopeakande
ms.reviewer: malpande
reviewer: mpande98
ai-usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy and use MAI-image-2 in Microsoft Foundry so I can generate high-quality photorealistic images in my applications.
---

# Deploy and use MAI-image-2 in Microsoft Foundry (preview)

MAI-image-2 (Preview) is a text-to-image generation model designed to create high-quality, visually rich images from natural language prompts. It uses a diffusion-based generative approach to progressively refine images, enabling strong alignment between the input text and the generated output. The model is optimized to produce diverse and coherent images across a wide range of creative and design scenarios, making it well suited for tasks such as concept visualization, creative content generation, and image design workflows.

In this article, you learn how to:

- Deploy MAI-image-2 in Microsoft Foundry
- Authenticate by using Microsoft Entra ID or API keys
- Generate images by using the MAI image generation API

## Key model capabilities

- **Text-to-image generation:** Generates high-quality images from natural language prompts, enabling users to translate textual descriptions into visually coherent outputs suitable for a wide range of creative and design use cases.
- **Photorealistic image synthesis:** Capable of generating realistic imagery with consistent visual structure, making it suitable for concept visualization and content creation scenarios.
- **General-purpose image generation:** Designed as a general-purpose image generation model that can be applied across multiple creative, design, and visualization workflows rather than being optimized for a single narrow domain.

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go).
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../how-to/create-projects.md). MAI-image-2 is available for **global standard deployment in all regions**.
- **Contributor** or **Owner** role on the resource group to deploy models. For more information, see [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).

## Deploy MAI-image-2

MAI-image-2 is available for [global standard deployment](../concepts/deployment-types.md#global-standard) in all regions. To deploy the model, follow the instructions in [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md).

Alternatively, you can deploy the model by using the Azure CLI:

```bash
az cognitiveservices account deployment create \
  --name <ACCOUNT_NAME> \
  --resource-group <RESOURCE_GROUP> \
  --deployment-name <DEPLOYMENT_NAME> \
  --model-name mai-image-2 \
  --model-format Microsoft \
  --model-version 2026-02-20 \
  --sku-name GlobalStandard \
  --sku-capacity 1
```

**Reference:** [az cognitiveservices account deployment create](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-create)

After deployment, use the [Foundry playground](../../concepts/concept-playgrounds.md) to interactively test the model with text prompts.

## Overview of image generation with MAI-image-2

After you deploy MAI-image-2, use the **MAI image generation API** to generate images. This is a Microsoft-managed endpoint that accepts a text prompt and returns a PNG image.

#### API endpoint

The API endpoint has the following form:

```
https://<resource-name>.services.ai.azure.com/mai/v1/images/generations
```

To authenticate, you need your **resource endpoint** and either a **Microsoft Entra ID token** or an **API key**. You can find these values in the **Keys and Endpoint** section of your resource in the Azure portal, or on the deployment details page in the [Foundry portal](https://ai.azure.com).

#### Model capabilities

The model accepts text input (32,000 tokens) and outputs one PNG image. Supported output resolutions range from **256×256** to **1024×1024** pixels, with `width` and `height` configurable independently within that range depending on aspect ratio.

The following table lists the request parameters:

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `model` | string | The deployment name you assigned when you deployed the model. |
| `prompt` | string | The text prompt that describes the image to generate. Maximum context length: 32,000 tokens. |
| `width` | string | Width of the output image in pixels. Supported range: 256–1024. |
| `height` | string | Height of the output image in pixels. Supported range: 256–1024. |

> [!NOTE]
> The output format is always PNG. The maximum output resolution is 1024×1024 pixels.

See [the Microsoft model collection in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=Microsoft/?cid=learnDocs) for a list of the model's capabilities.

## Generate images

The following examples show how to generate an image from a text prompt using MAI-image-2 with the MAI image generation API.

# [Python](#tab/python)

#### Use API key authentication

1. **Install the `requests` library:**

    ```bash
    pip install requests
    ```

1. **Set environment variables:**

    ```bash
    export AZURE_ENDPOINT="https://<resource-name>.services.ai.azure.com"
    export AZURE_API_KEY="<your-api-key>"
    export DEPLOYMENT_NAME="<your-deployment-name>"
    ```

1. **Run the following code:**

    ```python
    import os
    import requests

    endpoint = os.environ["AZURE_ENDPOINT"]
    api_key = os.environ["AZURE_API_KEY"]
    deployment_name = os.environ["DEPLOYMENT_NAME"]

    url = f"{endpoint}/mai/v1/images/generations"

    payload = {
        "model": deployment_name,
        "prompt": "A photorealistic image of a mountain lake at sunrise",
        "width": "1024",
        "height": "1024",
    }

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
        },
        json=payload,
    )
    response.raise_for_status()

    result = response.json()
    print(result)
    ```

    **Expected output:** A JSON response containing the generated image data in PNG format.

#### Use Microsoft Entra ID authentication

To use Microsoft Entra ID instead of an API key, replace the `api-key` header with a bearer token obtained using the `DefaultAzureCredential`:

1. **Install the Azure Identity library:**

    ```bash
    pip install azure-identity
    ```

1. **Update the request headers in the previous code:**

    ```python
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    token = token_provider()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    ```

    **Reference:** [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

# [REST API](#tab/rest-api)

#### Use API key authentication

Export your endpoint and API key, then run the following cURL command:

```bash
export AZURE_API_KEY="<your-api-key>"
export DEPLOYMENT_NAME="<your-deployment-name>"
```

```sh
curl -X POST "https://<resource-name>.services.ai.azure.com/mai/v1/images/generations" \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_API_KEY" \
  -d '{
      "model": "'"$DEPLOYMENT_NAME"'",
      "prompt": "A photorealistic image of a mountain lake at sunrise",
      "width": "1024",
      "height": "1024"
    }'
```

**Expected output:** A JSON response containing the generated image data in PNG format.

#### Use Microsoft Entra ID authentication

Replace the `api-key` header with an `Authorization` header:

```sh
-H "Authorization: Bearer $AZURE_AUTH_TOKEN"
```

Where `AZURE_AUTH_TOKEN` is a valid Microsoft Entra ID token scoped to `https://cognitiveservices.azure.com/.default`.

---

## API quotas and limits

MAI-image-2 has the following rate limits measured in Requests Per Minute (RPM). The tier available to you depends on your subscription and deployment configuration.

| Model | Deployment Type | Tier | Requests Per Minute (RPM) |
| -- | -- | -- | -- |
| MAI-image-2 | Global Standard | 1 | 9 |
| MAI-image-2 | Global Standard | 2 | 15 |
| MAI-image-2 | Global Standard | 3 | 30 |
| MAI-image-2 | Global Standard | 4 | 45 |
| MAI-image-2 | Global Standard | 5 | 60 |
| MAI-image-2 | Global Standard | 6 | 90 |

To request a quota increase, submit the [quota increase request form](https://aka.ms/oai/stuquotarequest). Requests are processed in the order they're received, and priority goes to customers who actively use their existing quota allocation.

## Responsible AI considerations

When using MAI-image-2 in Foundry, consider these responsible AI practices:

- **Be aware of known limitations**: Despite technical mitigations such as data filtering and content classifiers applied at the system level, image generation models can produce harmful or unexpected content based on user requests. Common risk areas include violent or gory content, sexual content or nudity, depictions of public figures, and replication of trademarked or other protected material.
- **Configure content safety**: Apply additional mitigations appropriate to your use case, because no generative model is immune to adversarial prompts.
- **Comply with applicable terms**: Ensure your use of generated images complies with [Microsoft's terms of service](https://www.microsoft.com/en-us/legal/terms-of-use) and applicable copyright and intellectual property laws.
- **Be transparent**: Disclose that content is AI-generated when sharing or publishing images.
- **Avoid harmful content**: Don't generate content that could be harmful, misleading, or in violation of privacy.

## Related content

- [Explore available models in Foundry](../concepts/models-sold-directly-by-azure.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md)
- [Configure Microsoft Entra ID authentication](configure-entra-id.md)
