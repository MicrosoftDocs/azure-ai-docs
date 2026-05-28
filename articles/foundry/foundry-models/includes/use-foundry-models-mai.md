---
title: Include file
description: Include file
ms.author: mopeakande
author: msakande
ms.reviewer: rasavage
reviewer: RSavage2
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 05/27/2026
ai-usage: ai-assisted
ms.custom: classic-and-new
---

MAI Image models are a family of image models developed by Microsoft AI that deliver state-of-the-art text-to-image generation and for some models, image-to-image edits. These models are offered as part of Microsoft Foundry Models sold by Azure, providing secure, enterprise-grade access through Microsoft Foundry.

In this article, you learn how to:

- Deploy MAI image models in Microsoft Foundry
- Authenticate by using Microsoft Entra ID or API keys
- Generate images by using the MAI image generation API
- Run an image edit

MAI image models in Microsoft Foundry include:

| Model name | Model version | Key Capabilities |
| --- | --- | --- |
| `MAI-Image-2.5-Flash` (Preview) | | Text-to-image generation, Image-to-image edits |
| `MAI-Image-2.5` (Preview) | `2026-06-02` | Text-to-image generation, Image-to-image edits |
| `MAI-Image-2e` (Preview) | `2026-04-09`| Text-to-image generation |
| `MAI-Image-2` (Preview) | `2026-02-20` | Text-to-image generation |

To learn more about the individual models, see [Available MAI image models](#available-mai-image-models).

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../how-to/create-projects.md). MAI image models are available for **global standard deployment** (West Central US, East US, West US, West Europe, Sweden Central, South India, and UAE North).
- **Cognitive Services Contributor** role on the Azure AI Foundry resource to deploy models. For more information, see [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).

## Deploy MAI image models

To deploy an MAI image model, follow the instructions in [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md).

Alternatively, you can deploy the model by using the Azure CLI. The following code shows deployment of `MAI-Image-2.5` To deploy a different model, replace the model name and version in the lines `--model-name MAI-Image-2.5` and `--model-version 2026-06-02` with the values for your desired model.

Replace `<ACCOUNT_NAME>`, `<RESOURCE_GROUP>`, `<DEPLOYMENT_NAME>` with your values.

```bash
az cognitiveservices account deployment create \
  --name <ACCOUNT_NAME> \
  --resource-group <RESOURCE_GROUP> \
  --deployment-name <DEPLOYMENT_NAME> \
  --model-name "MAI-Image-2.5" \
  --model-format Microsoft \
  --model-version 2026-06-02 \
  --sku-name GlobalStandard \
  --sku-capacity 1
```

**Reference:** [az cognitiveservices account deployment create](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-create)

To list all available models and versions on your resource:

```bash
az cognitiveservices account list-models \ 
  --resource-group <RESOURCE_GROUP> \ 
  --name <ACCOUNT_NAME> \ 
  -o table 
```

**Reference:** [az cognitiveservices account deployment list](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-list)

After deployment, use the [Foundry playground](../../concepts/concept-playgrounds.md) to interactively test the model.

## Run text-to-image generation

The following examples show how to generate an image from a text prompt using MAI image models with the [MAI image generations API](#api-endpoints).

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
    import base64
    import requests
    
    endpoint = os.environ["AZURE_ENDPOINT"]
    api_key = os.environ["AZURE_API_KEY"]
    deployment_name = os.environ["DEPLOYMENT_NAME"]
    
    width = 1024
    height = 1024
    
    url = f"{endpoint}/mai/v1/images/generations"
    
    payload = {
        "model": deployment_name,
        "prompt": "A photorealistic concept art poster of a university at sunset, cinematic lighting",
        "width": width,
        "height": height
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
    
    image_data = [
        output
        for output in result.get("data", [])
        if "b64_json" in output
    ]
    
    if image_data:
        image_base64 = image_data[0]["b64_json"]
        output_path = "output.png"
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_base64))
        print(f"Image saved to {output_path}")
    else:
        print("Unexpected response format:", result)
    ```

    **Expected output:** A JSON response containing the generated image data in base64 format. The image is decoded and saved as `output.png` in the current directory.

#### Use Microsoft Entra ID authentication

To use Microsoft Entra ID instead of an API key, replace the `api-key` header with a bearer token obtained using the `DefaultAzureCredential`:

1. **Install the Azure Identity library:**

    ```bash
    pip install azure-identity
    ```

1. **Update the request headers in the API key authentication code:**

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
      "prompt": "A photorealistic concept art poster of a university at sunset, cinematic lighting",
      "width": 1024,
      "height": 1024
    }' \
  | jq -r '.data[0].b64_json' \
  | base64 --decode > output.png
```

**Expected output:** A JSON response containing the generated image data in base64 format. The image is decoded and saved as `output.png` in the current directory.

#### Use Microsoft Entra ID authentication

Replace the `api-key` header with an `Authorization` header:

```sh
-H "Authorization: Bearer $AZURE_AUTH_TOKEN"
```

Where `AZURE_AUTH_TOKEN` is a valid Microsoft Entra ID token scoped to `https://cognitiveservices.azure.com/.default`.

---

## Run an image-to-image edit

The following examples show how to perform an image-to-image edit using an MAI image model with the [MAI image edits API](#api-endpoints). 

> [!NOTE]
> Thee `MAI-Image-2.5-Flash` (Preview) and `MAI-Image-2.5` (Preview) models support image-to-image edits.

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
    import base64
    import requests
    
    endpoint = os.environ["AZURE_ENDPOINT"]
    api_key = os.environ["AZURE_API_KEY"]
    deployment_name = os.environ["DEPLOYMENT_NAME"]
    
    width = 1024
    height = 1024
    
    url = f"{endpoint}/mai/v1/images/edits"
    
    payload = {
        "model": deployment_name,
        "prompt": "A photorealistic concept art poster of a university at sunset, cinematic lighting",
        "width": width,
        "height": height
        "input": <PATH_TO_IMAGE.png>
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
    
    image_data = [
        output
        for output in result.get("data", [])
        if "b64_json" in output
    ]
    
    if image_data:
        image_base64 = image_data[0]["b64_json"]
        output_path = "output.png"
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_base64))
        print(f"Image saved to {output_path}")
    else:
        print("Unexpected response format:", result)
    ```

    **Expected output:** A JSON response containing the edited image data in base64 format. The image is decoded and saved as `output.png` in the current directory.


To use Microsoft Entra ID instead of an API key, modify this code as described in the earlier section: [Use Microsoft Entra ID authentication](#use-microsoft-entra-id-authentication).


# [REST API](#tab/rest-api)

#### Use API key authentication

Export yourAPI key, then run the following cURL command:

```bash
export AZURE_API_KEY="<your-api-key>"
```

```sh
# Save API response to file
curl -s "https://<resource-name>.services.ai.azure.com/mai/v1/images/edits" \
  -H "api-key: $AZURE_API_KEY" \
  -F "prompt=Turn this image into a clean futuristic product shot with studio lighting" \
  -F "model=<your-deployment-name>" \
  -F "image=@/path/to/your/image.png" \
  -o /tmp/response.json

# Decode and save the output image
jq -r '.data[0].b64_json' /tmp/response.json | base64 -d > /path/to/output.png
```


**Expected output:** A JSON response containing the generated image data in base64 format. The image is decoded and saved as `output.png` in the current directory.

To use Microsoft Entra ID authentication instead of an API key, modify this code as described in the earlier section: [Use Microsoft Entra ID authentication](#use-microsoft-entra-id-authentication-1)

---


## Available MAI image models

Foundry supports use of MAI-Image-2.5-Flash (Preview), MAI-Image-2.5 (Preview), MAI-Image-2 (Preview), and MAI-Image-2e (Preview). Each of these models are suitable for the following key use-cases:

- **Text-to-image generation:** Generate high-quality images from natural language prompts, enabling users to translate textual descriptions into visually coherent outputs suitable for a wide range of creative and design use cases.
- **Photorealistic image synthesis:** Capable of generating realistic imagery with consistent visual structure, making it suitable for concept visualization and content creation scenarios.
- **Product, branding and commercial design:** Well suited for product imagery, marketing visuals, brand assets, and commercial creative workflows.

MAI-Image-2.5-Flash (Preview) and MAI-Image-2.5 (Preview) further excel in these key use cases:

- **Image-to-image editing:** Support precise, controllable edits to existing images, including object removal, replacement, attribute changes, inpainting, text updates, and artifact cleanup while preserving composition and layout.
- **High-fidelity portraits:** Generate expressive, natural-looking portraits with accurate facial structure, lighting, and texture.
- **Accurate text rendering:** Improved rendering of text within generated images, including labels, posters, packaging, and signage.
- **Visual reasoning:** Reason across objects, scene structure, lighting, scale, and spatial positioning to produce consistent outputs, even from ambiguous prompts.

For more details about the model capabilities, see capabilities of Microsoft models in [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md#microsot-models-sold-by-azure).

### MAI-Image-2.5-Flash (Preview) 

MAI-Image-2.5-Flash (Preview) is a text-to-image generation and image-to-image editing model designed to create high-quality, visually rich images from natural language prompts and to perform precise, controllable edits on existing images. It uses a diffusion-based generative approach to progressively refine images, enabling strong alignment between the input text and the generated output. The model is optimized to produce diverse and coherent images across a wide range of creative and design scenarios, making it well suited for tasks such as concept visualization, creative content generation, image editing workflows, and production design.

### MAI-Image-2.5 (Preview) 

MAI-Image-2.5 (Preview) is a text-to-image generation and image-to-image editing model designed to create high-quality, visually rich images from natural language prompts and to perform precise, controllable edits on existing images. It uses a diffusion-based generative approach to progressively refine images, enabling strong alignment between the input text and the generated output. The model excels at precise, surgical edits with consistency — enabling users and developers to make targeted object edits, adapt layouts, update text, clean up artifacts like motion blur, and preserve visual consistency across iterations.

### MAI-Image-2e (Preview)

MAI-Image-2e (Preview) delivers high-quality image generation – just like MAI-Image-2 — but up to 22% faster and four times more efficient than MAI-Image-2, making it the smartest choice for developers building at scale. MAI-Image-2e is best suited for high-volume, fast-turnaround scenarios — for example, product imagery at scale, marketing variations, branded assets, or any workflow where efficiency and cost per image are key.

### MAI-Image-2 (Preview)

MAI-Image-2 (Preview) is a text-to-image generation model designed to create high-quality, visually rich images from natural language prompts. It uses a diffusion-based generative approach to progressively refine images, enabling strong alignment between the input text and the generated output. The model is optimized to produce diverse and coherent images across a wide range of creative and design scenarios, making it well suited for tasks such as concept visualization, creative content generation, and image design workflows.


## API endpoints

After you deploy an MAI image model, use the **MAI image generations API** to generate images and the **MAI image edits API** for image-to-image edits. 

- **Image generations API endpoint**: A Microsoft-managed endpoint that accepts a text prompt and returns a PNG image. The API endpoint has the following form:

    ```
    https://<resource-name>.services.ai.azure.com/mai/v1/images/generations
    ```

- **Image edits API endpoint**: A Microsoft-managed endpoint that accepts a JPEG or PNG image and returns a PNG image. The API endpoint has the following form:

    ```
    https://<resource-name>.services.ai.azure.com/mai/v1/images/edits
    ```

To authenticate, you need your **resource endpoint** and either a **Microsoft Entra ID token** or an **API key**. You can find these values in the **Keys and Endpoint** section of your resource in the Azure portal, or on the deployment details page in the [Foundry portal](https://ai.azure.com).

#### Model capabilities

The following table lists the request parameters for the image APIs:

| Parameter | API | Type | Description |
| --------- | ---- | ---- | ----------- |
| `model` | Both | string | The deployment name you assigned when you deployed the model. |
| `prompt` | Both | string | The text prompt that describes the image to generate or edits to make. <br>Maximum context length: 32,000 tokens. |
| `image` | Image edits | string | The path to the image you want to edit. The image is passed as Multipart Form Data. Must be in JPEG or PNG format. |
| `width` | Image generations | integer | Width of the output image in pixels. <br>Minimum: 768. The product of `width` × `height` must not exceed 1,048,576. |
| `height` | Image generations | integer | Height of the output image in pixels. <br>Minimum: 768. The product of `width` × `height` must not exceed 1,048,576. |

> [!NOTE]
> The output format is always PNG. The maximum total pixel count is 1,048,576 (equivalent to 1024×1024). Both `width` and `height` must be at least 768 pixels each. Either dimension can exceed 1024 as long as the total pixel count stays within the limit.

## API quotas and limits

MAI image models have the following rate limits measured in Requests Per Minute (RPM). The tier available to you depends on your subscription and deployment configuration.

| Deployment Type | Tier | MAI-Image-2.5-Flash RPM | MAI-Image-2.5 RPM | MAI-Image-2e RPM | MAI-Image-2 RPM |
| -- | -- | -- | -- | -- | -- |
| Global Standard | 1 |  |  | 18 | 9 |
| Global Standard | 2 |  |  | 30 | 15 |
| Global Standard | 3 |  |  | 60 | 30 |
| Global Standard | 4 |  |  | 90 | 45 |
| Global Standard | 5 |  |  | 120 | 60 |
| Global Standard | 6 |  |  | 180 | 90 |

To request a quota increase, submit the [quota increase request form](https://aka.ms/oai/stuquotarequest). Requests are processed in the order they're received, and priority goes to customers who actively use their existing quota allocation.

## Troubleshoot

Use the following table to resolve common errors when working with MAI image generation models:

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Invalid API key or expired token | Regenerate the key in the Azure portal. For Entra ID authentication, ensure the token scope is `https://cognitiveservices.azure.com/.default`. |
| `404 Not Found` | Incorrect deployment name or endpoint URL | Verify the deployment name and endpoint in the Foundry portal under **Deployments**. |
| `400 Bad Request` | `width` or `height` below minimum, or total pixel count exceeds maximum | Ensure `width` and `height` are each at least 768, and that `width` × `height` ≤ 1,048,576. |
| `429 Too Many Requests` | Rate limit exceeded | Wait and retry, or [request a quota increase](https://aka.ms/oai/stuquotarequest). |

## Responsible AI considerations

When using MAI image generation models in Foundry, consider these responsible AI practices:

- **Be aware of known limitations**: Despite technical mitigations such as data filtering and content classifiers applied at the system level, image generation models can produce harmful or unexpected content based on user requests. Common risk areas include violent or gory content, sexual content or nudity, depictions of public figures, and replication of trademarked or other protected material.
- **Configure content safety**: Apply additional mitigations appropriate to your use case, because no generative model is immune to adversarial prompts.
- **Comply with applicable terms**: Ensure your use of generated images complies with [Microsoft's terms of service](https://www.microsoft.com/en-us/legal/terms-of-use) and applicable copyright and intellectual property laws.
- **Be transparent**: Disclose that content is AI-generated when sharing or publishing images.
- **Avoid harmful content**: Don't generate content that could be harmful, misleading, or in violation of privacy.

## Related content

- [Explore available models in Foundry](../concepts/models-sold-directly-by-azure.md)
- [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md)
- [Configure Microsoft Entra ID authentication](../how-to/configure-entra-id.md)
