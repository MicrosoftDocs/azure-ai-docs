---
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.date: 06/10/2026
ms.topic: include
---

The following API reference shows the request payload, headers, response schema, and error codes for the MedImageInsight Premium embedding endpoint. Use it to send authenticated requests, confirm your deployment is reachable, and as a reference to build applications using the API.

### Request headers

- `Authorization: Bearer <your-api-key>`
- `Content-Type: application/json`

### Request body

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `model` | string | Yes | — | Served model name for the deployment. |
| `texts` | string array | Conditional | — | Text inputs to embed. Provide `texts` or `images`. |
| `images` | string array | Conditional | — | Images as base64 data URIs (for example, `data:image/png;base64,...`). Provide `texts` or `images`. |
| `embedding_types` | string array | No | `["float"]` | Accepted values: `float` (recommended), `binary`, `ubinary`, `base64`. See [Embedding formats](#embedding-formats). |

- **One modality per request.** Provide `texts` or `images`, not both. If both fields are present, the endpoint silently processes one and ignores the other.
- **Batching is supported.** You can send multiple items in a single call. The response returns one vector per item, ordered to match the input array.
- **Supported image formats:** PNG and JPEG.
- **Image preparation.** If your source data is DICOM, convert it before sending. The model expects single 2D images; for volumetric studies (CT, MRI), select the relevant slice and apply standard windowing for the modality before encoding. For reference DICOM-to-image conversion and modality-specific preprocessing utilities, see the [Healthcare AI Examples](https://aka.ms/HealthcareAIExamples) repository.

#### Embedding formats

The response key matches the requested type (for example, `embeddings.binary` when you request `binary`).

- **`float`** (recommended): list of 1024 float values per vector. The canonical embedding.
- **`base64`**: the float vector encoded as raw float32 bytes, base64-encoded. Lossless equivalent of `float`, smaller wire payload.
- **`binary`** / **`ubinary`**: 128 bytes per vector — the 1024 sign bits of the float vector, packed 8 per byte. 32× smaller but lossy (only preserves sign). Suitable for fast approximate similarity search using Hamming distance.

**Minimal text-only request**

```json
{
  "model": "MedImageInsight-Premium",
  "texts": ["x-ray chest anteroposterior Atelectasis."]
}
```

**Full image-embedding request**

```json
{
  "model": "MedImageInsight-Premium",
  "images": ["data:image/png;base64,<base64-encoded-image>"]
}
```

### Response body

| Field | Type | Description |
|---|---|---|
| `embeddings.float` | array of float arrays | List of embedding vectors. Each vector is a list of 1024 floating-point numbers. The outer list has one vector per input item, ordered to match your `texts` or `images`. |
| `id` | string | Unique identifier for the request. |
| `texts` | string array | Echo of the input texts, if provided. |
| `meta` | object | Request metadata including API version and billed units. |
| `response_type` | string | Response format identifier. |

```json
{
  "id": "...",
  "embeddings": {
    "float": [[0.0123, -0.0456, "... (1024 floats total)"]]
  },
  "texts": ["x-ray chest anteroposterior Atelectasis."],
  "meta": { ... },
  "response_type": "embeddings_by_type"
}
```

### Response codes

| Status | Condition |
|---|---|
| `200` | Request succeeded. |
| `400` | Missing or invalid request field. Confirm that `model` is present, `images` values use the `data:image/...;base64,` prefix, and any provided `embedding_types` values are valid. |
| `401` or `403` | Confirm that you're using a key for the same resource as the endpoint. |
| `404` | Confirm that the endpoint starts with `https://` and matches the endpoint shown for your deployment. |
