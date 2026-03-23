---
title: "Deploy and use FLUX models in Microsoft Foundry"
description: "Deploy Black Forest Labs FLUX image generation models in Microsoft Foundry to generate and edit high-quality images from text prompts and reference images."
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 03/23/2026
ms.custom:
  - doc-kit-assisted
  - classic-and-new
author: msakande
ms.author: mopeakande
ms.reviewer: malpande
reviewer: mpande98
ai-usage: ai-assisted

#CustomerIntent: As a developer or AI practitioner, I want to deploy and use FLUX image generation models in Microsoft Foundry so I can generate and edit high-quality images in my applications.
---

# Deploy and use FLUX models in Microsoft Foundry

Black Forest Labs (BFL) FLUX models bring state-of-the-art image generation to Microsoft Foundry, enabling you to generate and edit high-quality images from text prompts and reference images. In this article, you learn how to:

- Deploy FLUX models in Microsoft Foundry
- Authenticate by using Microsoft Entra ID or API keys
- Generate images by using the BFL provider-specific API or the Image API
- Edit images by combining text prompts with reference images
- Choose the right FLUX model for your use case

FLUX models are optimized for photorealism, prompt fidelity, and compositional control, making them well suited for creative, e-commerce, media, and design-centric applications. They support a range of capabilities including text-to-image generation, multi-reference image editing, and in-context generation and editing.

FLUX models in Foundry include:

| Model ID | Model name | Key capabilities |
| -- | -- | -- |
| `FLUX.2-flex` | FLUX.2 \[flex\] | Text-to-image generation; multi-reference image editing with up to 10 reference images |
| `FLUX.2-pro` | FLUX.2 \[pro\] | Text-to-image generation; multi-reference image editing with up to 8 reference images |
| `FLUX.1-Kontext-pro` | FLUX.1 Kontext \[pro\] | In-context generation and editing; character consistency |
| `FLUX-1.1-pro` | FLUX1.1 \[pro\] | Fast text-to-image generation |

To learn more about each model, see [Available FLUX models](#available-flux-models).

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go).
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../how-to/create-projects.md). FLUX models are available for global standard deployment in all regions.
- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace** to create subscriptions. Ensure that you have the [permissions required to subscribe to model offerings](configure-marketplace.md).
- **Contributor** or **Owner** role on the resource group to deploy models. For more information, see [Azure RBAC roles](https://learn.microsoft.com/azure/role-based-access-control/built-in-roles).
- **For FLUX.2 \[flex\]**: Approved registration. Use the [registration form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMzM2TDBZRko3QldSSFlWREhQSEpSSEdKVyQlQCN0PWcu) before you attempt deployment.

## Deploy FLUX models

FLUX models are available for [global standard deployment](../concepts/deployment-types.md#global-standard) in all regions. To deploy a FLUX model, follow the instructions in [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md).

After deployment, use the [Foundry playground](../../concepts/concept-playgrounds.md) to interactively test the model with text prompts.

> [!NOTE]
> Support for **multiple reference images** is available for FLUX.2 \[pro\] and FLUX.2 \[flex\] through the API, but not in the playground.

## Overview of image generation with FLUX models

After you deploy a FLUX model, use either the **BFL provider-specific API** or the **Image API** to generate images:

- **BFL provider-specific API**: Supports all FLUX models and provides access to additional parameters such as `guidance`, `steps`, `seed`, `aspect_ratio`, `safety_tolerance`, and `output_format`. Use this route for fine-grained control over generation.
- **Image API**: An OpenAI-compatible endpoint available for `FLUX.1-Kontext-pro` and `FLUX-1.1-pro`. Use this route if your application already uses the Azure OpenAI images API.

To authenticate, you need your **resource endpoint** and either a **Microsoft Entra ID token** or an **API key**. You can find these values in the **Keys and Endpoint** section of your resource in the Azure portal, or on the deployment details page in the [Foundry portal](https://ai.azure.com).

## Use the BFL provider-specific API with FLUX models

The BFL provider-specific API endpoint has the following form:

```
https://<resource-name>.api.cognitive.microsoft.com/providers/blackforestlabs/v1/<model-path>?api-version=preview
```

For each model, replace the model path `<model-path>` in the endpoint as follows:

> [!IMPORTANT]
> The model ID and `<model-path>` are not identical. Be sure to use the model path in the endpoint URL.

| Model | Model path |
| -- | -- |
| FLUX.2 \[flex\] | `flux-2-flex` |
| FLUX.2 \[pro\] | `flux-2-pro` |
| FLUX.1 Kontext \[pro\] | `flux-kontext-pro` |
| FLUX1.1 \[pro\] | `flux-pro-1.1` |

### Image generation (text to image)

The following examples use FLUX.2 \[pro\] to generate an image from a text prompt. For a FLUX.2 \[flex\]-specific example with its additional parameters (`guidance`, `steps`), see [FLUX.2 \[flex\] image generation](#flux2-flex-image-generation).

# [Python](#tab/python)

#### Use API key authentication

1. **Install the `requests` library:**

    ```bash
    pip install requests
    ```

1. **Set environment variables:**

    ```bash
    export AZURE_ENDPOINT="https://<resource-name>.api.cognitive.microsoft.com"
    export AZURE_API_KEY="<your-api-key>"
    ```

1. **Run the following code:**

    ```python
    import os
    import requests

    endpoint = os.environ["AZURE_ENDPOINT"]
    api_key = os.environ["AZURE_API_KEY"]

    url = f"{endpoint}/providers/blackforestlabs/v1/flux-2-pro?api-version=preview"

    payload = {
        "model": "FLUX.2-pro",
        "prompt": "A photograph of a red fox in an autumn forest",
        "width": 1024,
        "height": 1024,
        "output_format": "jpeg",
        "num_images": 1,
    }

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        json=payload,
    )
    response.raise_for_status()

    result = response.json()
    print(result)
    ```

    **Expected output:** A JSON response containing a URL or base64-encoded image data for the generated image.

    **Reference:** [BFL FLUX.2 text-to-image API](https://docs.bfl.ai/flux_2/flux2_text_to_image)

#### Use Microsoft Entra ID authentication

To use Microsoft Entra ID instead of an API key, replace the `Authorization` header value with a bearer token obtained using the `DefaultAzureCredential`:

1. **Install the Azure Identity library:**

    ```bash
    pip install azure-identity
    ```

1. **Update the authorization header in the previous code:**

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

    **Reference:** [DefaultAzureCredential](https://learn.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential)

# [REST API](#tab/rest-api)

#### Use API key authentication

Export your API key and run the following cURL command:

```bash
export AZURE_API_KEY="<your-api-key>"
```

```sh
curl -X POST https://<resource-name>.api.cognitive.microsoft.com/providers/blackforestlabs/v1/flux-2-pro?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_API_KEY" \
  -d '{
      "model": "FLUX.2-pro",
      "prompt": "A photograph of a red fox in an autumn forest",
      "width": 1024,
      "height": 1024,
      "output_format": "jpeg",
      "num_images": 1
    }'
```

**Expected output:** A JSON response containing a URL or base64-encoded image data for the generated image.

**Reference:** [BFL FLUX.2 text-to-image API](https://docs.bfl.ai/flux_2/flux2_text_to_image)

#### Use Microsoft Entra ID authentication

Replace `Bearer $AZURE_API_KEY` with `Bearer $AZURE_AUTH_TOKEN`, where `AZURE_AUTH_TOKEN` is a valid Microsoft Entra ID token scoped to `https://cognitiveservices.azure.com/.default`.

---

### Image editing with reference images (FLUX.2 models)

FLUX.2 \[pro\] and FLUX.2 \[flex\] support multi-reference image editing, which lets you pass multiple base64-encoded images alongside a text prompt. The model applies stylistic or content changes across all reference images.

- FLUX.2 \[pro\]: Up to 8 reference images
- FLUX.2 \[flex\]: Up to 10 reference images

# [Python](#tab/python)

```python
import os
import base64
import requests

endpoint = os.environ["AZURE_ENDPOINT"]
api_key = os.environ["AZURE_API_KEY"]

url = f"{endpoint}/providers/blackforestlabs/v1/flux-2-pro?api-version=preview"

# Load and encode reference images
def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

payload = {
    "model": "FLUX.2-pro",
    "prompt": "Apply a cinematic, moody lighting effect to all photos. Make them look like scenes from a sci-fi noir film",
    "output_format": "jpeg",
    "input_image": encode_image("image1.jpg"),
    "input_image_2": encode_image("image2.jpg"),
}

response = requests.post(
    url,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    },
    json=payload,
)
response.raise_for_status()

result = response.json()
print(result)
```

**Expected output:** A JSON response containing a URL or base64-encoded image reflecting the cinematic style applied to the input images.

**Reference:** [BFL FLUX.2 text-to-image API](https://docs.bfl.ai/flux_2/flux2_text_to_image)

# [REST API](#tab/rest-api)

```sh
curl -X POST https://<resource-name>.api.cognitive.microsoft.com/providers/blackforestlabs/v1/flux-2-pro?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_API_KEY" \
  -d '{
      "model": "FLUX.2-pro",
      "prompt": "Apply a cinematic, moody lighting effect to all photos. Make them look like scenes from a sci-fi noir film",
      "output_format": "jpeg",
      "input_image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDA.......",
      "input_image_2": "iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAIAAADwf........."
    }'
```

**Expected output:** A JSON response containing a URL or base64-encoded image reflecting the cinematic style applied to the input images.

**Reference:** [BFL FLUX.2 text-to-image API](https://docs.bfl.ai/flux_2/flux2_text_to_image)

---

## Use the Image API with FLUX models

`FLUX.1-Kontext-pro` and `FLUX-1.1-pro` are also available through the Image API, which uses the same endpoint format as the Azure OpenAI images API. The Image API endpoint has the following form:

```
https://<resource-name>.services.ai.azure.com/openai/deployments/<deployment-name>/images/generations?api-version=preview
```

For image editing (in-context generation), `FLUX.1-Kontext-pro` also supports:

```
https://<resource-name>.services.ai.azure.com/openai/deployments/<deployment-name>/images/edits?api-version=preview
```

### Image generation (text to image)

# [Python](#tab/python)

1. **Install the OpenAI library:**

    ```bash
    pip install openai
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
    from openai import OpenAI

    client = OpenAI(
        base_url=os.environ["AZURE_ENDPOINT"] + "/openai",
        api_key=os.environ["AZURE_API_KEY"],
        default_query={"api-version": "preview"},
    )

    result = client.images.generate(
        model=os.environ["DEPLOYMENT_NAME"],
        prompt="A photograph of a red fox in an autumn forest",
        n=1,
        size="1024x1024",
    )

    print(result.data[0].url)
    ```

    **Expected output:** A URL to the generated image.

    **Reference:** [OpenAI Python client](https://github.com/openai/openai-python), [images.generate](https://learn.microsoft.com/python/api/overview/azure/ai-openai-readme)

# [REST API](#tab/rest-api)

```bash
export AZURE_API_KEY="<your-api-key>"
export DEPLOYMENT_NAME="<your-deployment-name>"
```

```sh
curl -X POST https://<resource-name>.services.ai.azure.com/openai/deployments/$DEPLOYMENT_NAME/images/generations?api-version=preview \
  -H "Content-Type: application/json" \
  -H "api-key: $AZURE_API_KEY" \
  -d '{
      "prompt": "A photograph of a red fox in an autumn forest",
      "n": 1,
      "size": "1024x1024"
    }'
```

**Expected output:** A JSON response containing a URL to the generated image.

**Reference:** [Azure OpenAI Images API reference](../../openai/reference-preview.md)

---

### Image editing with the Image API (FLUX.1 Kontext \[pro\])

`FLUX.1-Kontext-pro` also supports the `images/edits` endpoint, which lets you pass a reference image alongside a text prompt for in-context editing.

# [Python](#tab/python)

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["AZURE_ENDPOINT"] + "/openai",
    api_key=os.environ["AZURE_API_KEY"],
    default_query={"api-version": "preview"},
)

with open("reference.jpg", "rb") as image_file:
    result = client.images.edit(
        model=os.environ["DEPLOYMENT_NAME"],
        image=image_file,
        prompt="Change the background to a sunset over the ocean",
        n=1,
        size="1024x1024",
    )

print(result.data[0].url)
```

**Expected output:** A URL to the edited image with the new background.

**Reference:** [OpenAI Python client](https://github.com/openai/openai-python), [images.edit](https://learn.microsoft.com/python/api/overview/azure/ai-openai-readme)

# [REST API](#tab/rest-api)

```sh
curl -X POST https://<resource-name>.services.ai.azure.com/openai/deployments/$DEPLOYMENT_NAME/images/edits?api-version=preview \
  -H "api-key: $AZURE_API_KEY" \
  -F "prompt=Change the background to a sunset over the ocean" \
  -F "image=@reference.jpg" \
  -F "n=1" \
  -F "size=1024x1024"
```

**Expected output:** A JSON response containing a URL to the edited image.

**Reference:** [Azure OpenAI Images API reference](../../openai/reference-preview.md)

---

## Available FLUX models

See [the Black Forest Labs model collection in the Foundry portal](https://ai.azure.com/explore/models?&selectedCollection=black+forest+labs/?cid=learnDocs) for available models.

For more details about model capabilities, see [Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md).

### FLUX.2 \[flex\]

> [!IMPORTANT]
> [Registration is required for access to FLUX.2 \[flex\]](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMzM2TDBZRko3QldSSFlWREhQSEpSSEdKVyQlQCN0PWcu).

FLUX.2 \[flex\] (`FLUX.2-flex`) offers fine-grained control with more stable throughput — throughput degrades more gracefully as image size increases. It's best suited for text-heavy layouts and images that require text overlay or fine detail preservation. It accepts text and image input (32,000 tokens and up to 10 images) and outputs one image in PNG or JPG format. Maximum output resolution is **4 MP**.

**Additional parameters (BFL provider API only):**

| Parameter | Description |
| -- | -- |
| `guidance` | Controls how closely the output follows the prompt. Range: 1.5–10, default: 4.5. Higher values increase prompt adherence. |
| `steps` | Number of inference steps. Maximum: 50, default: 50. Higher values produce more detail but are slower. |

The following example shows a FLUX.2 \[flex\]-specific request for image generation using the `guidance` and `steps` parameters:

```sh
curl -X POST https://<your-resource-name>.api.cognitive.microsoft.com/providers/blackforestlabs/v1/flux-2-flex?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {API_KEY}" \
  -d '{
      "model": "FLUX.2-flex",
      "prompt": "A photograph of a red fox in an autumn forest",
      "width": 1024,
      "height": 1024,
      "seed": 42,
      "safety_tolerance": 2,
      "output_format": "jpeg",
      "guidance": 1.5,
      "steps": 10
    }'
```

**Expected output:** A JSON response containing a URL or base64-encoded image data for the generated image.

### FLUX.2 \[pro\]

FLUX.2 \[pro\] (`FLUX.2-pro`) delivers state-of-the-art image quality at maximum speed, making it the best choice for production workloads at scale. Note that it exhibits higher response times compared to FLUX.1 Kontext \[pro\] and FLUX.2 \[flex\], and throughput decreases at higher resolutions. It accepts text and image input (32,000 tokens and up to 8 images) and outputs one image in PNG or JPG format. Maximum output resolution is **4 MP**.

The BFL provider API supports all parameters for FLUX.2 \[pro\], including `guidance`, `steps`, `seed`, `aspect_ratio`, `safety_tolerance`, and `output_format`.

### FLUX.1 Kontext \[pro\]

FLUX.1 Kontext \[pro\] (`FLUX.1-Kontext-pro`) specializes in in-context generation and editing with strong character consistency across edits. It accepts text and image input (5,000 tokens and 1 image) and outputs one image in PNG or JPG format. Maximum output resolution is **1 MP**.

FLUX.1 Kontext \[pro\] is available through both the BFL provider API and the Image API (`images/generations` and `images/edits`).

**Additional parameters (BFL provider API only):** `seed`, `aspect_ratio`, `input_image`, `prompt_unsampling`, `safety_tolerance`, `output_format`.

### FLUX1.1 \[pro\]

FLUX1.1 \[pro\] (`FLUX-1.1-pro`) delivers fast text-to-image generation with strong prompt adherence, competitive pricing, and scalable generation. It accepts text input (5,000 tokens) and outputs one image in PNG or JPG format. Maximum output resolution is **1.6 MP**.

FLUX1.1 \[pro\] is available through both the BFL provider API and the Image API (`images/generations`).

**Additional parameters (BFL provider API only):** `width`, `height`, `prompt_unsampling`, `seed`, `safety_tolerance`, `output_format`.

## API quotas and limits

FLUX models in Foundry have the following rate limits measured in Requests Per Minute (RPM). The tier available to you depends on your subscription and deployment configuration.

| Model | Tier | Requests Per Minute (RPM) |
| -- | -- | -- |
| FLUX.2 \[pro\] | Low | 15 |
| FLUX.2 \[pro\] | Medium | 30 |
| FLUX.2 \[pro\] | High | 100 |
| FLUX.2 \[flex\] | Low | 5 |
| FLUX.2 \[flex\] | Medium | 10 |
| FLUX.2 \[flex\] | High | 25 |
| FLUX.1 Kontext \[pro\] | Default | 6 |
| FLUX1.1 \[pro\] | Default | 6 |

To request a quota increase, submit the [quota increase request form](https://aka.ms/oai/stuquotarequest). Requests are processed in the order they're received, and priority goes to customers who actively use their existing quota allocation.

## Responsible AI considerations

When using FLUX models in Foundry, consider these responsible AI practices:

- Configure AI content safety during model inference, because Foundry doesn't provide built-in content filtering for FLUX models at deployment time.
- Ensure your use of generated images complies with [Black Forest Labs' terms of service](https://blackforestlabs.ai/terms-of-service/) and applicable copyright and intellectual property laws.
- Be transparent about AI-generated content when sharing or publishing images.
- Avoid generating content that could be harmful, misleading, or in violation of privacy.

## Code samples and notebooks

See the [GitHub sample for image generation with FLUX models in Microsoft Foundry](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/black-forest-labs/flux/README.md) and its associated [Jupyter notebook](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/black-forest-labs/flux/AIFoundry_ImageGeneration_FLUX.ipynb) for end-to-end examples of creating high-quality images from text prompts.

## Related content

- [Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md)
- [Configure Microsoft Entra ID authentication](configure-entra-id.md)
- [Explore available models in Foundry](../concepts/models-sold-directly-by-azure.md)
- [BFL API documentation](https://docs.bfl.ai)
