---
title: Fine-tune CxrReportGen Premium in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn the CxrReportGen Premium specifics for fine-tuning, including training data, image preparation, evaluation, and deployment quota.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: how-to
ms.date: 08/12/2026
ms.reviewer: jmerkow
reviewer: jmerkow
ms.author: ssalgado
author: ssalgadodev
ms.custom: dev-focus
ai-usage: ai-assisted
#customer intent: As a data scientist, I want the CxrReportGen Premium fine-tuning specifics so that I can prepare data and configure a job correctly.

---

# Fine-tune CxrReportGen Premium (preview)

[!INCLUDE [health-ai-models-meddev-disclaimer-preview](includes/health-ai-models-meddev-disclaimer-preview.md)]

This article covers the CxrReportGen Premium (preview) values you need for fine-tuning: the
training data format, image preparation, and evaluation metrics. For the shared
workflow — prerequisites, uploading files, creating and monitoring a job, and deploying the result —
see [Customize a premium healthcare AI model with fine-tuning](fine-tune-premium-healthcare-models.md).

## What this model learns

Fine-tuning makes it easy to adapt the phrasing and structure of the generated **Findings** and
**Impression** sections to your institution's reporting conventions. Use model ID
`CXRReportgen-Premium` when you create the fine-tuning job.

## Training data format

For shared JSONL, file, and upload information, see
[Prepare your data](fine-tune-premium-healthcare-models.md#prepare-your-data). This article defines the
model-specific CxrReportGen Premium record.

Training data uses JSON Lines (JSONL). Each line is one complete JSON object with its own top-level
`messages` array. The following formatted JSON shows the structure of one record. In the actual
`.jsonl` file, write the complete object on one physical line.

```json
{
  "messages": [
    {"role": "user", "content": [
      {"type": "image_url", "image_url": {"url": "<DATA_URI>"}},
      {"type": "text", "text": "<INPUT_TEXT>"}
    ]},
    {"role": "assistant", "content": "<GROUND_TRUTH_REPORT>"}
  ]
}
```
### User message: input

The required `user` message is the input to the model. Its `content` value is an ordered array.

```json
{
  "role": "user",
  "content": [
    {"type": "image_url", "image_url": {"url": "data:image/png;base64,<BASE64>"}},
    {"type": "text", "text": "Generate a report for this chest X-ray."}
  ]
}
```

| Input | Required | What to include |
|---|---|---|
| Current frontal image | Yes | Exactly one `image_url` part that contains a PNG or JPEG data URI: `data:image/png;base64,...` or `data:image/jpeg;base64,...`. |
| Report-generation instruction | Yes | Include the instruction in exactly one `text` part. |
| `Indication:` | No | Include optional current-study context in the `text` part. |
| `Technique:` | No | Include optional current-study context in the `text` part. |
| `Comparison:` | No | Include optional current-study context in the `text` part. |

The context labels are content inside the single `text` part, not top-level JSON fields. Put the
current image first and the single text part last.

### Assistant message: label

The required `assistant` message is the supervised label, or target. It isn't model input.

```json
{
   "role": "assistant",
   "content": "Findings: ... Impression: ..."
}
```

The `content` value is the complete ground-truth report for the current study. Use the desired
`Findings:` and `Impression:` style and structure.

### Complete JSONL example

The following example shows one complete record on one physical line. It uses one current
frontal image.

For a complete sample, see the CxrReportGen Premium fine-tuning sample in the
[Healthcare AI examples](https://aka.ms/HealthcareAIExamples) repository.

```jsonl
{"messages":[{"role":"user","content":[{"type":"image_url","image_url":{"url":"data:image/png;base64,<BASE64>"}},{"type":"text","text":"Generate a report for this chest X-ray."}]},{"role":"assistant","content":"Findings: ... Impression: ..."}]}
```

## Dataset requirements

For shared service and file requirements, including JSONL format, UTF-8 encoding, and upload
limits, see
[Prepare your data](fine-tune-premium-healthcare-models.md#prepare-your-data) in the fine-tuning
workflow hub.

Your training file needs at least 10 records. Job creation rejects files with
fewer records.

## Image preprocessing and requirements

### Image requirements

Training images must meet these requirements:

| Requirement | Value |
|---|---|
| File format | PNG or JPEG. |
| Color mode | RGB, three channels. |
| Maximum dimensions | 4096 x 4096 pixels. |

### Recommended DICOM preprocessing

To prepare a DICOM chest X-ray for fine-tuning:

1. Decode the DICOM pixel data.
1. Apply the applicable DICOM transforms, such as a lookup table (LUT) or the
   rescale slope and intercept values.
1. Normalize the intensities and scale the result to 8-bit. The recommended
   starting point is the 5th–95th percentile range; min/max normalization is
   also supported.
1. Convert the image to RGB. The recommended image size is 518 x 518 pixels.
1. Save the image as PNG or JPEG, and then base64-encode it for the training
   record. For JPEG, the recommended quality is 95.


```python
import base64
from io import BytesIO

import numpy as np
import pydicom
from PIL import Image

# Read the DICOM pixel data.
dicom = pydicom.dcmread("image.dcm")
image = dicom.pixel_array.astype(np.float32)

# Apply Rescale Slope and Rescale Intercept.
image = image * dicom.RescaleSlope + dicom.RescaleIntercept

# Normalize the 5th-95th percentile range to 8-bit.
low, high = np.percentile(image, (5, 95))
image = (
  (np.clip(image, low, high) - low) / (high - low) * 255
).astype(np.uint8)

# Convert the grayscale image to three-channel RGB.
image = Image.fromarray(image).convert("RGB")

# Resize the image to 518 x 518 pixels.
image = image.resize((518, 518))

# Encode PNG bytes as a data URI for image_url.url.
buffer = BytesIO()
image.save(buffer, format="PNG")
image_data_uri = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
```

## Hyperparameters

Use the shared hyperparameter request shape described in
[Create the fine-tuning job](fine-tune-premium-healthcare-models.md#create-the-fine-tuning-job)
on the hub. When you omit all hyperparameters, the service applies these default values for
CxrReportGen Premium:

| Hyperparameter | Default |
|---|---|
| `n_epochs` | `1` |
| `batch_size` | `8` |
| `learning_rate_multiplier` | `1.0` |

The managed fine-tuning request exposes `learning_rate_multiplier`. The service-applied value of
`1.0` sets a maximum learning rate of `1e-4`. The learning-rate scheduler warms up linearly during
the first 10% of training steps, then follows cosine decay.

## Deploy the fine-tuned model

Fine-tuned CxrReportGen Premium deployments draw on a separate quota,
`AIServices.GlobalStandard.CXRReportgen-Premium-finetune`, distinct from the base model's inference
quota. For deployment names, model identifiers, and capacity, see
[Deploy the fine-tuned model](fine-tune-premium-healthcare-models.md#deploy-the-fine-tuned-model) in
the fine-tuning workflow hub.

## Interpret training metrics

Reported loss is mean next-token cross-entropy over ground-truth assistant-report tokens. System
and user prompts, image-placeholder tokens, and padding don't contribute to the loss.
The Foundry portal reports two loss metrics:

- `train_loss` is the interval average of training losses reported since the previous metrics row.
- `eval_loss` is the validation loss aggregated over the complete validation file at each
  evaluation. It doesn't represent one batch or step.

> [!NOTE]
> Downloaded result CSVs include a third field, `avg_train_loss`. For CXR, `train_loss` contains
> periodic values, and `avg_train_loss` contains the final average of optimizer-step loss aggregates
> over the run.

## Evaluate the fine-tuned model

[!INCLUDE [Fine-tuning evaluation caveat](includes/fine-tuning-evaluation-caveat.md)]

Typical metrics for comparing a generated report with its reference report include:

| Metric | What it measures | Reference |
|---|---|---|
| BLEU-2 | Bigram overlap between generated and reference text. | [BLEU](https://aclanthology.org/P02-1040/) |
| BERTScore | Contextual token similarity between generated and reference text. | [BERTScore](https://arxiv.org/abs/1904.09675) |
| SEMB | Cosine similarity between CheXbert report embeddings. | [CheXbert](https://arxiv.org/abs/2004.09167) |
| RadGraph F1 | F1 overlap of clinical entities and relations extracted from both reports. | [RadGraph](https://arxiv.org/abs/2106.14463) |
| RadCliQ | Composite estimate of the number of errors a radiologist would assign. | [Evaluating Progress in Automatic Chest X-Ray Radiology Report Generation](https://www.medrxiv.org/content/10.1101/2022.08.30.22279318v1) |

## Related content

- [Customize a premium healthcare AI model with fine-tuning](fine-tune-premium-healthcare-models.md)
- [Fine-tune MedImageInsight Premium](fine-tune-medimageinsight-premium.md)
- [Deploy and use CxrReportGen Premium](deploy-cxrreportgen-premium.md)
- [Healthcare AI examples (GitHub)](https://aka.ms/HealthcareAIExamples)
