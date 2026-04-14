---
title: Include file
description: Include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/13/2026
ms.custom: include
---

## Input limitations

This section describes the limitations of vision-enabled chat models.

### Image support

- **Maximum input image size**: The maximum size for input images is restricted to 20 MB.
- **Low resolution accuracy**: When images are analyzed using the "low resolution" setting, it allows for faster responses and uses fewer input tokens for certain use cases. However, this could impact the accuracy of object and text recognition within the image.
- **Image chat restriction**: When you upload images in [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs) or the API, you're limited to 10 images per chat call.

## Special pricing information


> [!IMPORTANT]
> The following content is an example only, and prices are subject to change in the future.

Vision-enabled models accrue charges like other Azure OpenAI chat models. You pay a per-token rate for the prompts and completions, detailed on the [Pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). The base charges and other features are outlined here:

Base Pricing for GPT-4 Turbo with Vision is:
- Input: $0.01 per 1,000 tokens
- Output: $0.03 per 1,000 tokens

See the [Tokens section of the overview](/azure/ai-foundry/openai/overview#tokens) for information on how text and images translate to tokens.

### Example image price calculation



For a typical use case, take an image with both visible objects and text and a 100-token prompt input. When the service processes the prompt, it generates 100 tokens of output. In the image, both text and objects can be detected. The price of this transaction would be:

| Item        | Detail        |  Cost   |
|-----------------|-----------------|--------------|
| Text prompt input | 100 text tokens | $0.001 |
| Example image input (see [Image tokens](/azure/ai-foundry/openai/overview#image-tokens-gpt-4-turbo-with-vision)) | 170 + 85 image tokens | $0.00255 |
| Enhanced add-on features for OCR | $1.50 / 1,000 transactions | $0.0015 |
| Enhanced add-on features for Object Grounding | $1.50 / 1,000 transactions | $0.0015 | 
| Output Tokens      | 100 tokens (assumed)    | $0.003       |
| **Total** |  |**$0.00955** |
