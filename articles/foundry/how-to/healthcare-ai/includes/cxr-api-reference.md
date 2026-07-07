---
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.date: 06/10/2026
ms.topic: include
---

The following API reference shows the request payload, headers, response schema, and error codes for the CxrReportGen Premium inference endpoint. Use it to send authenticated requests, confirm your deployment is reachable, and as a reference to build applications using the API.

### Request headers

- `Authorization: Bearer <your-api-key>`
- `Content-Type: application/json`

### Request body

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `model` | string | Yes | — | Served model name for the deployment. Use `CXRReportgen-Premium`. |
| `current_image` | base64 string | Yes | — | Frontal chest X-ray image (AP or PA view). |
| `prior_image` | base64 string | No | — | Prior frontal chest X-ray (AP or PA view). |
| `prior_report` | string | No | — | Prior radiology report text. |
| `indication` | string | No | — | Clinical indication. |
| `technique` | string | No | — | Imaging technique. |
| `comparison` | string | No | — | Comparison statement. |
| `max_tokens` | integer | No | `450` | Maximum tokens to generate. |
| `temperature` | float | No | `0.0` | Sampling temperature. `0.0` selects greedy decoding. |
| `text_normalize_unicode` | string | No | `both` | Apply Unicode NFKC normalization to the listed scope. Allowed values: `both`, `current`, `prior`, `none`. |
| `text_normalize_whitespace` | string | No | `both` | Collapse runs of whitespace to a single space in the listed scope. Allowed values: `both`, `current`, `prior`, `none`. |
| `text_normalize_strip` | string | No | `both` | Strip leading/trailing whitespace in the listed scope. Allowed values: `both`, `current`, `prior`, `none`. |

- **Supported image formats:** PNG and JPEG.
- **Image preparation.** If your source data is DICOM, convert each chest X-ray to a single PNG or JPEG and apply standard windowing before encoding. For reference DICOM-to-image conversion utilities, see the [Healthcare AI Examples](https://aka.ms/HealthcareAIExamples) repository.
- **Prior context is paired.** `prior_image` and `prior_report` must both be present and non-empty. If only one is sent, both are ignored by the model. Send each image once; don't duplicate.
- **Pass bare values** for `indication`, `technique`, and `comparison`. Don't include the field name in the value. For example, send `"indication": "Cough"`, not `"indication": "Indication: Cough"`.
- **Omit fields you don't have.** Send `null` or leave the key out. Don't send an empty string (`""`), which adds a labeled-but-empty field to the prompt.
- **Text normalization scope.** `current` covers `indication`, `technique`, `comparison`; `prior` covers `prior_report`; `both` covers all; `none` disables normalization.

**Minimal image-only request**

```json
{
  "model": "CXRReportgen-Premium",
  "current_image": "<base64-encoded-image>"
}
```

**Full request with context and prior study**

```json
{
  "model": "CXRReportgen-Premium",
  "current_image": "<base64-encoded-current-image>",
  "indication": "Shortness of breath",
  "technique": "Single frontal view",
  "comparison": "Comparison is made to prior study dated 2024-01-01.",
  "prior_image": "<base64-encoded-prior-image>",
  "prior_report": "Lungs are clear. No pleural effusion.",
  "max_tokens": 512,
  "temperature": 0.0
}
```

### Response body

| Field | Type | Description |
|---|---|---|
| `findings` | string | Generated draft findings text. |
| `model` | string | Identifier of the served model on the deployment. This value is the internal served-model name and won't match the deployment name you sent in the request. |
| `usage` | object | Token counts: `prompt_tokens`, `completion_tokens`, `total_tokens`. |

```json
{
  "findings": "Findings: ... Impression: ...",
  "model": "...",
  "usage": {
    "prompt_tokens": 1024,
    "completion_tokens": 87,
    "total_tokens": 1111
  }
}
```

### Response codes

| Status | Condition |
|---|---|
| `200` | Request succeeded. |
| `400` | Missing or invalid request field. Confirm that `model` is present in the request body. |
| `401` or `403` | Confirm that you're using a key for the same resource as the endpoint. |
| `404` | Confirm that the endpoint starts with `https://` and matches the endpoint shown for your deployment. |
| `422` | Invalid or missing image data. Confirm that `current_image` is present and contains a valid base64-encoded PNG or JPEG. |
