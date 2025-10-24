---
title: Azure OpenAI Webhooks
titleSuffix: Azure OpenAI
description: Learn how to use webhooks with Azure OpenAI in AI Foundry Models.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 10/10/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
---

Azure OpenAI webhooks enable your applications to receive real-time notifications about API events, such as batch completions or incoming calls. By subscribing to webhook events, you can automate workflows, trigger alerts, and integrate with other systems seamlessly. This guide walks you through setting up a webhook server, securing your endpoints, deploying to production, and troubleshooting common issues.

## Create webhook endpoint

With Azure OpenAI webhook endpoints must be created using the REST API. Register your listener to receive webhook events for specific event types.  

> [!IMPORTANT]
> The signing secret is only shown once during creation. Store it securely.

# [Python)](#tab/python-key)

```python
import requests
import os

AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
WEBHOOK_NAME = "<WEBHOOK-NAME>"
WEBHOOK_URL = "<YOUR-URL>/webhook"  # e.g., "https://my-webhook-handler.azurewebsites.net/webhook"

url = "https://<YOUR_RESOURCE_NAME>.openai.azure.com/openai/v1/dashboard/webhook_endpoints"

headers = {
    "api-key": AZURE_OPENAI_API_KEY,
    "Content-Type": "application/json"
}

data = {
    "name": WEBHOOK_NAME,
    "url": WEBHOOK_URL,
    "event_types": ["response.completed"]
}

response = requests.post(url, headers=headers, json=data)

print(response.json())
```

# [REST](#tab/rest-api)


```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/dashboard/webhook_endpoints \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<WEBHOOK-NAME>",
    "url": "<YOUR-URL>/webhook",  # e.g., "https://my-webhook-handler.azurewebsites.net/webhook"
    "event_types": ["response.completed"]
  }'
```

# [Output](#tab/rest-api)

```json
{
  "id": "<webhook_id>",
  "object": "webhook.endpoint",
  "created_at": 1757528725,
  "event_types": ["realtime.call.incoming"],
  "name": "<WEBHOOK_NAME>",
  "signing_secret": "REDACTED",
  "signing_secret_hint": "whsec_...8s8=",
  "url": "https://my-webhook-handler.azurewebsites.net/webhook"
}
```

---

## Webhook Server Setup

A webhook server is an application that listens for and processes automated messages (webhooks) sent by Azure OpenAI when specific events occur.

### Prerequisites

Install the required Python packages:

```bash
pip install flask openai websockets requests
````

Set your webhook secret (obtained during webhook creation):

```bash
export OPENAI_WEBHOOK_SECRET="your_webhook_signing_secret_here"
```

### Example: Minimal Flask Webhook Listener

Below is a sample Flask application that receives and processes webhook events:

```python
from flask import Flask, request, Response
from openai import OpenAI, InvalidWebhookSignatureError
import os
import threading

app = Flask(__name__)

# Initialize OpenAI client with webhook secret
client = OpenAI(
    webhook_secret=os.environ["OPENAI_WEBHOOK_SECRET"]
)

@app.route("/", methods=["POST"])
def webhook():
    """Webhook endpoint to receive and process OpenAI events."""
    try:
        # Unwrap and verify the message using the webhook secret
        event = client.webhooks.unwrap(request.data, request.headers)
        # Process the event based on type
        if event.type == "realtime.call.incoming":
            print(f"Received a realtime.call.incoming message for call_id = {event.data.call_id}")
            # Add your custom logic here:
            # - Log the call details
            # - Trigger notifications
            # - Update databases
            # - Start call processing workflows
        else:
            print(f"Received unexpected message of type = {event.type}")
        # Always return 200 to acknowledge receipt
        return Response(status=200)
    except InvalidWebhookSignatureError as e:
        print(f"Invalid signature: {e}")
        return Response("Invalid signature", status=400)
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return Response("Internal server error", status=500)

if __name__ == "__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000, debug=True)
```

## Security Best Practices

Securing your webhook endpoint is critical. Follow these recommendations:

### Signature Verification

Always verify the webhook signature to ensure requests are from Azure OpenAI:

```python
try:
    event = client.webhooks.unwrap(request.data, request.headers)
except InvalidWebhookSignatureError:
    return Response("Invalid signature", status=400)
```

### Idempotency

Use the `Webhook-ID` header to prevent duplicate processing:

```python
webhook_id = request.headers.get('Webhook-ID')
if webhook_id in processed_webhooks:
    return Response(status=200)  # Already processed
```

### Timeout Handling

Respond quickly to avoid webhook timeouts. Offload heavy processing to background threads:

```python
def process_call_async(call_data):
    # Your heavy processing here
    pass

# In webhook handler:
threading.Thread(target=process_call_async, args=(event.data,)).start()
return Response(status=200)
```

### Additional Recommendations

* Store your signing secret securely; it is only shown once during creation.
* Use HTTPS for all webhook endpoints.
* Protect and rotate Azure access tokens regularly.
* Validate incoming requests using the signing secret.

## Webhook Server Deployment

### Run your server locally

Set environment variables:

```bash
export OPENAI_WEBHOOK_SECRET="your_webhook_signing_secret"
```

Run the Flask application:

```bash
python webhook_listener.py
```

### Azure Web App

To deploy your webhook server to Azure Web App:

```bash
az webapp up --name my-webhook-handler --resource-group myResourceGroup
```

Set environment variables in Azure:

```bash
az webapp config appsettings set --name my-webhook-handler \
  --resource-group myResourceGroup \
  --settings OPENAI_WEBHOOK_SECRET="your_webhook_signing_secret"
```

### Docker

Create a `Dockerfile` for containerized deployment:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "webhook_listener.py"]
```

## Testing webhook messages

You can test your webhook endpoint locally by sending sample events using `curl`. You�ll need to create a message signature using your encoded secret.

```bash
curl -X POST https://your-webhook-url.com/webhook \
  -H "Content-Type: application/json" \
  -H "Webhook-ID: test-id" \
  -H "Webhook-Timestamp: $(date +%s)" \
  -H "Webhook-Signature: v1,test-signature" \
  -d '{
    "object": "event",
    "id": "test-event",
    "type": "response.completed",
    "created_at": 1750287018,
    "data": {
      "call_id": "test-call",
      "sip_headers": []
    }
  }'
```

## Event Processing Examples

Here are some common patterns for processing webhook events:

### Call Logging

```python
if event.type == "realtime.call.incoming":
    call_data = {
        'call_id': event.data.call_id,
        'timestamp': event.created_at,
        'from': next((h['value'] for h in event.data.sip_headers if h['name'] == 'From'), None),
        'to': next((h['value'] for h in event.data.sip_headers if h['name'] == 'To'), None)
    }
    # Log to database or file
    log_call(call_data)
```

### Notification System

```python
if event.type == "realtime.call.incoming":
    # Send notification to monitoring system
    send_notification({
        'type': 'incoming_call',
        'call_id': event.data.call_id,
        'caller': get_caller_from_headers(event.data.sip_headers)
    })
```

## Managing webhook endpoints

### List Webhook Endpoints

```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/dashboard/webhook_endpoints \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json"
```

### Update Webhook Endpoint

Update webhook properties such as name, URL, and registered event types.  
**Note:** The signing secret cannot be updated through this operation.

```bash
curl -X POST https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/dashboard/webhook_endpoints/<webhook_id> \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<UpdatedName>",
    "url": "<UpdatedURL>",
    "event_types": [
      "response.completed",
      "response.failed",
      "realtime.call.incoming"
    ]
  }'
```

### Delete Webhook Endpoint

Remove a webhook endpoint using its webhook ID:

```bash
curl -X DELETE https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/dashboard/webhook_endpoints/<webhook_id> \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Accept: application/json"
```

## Common Issues & Troubleshooting

| Issue                 | Solution                                                                                             |
| --------------------- | ---------------------------------------------------------------------------------------------------- |
| **Invalid Signature** | Verify your `OPENAI_WEBHOOK_SECRET` is correct and matches the secret provided at creation.          |
| **Timeouts**          | Keep webhook processing under 10 seconds; use background tasks for heavy operations.                 |
| **Missing Events**    | Ensure your endpoint is publicly accessible and uses HTTPS. Monitor delivery attempts in Azure logs. |

## Handling webhook requests on a server

When an event happens that you're subscribed to, you'll receive a POST request with the following structure:

```http
POST https://my-webhook-handler.azurewebsites.net/webhook
User-Agent: OpenAI/1.0 (+https://platform.openai.com/docs/webhooks)
Content-Type: application/json
Webhook-ID: <webhook_eventid>
Webhook-Timestamp: 1750287078
Webhook-Signature: v1,Sample Signature
{
  "object": "event",
  "id": "evt_685343a1381c819085d44c354e1b330e",
  "type": "realtime.call.incoming",
  "created_at": 1750287018,
  "data": {
    "call_id": "some_unique_id",
    "sip_headers": [
      { 
        "name": "From", 
        "value": "sip:+142555512112@sip.example.com" 
      },
      { 
        "name": "To", 
        "value": "sip:+18005551212@sip.example.com" 
      },
      { 
        "name": "Call-ID", 
        "value": "rtc_9d3d08ea002a4909813d207a592957c4"
      }
    ]
  }
}
```

**Header**

- **`Webhook-ID`**: Unique identifier for idempotency - use this to prevent duplicate processing
- **`Webhook-Timestamp`**: Unix timestamp of the delivery attempt
- **`Webhook-Signature`**: Cryptographic signature to verify authenticity from OpenAI

**Payload**

- **`object`**: Always "event" for webhook events
- **`id`**: Unique event identifier
- **`type`**: Event type (e.g., "realtime.call.incoming")
- **`created_at`**: Unix timestamp when the event was created
- **`data`**: Event-specific data containing call information and SIP headers

## Webhook Events Reference

The following event types are available for webhook registration:

| Category        | Event Type               | Description                     |
| --------------- | ------------------------ | ------------------------------- |
| Response Events | `response.completed`     | Response successfully completed |
|                 | `response.failed`        | Response failed                 |
|                 | `response.cancelled`     | Response cancelled              |
|                 | `response.incomplete`    | Response incomplete             |
| Batch Events    | `batch.completed`        | Batch successfully completed    |
|                 | `batch.failed`           | Batch failed                    |
|                 | `batch.cancelled`        | Batch cancelled                 |
|                 | `batch.expired`          | Batch expired                   |
| Realtime Events | `realtime.call.incoming` | Incoming call event             |

### Example Payload

```json
{
  "object": "event",
  "id": "evt_685343a1381c819085d44c354e1b330e",
  "type": "realtime.call.incoming",
  "created_at": 1750287018,
  "data": {
    "call_id": "some_unique_id",
    "sip_headers": [
      { "name": "From", "value": "sip:+142555512112@sip.example.com" },
      { "name": "To", "value": "sip:+18005551212@sip.example.com" },
      { "name": "Call-ID", "value": "rtc_9d3d08ea002a4909813d207a592957c4" }
    ]
  }
}
```

## Next steps

* Implement proper logging and monitoring for webhook events.
* Add database storage for call records.
* Set up alerting for failed webhook deliveries.
* Implement retry logic for downstream service calls.
* Add authentication for your webhook endpoint if needed.