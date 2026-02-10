---
title: Azure OpenAI in Foundry Models Webhooks
titleSuffix: Azure OpenAI
description: Learn how to use webhooks with Azure OpenAI in Foundry Models.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 01/31/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
monikerRange: 'foundry-classic || foundry'
---

# Azure OpenAI in Foundry Models webhooks

Azure OpenAI webhooks enable your applications to receive real-time notifications about API events, such as batch completions or incoming calls. By subscribing to webhook events, you can automate workflows, trigger alerts, and integrate with other systems seamlessly. This guide walks you through setting up a webhook server, securing your endpoints, deploying, and troubleshooting common issues.

## Prerequisites

Install the required Python packages:

```bash
pip install flask openai websockets requests
```


## Webhook server setup

A webhook server is an application that listens for and processes automated messages (webhooks) sent by Azure OpenAI when specific events occur.

### Create the webhook listener application

Create a file called app.py with the following Flask application that receives and processes webhook events:

```python
from flask import Flask, request, Response
from openai import OpenAI, InvalidWebhookSignatureError
import os
import logging

app = Flask(__name__)

# Configure logging for Azure App Service
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(
    # api-key parameter is required, but If you are only using the client for webhooks the key can be a placeholder string 
    api_key=os.environ.get("OPENAI_API_KEY", "placeholder-key-for-webhooks-only"), 
    webhook_secret=os.environ["OPENAI_WEBHOOK_SECRET"] # This will be created later
)

@app.route("/webhook", methods=["POST"])
def webhook():
    """Webhook endpoint to receive and process OpenAI events."""
    try:
        # Unwrap and verify the message using the webhook secret
        event = client.webhooks.unwrap(request.data, request.headers)
        # Process the event based on type
        if event.type == "realtime.call.incoming":
            logger.info(f"Received a realtime.call.incoming message for call_id = {event.data.call_id}")
            # Add your custom logic here:
            # - Log the call details
            # - Trigger notifications
            # - Update databases
            # - Start call processing workflows
        elif event.type == "response.completed":
            logger.info(f"Received a response.completed message")
            # Add your custom logic here
        else:
            logger.info(f"Received unexpected message of type = {event.type}")
        # Always return 200 to acknowledge receipt
        return Response(status=200)
    except InvalidWebhookSignatureError as e:
        logger.error(f"Invalid signature: {e}")
        return Response("Invalid signature", status=400)
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return Response("Internal server error", status=500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
```

### Create a requirements.txt file

Create a `requirements.txt` file in the same directory as your `app.py` file:

```text
flask
openai
websockets
requests
```

## Create an Azure web app

Deploy your webhook server using [`az webapp up`](/cli/azure/webapp?view=azure-cli-latest#az-webapp-up&preserve-view=true). The command must be run from the folder where the `app.py` code for your application is located.

```bash
az webapp up --name unique-webhook-handler-name --resource-group myResourceGroup --runtime "PYTHON:3.12"
```

This command will:

- Create a resource group if it doesn't exist.
- Create an [App Service plan](/azure/app-service/overview-hosting-plans).
- Create a web app.
- Deploy your code.

Your webhook URL will be: `https://unique-webhook-handler-name.azurewebsites.net/webhook`

## Create webhook endpoint

With Azure OpenAI webhook endpoints must be created using the REST API. Register your listener to receive webhook events for specific event types.  

# [Python](#tab/python-key)

```python
import requests
import json
import os

AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
WEBHOOK_NAME = "<WEBHOOK-NAME>" # Give your webhook a custom name
WEBHOOK_URL = "<YOUR-URL>/webhook"  # e.g., "https://unique-webhook-handler-name.azurewebsites.net/webhook"

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

print(json.dumps(response.json(), indent=2))
```

# [REST](#tab/rest-api)


```bash
curl -X POST https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/dashboard/webhook_endpoints \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<WEBHOOK-NAME>",
    "url": "<YOUR-URL>/webhook", 
    "event_types": ["response.completed"]
  }'
```

# [Output](#tab/output)

```json
{
  "id": "<webhook_id>",
  "object": "webhook.endpoint",
  "created_at": 1757528725,
  "event_types": ["response.completed"],
  "name": "<WEBHOOK_NAME>",
  "signing_secret": "REDACTED",
  "signing_secret_hint": "whsec_...8s8=",
  "url": "https://my-webhook-handler.azurewebsites.net/webhook"
}
```

---

> [!IMPORTANT]
> The signing secret is only shown once during creation. Secrets can be stored securely using [Azure Key Vault](/azure/key-vault/general/overview).

### Configure webhook secret in Azure Web App

Set the webhook signing secret as an environment variable in your Azure Web App:

```bash
az webapp config appsettings set --name unique-webhook-handler-name \
  --resource-group myResourceGroup \
  --settings OPENAI_WEBHOOK_SECRET="<YOUR-SIGNING-SECRET-GOES-HERE>"
```

After setting the environment variable, restart your web app:

```bash
az webapp restart --name unique-webhook-handler-name --resource-group myResourceGroup
```

## Testing webhook messages

First confirm that your web app finished restarting by checking the log stream:

```bash
az webapp log tail --name unique-webhook-handler-name --resource-group myResourceGroup
```

Once the restart is complete, You can test your webhook endpoint by sending sample REST API events.

# [Python](#tab/python-key)

```python
import requests
import time
import json

WEBHOOK_URL = "https://<unique-webhook-handler-name>.azurewebsites.net/webhook"
TEST_TIMESTAMP = int(time.time())

headers = {
    "Content-Type": "application/json",
    "Webhook-ID": "test-id",
    "Webhook-Timestamp": str(TEST_TIMESTAMP),
    "Webhook-Signature": "test-signature"
}

payload = {
    "object": "event",
    "id": "test-event",
    "type": "response.completed",
    "created_at": TEST_TIMESTAMP,
    "data": {
        "call_id": "test-call",
        "sip_headers": []
    }
}

try:
    # timeout in seconds (connect timeout, read timeout)
    response = requests.post(WEBHOOK_URL, headers=headers, json=payload, timeout=(5, 30))
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except requests.exceptions.Timeout:
    print("Request timed out!")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

# [REST](#tab/rest-api)

```bash
curl -X POST https://my-webhook-handler.azurewebsites.net/webhook \
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

# [Output](#tab/output)

```text
Status Code: 400
Response: Invalid signature
```

A response of `Invalid signature` indicates that your webhook listener successfully handled you test call. You'll also see the message in the log stream for your web app: 

`2025-10-24T23:34:57.576593554Z ERROR:app:Invalid signature: The given webhook signature does not match the expected signature`

---

> [!NOTE]
> The initial test signature won't pass validation. For production testing, we can trigger actual events from Azure OpenAI with valid signatures.

Now launch the log stream for your webhook listener webapp if it isn't still running:

```bash
az webapp log tail --name unique-webhook-handler-name --resource-group myResourceGroup
```

 To test again with a valid signature make a call with the responses API with `background=True` set.

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

resp = client.responses.create(
  model="o4-mini",
  input="Write a very long novel about otters in space.",
  background=True,
)

print(resp.status)
```

**Python output**:

```output
queued 
```

**Log stream output**:

```text
2025-10-24T23:40:23.623889430Z INFO:app:Received a response.completed message
```

## Security best practices

Securing your webhook endpoint is critical. Follow these recommendations:

### Signature verification

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

### Timeout handling

Respond quickly to avoid webhook timeouts. Offload heavy processing to background threads:

```python
def process_call_async(call_data):
    # Your heavy processing here
    pass

# In webhook handler:
threading.Thread(target=process_call_async, args=(event.data,)).start()
return Response(status=200)
```

### Additional recommendations

* Store your signing secret securely; it's only shown once during creation.
* Use HTTPS for all webhook endpoints.
* Protect and rotate Azure access tokens regularly.
* Validate incoming requests using the signing secret.

## Event processing examples

Here are some common patterns for processing webhook events:

### Call logging

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

### Notification system

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

### List webhook endpoints

```bash
curl -X GET https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/dashboard/webhook_endpoints \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Content-Type: application/json"
```

### Update webhook endpoint

> [!NOTE] 
> Update webhook properties such as name, URL, and registered event types. The signing secret can't be updated through this operation.

```bash
curl -X POST https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/dashboard/webhook_endpoints/<webhook_id> \
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

### Delete webhook endpoint

Remove a webhook endpoint using its webhook ID:

```bash
curl -X DELETE https://<YOUR-RESOURCE-NAME>.openai.azure.com/openai/v1/dashboard/webhook_endpoints/<webhook_id> \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H "Accept: application/json"
```

## Common issues and troubleshooting

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
- **`type`**: Event type (for example, "realtime.call.incoming")
- **`created_at`**: Unix timestamp when the event was created
- **`data`**: Event-specific data containing call information and SIP headers

## Webhook events reference

The following event types are available for webhook registration:

| Category          | Event Type               | Description                     |
| ----------------- | ------------------------ | ------------------------------- |
| Response Events   | `response.completed`     | Response successfully completed |
|                   | `response.failed`        | Response failed                 |
|                   | `response.cancelled`     | Response canceled               |
|                   | `response.incomplete`    | Response incomplete             |
| Batch Events      | `batch.completed`        | Batch successfully completed    |
|                   | `batch.failed`           | Batch failed                    |
|                   | `batch.cancelled`        | Batch canceled                  |
|                   | `batch.expired`          | Batch expired                   |
| Fine-tuning Events| `fine_tuning.job.succeeded` | Fine-tuning job succeeded    |
|                   | `fine_tuning.job.failed`    | Fine-tuning job failed       |
|                   | `fine_tuning.job.cancelled` | Fine-tuning job canceled     |
| Real-time Events  | `realtime.call.incoming` | Incoming call event             |

### Example payload

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

## Clean up resources

When you no longer need the webhook server, you can delete the Azure Web App and its associated resources.

### Delete the web app only

To delete just the web app while keeping the resource group and other resources:

```bash
az webapp delete --name unique-webhook-handler-name --resource-group myResourceGroup
```

## Additional suggested configurations

* Implement proper logging and monitoring for webhook events.
* Add database storage for call records.
* Set up alerting for failed webhook deliveries.
* Implement retry logic for downstream service calls.
* Add authentication for your webhook endpoint if needed.
