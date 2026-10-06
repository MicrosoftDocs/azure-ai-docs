---
title: Fine-tune MedImageInsight Premium in Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn the MedImageInsight Premium specifics for fine-tuning — training data format, image requirements, hyperparameters, and evaluation.
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
#customer intent: As a data scientist, I want the MedImageInsight Premium fine-tuning specifics so that I can prepare data and configure a job correctly.

---

# Fine-tune MedImageInsight Premium (preview)

[!INCLUDE [health-ai-models-meddev-disclaimer-preview](includes/health-ai-models-meddev-disclaimer-preview.md)]

Fine-tuning MedImageInsight Premium follows the shared premium healthcare model
workflow: prepare data, upload a training file, create a job, monitor it, and
deploy the result. For that end-to-end workflow, prerequisites, quota, and job
creation and monitoring steps, see
[Customize a premium healthcare AI model with fine-tuning](fine-tune-premium-healthcare-models.md).
This article covers only the values specific to MedImageInsight Premium.

## What this model learns

Fine-tuning adapts MedImageInsight Premium's image and text embeddings so that
images and their assigned labels sit closer together in the shared embedding
space for your label taxonomy. The model's output remains an embedding
vector, not a classification label or a generated report. To get
classification-style results, add a downstream step that compares the
fine-tuned embeddings against your label-text embeddings, for example with
cosine similarity.

In the job body, set `model` to `MedImageInsight-Premium`.

## Training data format

For shared JSONL, file, and upload information, see
[Prepare your data](fine-tune-premium-healthcare-models.md#prepare-your-data).
This article defines the model-specific MedImageInsight Premium record.

MedImageInsight Premium training data uses JSON Lines (JSONL). Each physical line is one complete
JSON object with its own top-level `messages` array in `user` then `assistant` order. This
classification shape doesn't include a `system` message.

The formatted JSON in the following section shows the structure of one record. In the actual `.jsonl` file, write the
complete object on one physical line.

```json
{
  "messages": [
    {"role": "user", "content": [
      {"type": "image_url", "image_url": {"url": "<DATA_URI>"}}
    ]},
    {"role": "assistant", "content": "<JSON_ENCODED_TEXT_INPUT>"}
  ]
}
```

### User message: image input

The required `user` message is the model input. Its `content` value is an array that contains
exactly one image part.

```json
{
  "role": "user",
  "content": [
    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,<BASE64>"}}
  ]
}
```


### Assistant message: text input

The required `assistant` message supplies the text paired with the image during contrastive
embedding fine-tuning. For this documented classification shape, its `content` value is a
JSON-encoded string, not a nested JSON object.

The decoded string uses the following classification fields.

| Field | Required | Meaning |
|---|---|---|
| `class_id` | Yes | A positive integer that groups records in the same class. |
| `class_name` | Yes | The text paired with the image for training. |
| `source` | No | Optional metadata that identifies the dataset or source. |
| `task` | No | Optional metadata whose value is `classification` for this shape. |

Use `class_id` only to group classification records by class. Assign the same positive ID to every
record in a class and a different positive ID to each distinct class. Treat a combination of
findings as a separate composite class with its own ID. This format isn't multilabel training.
Use `caption` or `captions`, not `class_id: 0`, for ungrouped image-text pairs.

The decoded inner object looks like this:

```json
{
  "class_id": 1,
  "class_name": "x-ray chest anteroposterior Pleural Effusion.",
  "source": "NIH-CXR",
  "task": "classification"
}
```

Serialize the inner object as the `content` string. The complete assistant message looks like this:

```json
{
  "role": "assistant",
  "content": "{\"class_id\": 1, \"class_name\": \"x-ray chest anteroposterior Pleural Effusion.\", \"source\": \"NIH-CXR\", \"task\": \"classification\"}"
}
```

| Convention | Example | When to use |
|---|---|---|
| Concise class name | `Effusion` | Use when inference or evaluation candidate text uses concise class names. |
| Structured medical text | `x-ray chest anteroposterior Pleural Effusion.` | Use when candidate text includes modality, anatomy, exam parameters, and condition/pathology. |

The general structured pattern is `<image modality> <anatomy> <exam parameters>
<condition/pathology>.` Choose one convention and use it consistently across training records and
evaluation or inference text inputs.

### Caption records

A caption record uses either `caption` with one string or `captions` with a nonempty list of
alternative descriptions. Each record should use one target form. Don't put classification and
caption fields in the same record.

You can mix classification records, singular `caption` records, one-item `captions` records, and
multi-item `captions` records in the same training and validation files. Values in `captions` are
alternative descriptions of the same image, not simultaneous labels. One value is selected each
time the record is used, including validation.

These JSONL examples each occupy one physical line:

```jsonl
{"messages":[{"role":"user","content":[{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,<BASE64>"}}]},{"role":"assistant","content":"{\"caption\": \"A chest X-ray showing a right pleural effusion.\"}"}]}
{"messages":[{"role":"user","content":[{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,<BASE64>"}}]},{"role":"assistant","content":"{\"captions\": [\"A chest X-ray showing a right pleural effusion.\", \"Right pleural fluid with adjacent basilar atelectatic change.\"]}"}]}
```

### Complete JSONL examples

The following two records each occupy one physical line. They represent the example classes
`Not_Effusion` and `Effusion`, respectively.

```jsonl
{"messages":[{"role":"user","content":[{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,<BASE64>"}}]},{"role":"assistant","content":"{\"class_id\": 1, \"class_name\": \"Not_Effusion\", \"source\": \"NIH-CXR\", \"task\": \"classification\"}"}]}
{"messages":[{"role":"user","content":[{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,<BASE64>"}}]},{"role":"assistant","content":"{\"class_id\": 2, \"class_name\": \"Effusion\", \"source\": \"NIH-CXR\", \"task\": \"classification\"}"}]}
```

For complete, runnable training files, see the
[Healthcare AI examples (GitHub)](https://aka.ms/HealthcareAIExamples).

## Dataset requirements

Your training file needs at least 10 records. A file with fewer records
uploads and preprocesses without error, but job creation rejects it.

```
Training files has too few examples. At least 10 examples are required.
```

For shared file requirements, such as encoding and file size, see
[Prepare your data](fine-tune-premium-healthcare-models.md#prepare-your-data)
on the hub.

## Image preprocessing and requirements

### Image requirements

Training images must meet these requirements:

| Requirement | Value |
|---|---|
| File format | PNG or JPEG. |
| Color mode | RGB, three channels. |

### Recommended DICOM preprocessing

To prepare a DICOM image for fine-tuning:

1. Decode the DICOM pixel data.
1. Apply the applicable DICOM transforms, such as a lookup table (LUT) or the
  rescale slope and intercept values.
1. Normalize the intensities to the 1st–99th or 5th–95th percentile range, and
  scale the result to 8-bit.
1. Convert the image to RGB and resize it to 480 x 480 pixels.
1. Save the image as PNG or JPEG, and then base64-encode it for the training record.


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

# Resize the image to 480 x 480 pixels.
image = image.resize((480, 480))

# Encode PNG bytes as a data URI for image_url.url.
buffer = BytesIO()
image.save(buffer, format="PNG")
image_data_uri = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
```

> [!NOTE]
> The training code downsizes images to 480 x 480 pixels. Larger images can pass file validation,
> but they don't provide extra training resolution. You can evaluate other DICOM preprocessing
> methods, including different modality-specific windows or normalization ranges. MedImageInsight
> Premium can learn from consistently processed images, and results can vary with the selected
> method.

## Hyperparameters

Use the shared hyperparameter request shape described in
[Create the fine-tuning job](fine-tune-premium-healthcare-models.md#create-the-fine-tuning-job)
on the hub. When you omit all hyperparameters, the service applies these default values for
MedImageInsight Premium:

| Hyperparameter | Default |
|---|---|
| `n_epochs` | `3` |
| `batch_size` | `256` |
| `learning_rate_multiplier` | `0.2` |

For MedImageInsight Premium, `batch_size` accepts values from 1 through 256. The managed fine-tuning
request exposes `learning_rate_multiplier`. The service-applied value of `0.2` sets the current
trainer learning rate to `2e-5`.

## Deploy the fine-tuned model

MedImageInsight Premium fine-tuned deployments use the
`AIServices.GlobalStandard.MedImageInsight-Premium-finetune` quota. For
deployment instructions, see
[Deploy the fine-tuned model](fine-tune-premium-healthcare-models.md#deploy-the-fine-tuned-model)
on the hub.

## Interpret training metrics

Fine-tuning uses the [UniCL](https://openaccess.thecvf.com/content/CVPR2022/html/Yang_Unified_Contrastive_Learning_in_Image-Text-Label_Space_CVPR_2022_paper.html)
symmetric image-to-text and text-to-image contrastive objective.
The Foundry portal reports two loss metrics:

- `train_loss` is the UniCL loss for the current effective update.
- `eval_loss` is the sample-weighted aggregate over the complete validation file at each evaluation.

The current trainer evaluates before training and every 100 optimizer steps. If a run ends before
step 100, it has no post-training `eval_loss`, and the reported final value is the pre-training
baseline.

> [!NOTE]
> Downloaded result CSVs include a third field, `avg_train_loss`. For MI2, it can duplicate periodic
> `train_loss` and isn't a reliable full-run average. Use `train_loss` for the training-loss curve.

## Evaluate the fine-tuned model

[!INCLUDE [Fine-tuning evaluation caveat](includes/fine-tuning-evaluation-caveat.md)]

You can evaluate MedImageInsight Premium at two levels:

1. **Direct image-text alignment.** This level measures how highly the correct
  candidate text ranks by cosine similarity for each image. Metrics can include
  top-k accuracy or recall, mean reciprocal rank, per-class AUC, and macro-F1,
  depending on the label structure.
1. **Downstream workflow.** This level measures the task that consumes the
  embeddings. Examples include image retrieval, zero-shot classification,
  classification with a trained adapter, outlier detection, and multimodal
  prediction.

A base-versus-fine-tuned comparison uses the same evaluation data, candidate
text, preprocessing, and downstream method for both deployments. This approach
isolates the embedding change from differences in the evaluation setup.

The [MedImageInsight paper](https://arxiv.org/abs/2410.06542) reports
classification, image-image search, and fine-tuning evaluations across medical
imaging domains. For runnable patterns, see these Healthcare AI Examples:

- [Zero-shot classification](https://github.com/microsoft/healthcareai-examples/blob/main/azureml/medimageinsight/zero-shot-classification.ipynb)
- [Adapter training](https://github.com/microsoft/healthcareai-examples/blob/main/azureml/medimageinsight/adapter-training.ipynb)
- [Image search](https://github.com/microsoft/healthcareai-examples/blob/main/azureml/advanced_demos/image_search/2d_image_search.ipynb)
- [Outlier detection](https://github.com/microsoft/healthcareai-examples/blob/main/azureml/medimageinsight/outlier-detection-demo.ipynb)

## Model-specific errors

| Condition | Message | Fix |
|---|---|---|
| `batch_size` outside the accepted range | `batchSize must be in [1, 256].` | Set `batch_size` to a value from 1 through 256. |
| Fewer than 10 training records | `Training files has too few examples. At least 10 examples are required.` | Add records so the file has at least 10. |

## Related content

- [Customize a premium healthcare AI model with fine-tuning](fine-tune-premium-healthcare-models.md)
- [Fine-tune CxrReportGen Premium](fine-tune-cxrreportgen-premium.md)
- [Deploy and use MedImageInsight Premium](deploy-medimageinsight-premium.md)
- [Healthcare AI examples (GitHub)](https://aka.ms/HealthcareAIExamples)
