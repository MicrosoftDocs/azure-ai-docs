---
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 02/17/2026
---

## Transcription error handling

When you call the fast transcription API, implement retry logic to handle transient errors and rate limiting. The API enforces rate limits, which can result in an error during high-concurrency operations.

### Recommended retry configuration

- Retry up to five times on transient errors.

- Use exponential backoff: 2 seconds, 4 sec, 8 sec, 16 sec, 32 sec.

- Total backoff time: 62 sec.

This configuration provides sufficient time for the API to recover during rate-limiting windows, especially when you run batch operations with multiple concurrent workers.

### When to use retry logic

Implement retry logic for the following error categories:

- **HTTP errors** - Retry on:
  - HTTP 429 (rate limit)
  - HTTP 500, 502, 503, 504 (server errors)
  - `status_code=None` (incomplete response downloads)

- **Azure SDK network errors** - Retry on:
  - `ServiceRequestError`
  - `ServiceResponseError`
  
  These errors wrap low-level network exceptions like `urllib3.exceptions.ReadTimeoutError`, connection resets, and TLS failures.

- **Python network exceptions** - Retry on:
  - `ConnectionError`
  - `TimeoutError`
  - `OSError`

Don't retry on the following errors, because they indicate client-side issues that require correction:

- HTTP 400 (bad request)
- HTTP 401 (unauthorized)
- HTTP 422 (unprocessable entity)
- Other client errors (4xx status codes)

### Implementation notes

- Reset the audio file stream (`seek(0)`) before each retry attempt.

- When you use concurrent workers, be aware that the default HTTP read timeout (300 seconds) might be exceeded under heavy rate limiting.

- Be aware that the API might accept a request but time out while generating the response. This condition can appear as an SDK-wrapped network error rather than a standard HTTP error.
