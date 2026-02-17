




## Error handling best practices

### Implement retry logic with exponential backoff

When calling the fast transcription API, implement retry logic to handle transient errors and rate limiting. The API enforces rate limits, which can result in HTTP 429 responses during high-concurrency operations.

#### Recommended retry configuration

- Retry up to 5 times on transient errors
- Use exponential backoff: 2s, 4s, 8s, 16s, 32s
- Total backoff time: 62 seconds

This configuration provides sufficient time for the API to recover during rate-limiting windows, especially when running batch operations with multiple concurrent workers.

#### Handle these error types

Implement retry logic for the following error categories:

1. **HTTP errors** - Retry on:
   - HTTP 429 (rate limit)
   - HTTP 500, 502, 503, 504 (server errors)
   - `status_code=None` (incomplete response downloads)

2. **Azure SDK network errors** - Retry on:
   - `ServiceRequestError`
   - `ServiceResponseError`
   
   These errors wrap low-level network exceptions like `urllib3.exceptions.ReadTimeoutError`, connection resets, and TLS failures.

3. **Python network exceptions** - Retry on:
   - `ConnectionError`
   - `TimeoutError`
   - `OSError`

#### Non-retryable errors

Don't retry on the following errors, as they indicate client-side issues that require correction:

- HTTP 400 (bad request)
- HTTP 401 (unauthorized)
- HTTP 422 (unprocessable entity)
- Other client errors (4xx status codes)

#### Implementation notes

- Reset the audio file stream (`seek(0)`) before each retry attempt
- When using concurrent workers, be aware that the default HTTP read timeout (300 seconds) might be exceeded under heavy rate limiting
- The API might accept a request but time out while generating the response, which can appear as SDK-wrapped network errors rather than standard HTTP errors

### Configure diarization

When enabling speaker diarization, set the maximum number of speakers based on your audio content. For example:

```python
diarization_options = TranscriptionDiarizationOptions(
    enabled=True,
    max_speakers=35
)
```

### Use phrase lists for better accuracy

Provide a phrase list to improve recognition of domain-specific terms:

```python
phrase_list = PhraseListProperties(
    phrases=["term1", "term2", "term3"]
)
```

Phrase lists are supported in fast transcription (default mode) but not in LLM speech (enhanced mode). For LLM speech, use custom prompting instead to emphasize specific terms.