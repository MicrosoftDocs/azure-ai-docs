---
title: 'Use the GPT Realtime API via SIP'
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Learn how to use the GPT Realtime API for speech and audio via SIP.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/12/2026
author: PatrickFarley
ms.author: pafarley
ms.custom: references_regions
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted

---

# Use the GPT Realtime API via SIP

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Azure OpenAI GPT Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. 

You can use the Realtime API via WebRTC, SIP, or WebSocket to send audio input to the model and receive audio responses in real time. Follow the instructions in this article to get started with the Realtime API via SIP.

SIP is a protocol used to make phone calls over the internet. With SIP and the Realtime API you can direct incoming phone calls to the API.

## Supported models

The GPT real-time models are available for global deployments in [East US 2 and Sweden Central regions](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- `gpt-4o-mini-realtime-preview` (`2024-12-17`)
- `gpt-4o-realtime-preview` (`2024-12-17` and `2025-06-03`)
- `gpt-realtime` (`2025-08-28`)
- `gpt-realtime-mini` (`2025-10-06`)
- `gpt-realtime-mini-2025-12-15` (`2025-12-15`)

## Prerequisites

Before you can use GPT real-time audio, you need:

:::moniker range="foundry"
- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) in one of the [supported regions](#supported-models).
- A deployment of the `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model in a supported region as described in the [supported models](#supported-models) section in this article.
    - In the Microsoft Foundry portal, load your project. Select **Build** in the upper right menu, then select the **Models** tab on the left pane, and **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.
- Azure role assignment: **Cognitive Services User** or **Cognitive Services Contributor** on your resource.
:::moniker-end

:::moniker range="foundry-classic"

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](create-resource.md).
- A deployment of the `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model in a supported region as described in the [supported models](#supported-models) section in this article. You can deploy the model from the [Foundry model catalog](../../../ai-foundry/how-to/model-catalog-overview.md) or from your project in Microsoft Foundry portal.
- Azure role assignment: **Cognitive Services User** or **Cognitive Services Contributor** on your resource.
:::moniker-end

For the code samples in this article, you also need:

- Python 3.8 or later.
- The following Python packages installed:
  - `openai>=1.0.0` (includes webhook support)
  - `flask>=2.0.0`
  - `websockets>=10.0`
  - `requests`
- An account with a SIP trunking provider (for example, Twilio, Vonage, or Bandwidth).
- A phone number purchased from your SIP provider.

## Connect to SIP

To connect a phone number to the Realtime API, use a SIP trunking provider (for example, Twilio). A trunking provider is a service that converts your phone call to IP traffic.

1. Purchase a phone number from your SIP trunking provider.
1. Create a webhook for incoming calls using the [Azure OpenAI Webhook Service REST API](../../../ai-foundry/openai/how-to/webhooks.md).
1. Get the internal ID of your Azure OpenAI resource:
   1. In the Azure portal, navigate to your resource.
   1. Select **JSON View** to find the internal ID.
1. Construct your project ID using the format `proj_<internalId>` (for example, `proj_88c4a88817034471a0ba0fcae24ceb1b`).
1. Configure your SIP trunk to route calls to: `sip:proj_<internalId>@<region>.sip.ai.azure.com;transport=tls`

> [!NOTE]
> The currently supported regions for SIP are `swedencentral` and `eastus2`. 

## Handling incoming calls

When Azure OpenAI receives SIP traffic associated with your project, your webhook endpoint receives an incoming event message. The event fired for SIP calls is type = `realtime.call.incoming` like the example shown here. 

```http
POST https://my_website.com/webhook_endpoint
user-agent: OpenAI/1.0 (+https://platform.openai.com/docs/webhooks)
content-type: application/json
webhook-id: wh_685342e6c53c8190a1be43f081506c52 # unique ID for idempotency
webhook-timestamp: 1750287078 # timestamp of delivery attempt
webhook-signature: v1,Signature # signature to verify authenticity from OpenAI

{
  "object": "event",
  "id": "evt_685343a1381c819085d44c354e1b330e",
  "type": "realtime.call.incoming",
  "created_at": 1750287018, // Unix timestamp
  "data": {
    "call_id": "some_unique_id",
    "sip_headers": [
      { "name": "From", "value": "sip:+142555512112@sip.example.com" },
      { "name": "To", "value": "sip:+18005551212@sip.example.com" },
      { "name": "Call-ID", "value": "rtc_xyz"}
    ]
  }
}
```

From your webhook endpoint, you can accept, reject, or refer this call, using the call_id value from the webhook event. When accepting the call, you provide the needed configuration (instructions, voice, etc.) for the Realtime API session. Once established, you can set up a WebSocket and monitor the session as usual. The APIs to accept, reject, monitor, refer, and hang up the call are documented in the following sections.

### Accept the call and configure the session

Use the Accept call endpoint to approve the inbound call and configure the real-time session that answers it. Send the same parameters you would send in to a create client secret. You can include any values you would use in a `session.update` message, but `type`, `model`, and `instructions` are required.

> [!NOTE]
> For authorization, you can either use the `api-key` header or the Bearer token as shown here. Remember the model name is actually the name of your deployment. 

```bash
curl -X POST "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/$CALL_ID/accept" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "type": "realtime",
        "model": "gpt-realtime",
        "instructions": "You are Alex, a friendly concierge for Example Corp."
      }'
```

The request path must include:

- The `call_id` from the `realtime.call.incoming` webhook event
- `Authorization` (or `api-key`) header 

The endpoint returns `200 OK` once the SIP leg is ringing and the real-time session is being established.

> [!TIP]
> **Verify**: A successful accept returns HTTP 200. Check your webhook server logs for the response status.

### Reject unwanted calls

Use the Reject call endpoint to decline an invite when you don't want to handle the incoming call (for example, from an unsupported country/region code). To control the response sent back to the carrier, supply an optional SIP status code along with the required `call_id` path parameter. The following example shows a request sending `486`, which indicates the system is too busy to take the call.

```bash
curl -X POST "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/$CALL_ID/reject" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status_code": 486}'
```

If no status code is supplied, the SIP server sends a status code of `603` (Decline) to the carrier. A successful request responds with `200 OK` after the SIP response is delivered.

### Transfer (refer) the call to another endpoint

Transfer an active call using the Refer call endpoint. Provide the `call_id` and the `target_uri` that should be placed in the SIP `Refer-To` header (for example, `tel:+14155550123` or `sip:agent@example.com`).

```bash
curl -X POST "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/$CALL_ID/refer" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_uri": "tel:+14155550123"}'
```

The API returns `200 OK` once the REFER is relayed to your SIP provider. The downstream system handles the rest of the call flow for the caller.

### Monitor call events and issue session commands

After you accept a call, open a WebSocket connection to the same session to stream events and issue Realtime API commands. To create a WebSocket to an existing call, you must use the `call_id` parameter. The model argument isn't used because it's configured as part of the JSON when accepting the call. The following example shows a common scenario: issuing a `response.create` message to instruct the Realtime API system to answer the phone and say hello.

Here's a sample of a WebSocket request to a specific SIP call:

```http
GET wss://<your azure resource name>.openai.azure.com/openai/v1/realtime?call_id={call_id}
```

**Query parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `call_id` | string | Identifier from the `realtime.call.incoming` webhook. |

**Headers**

`Authorization: Bearer $TOKEN` (or `api-key: <your API key>`)

The WebSocket behaves exactly like any other Realtime API connection. You can send messages like `response.create` or `session.update` to control the call, and listen for server events to track progress. 

The following code snippet illustrates how a WebSocket connection is made:

```javascript
import WebSocket from "ws";

const callId = "rtc_u1_9c6574da8b8a41a18da9308f4ad974ce";
const ws = new WebSocket(`wss://<your azure resource name>.openai.azure.com/openai/v1/realtime?call_id=${callId}`, {
    headers: {
        "api-key": `${process.env.OPENAI_API_KEY}`,
    },
});

ws.on("open", () => {
    ws.send(
        JSON.stringify({
            type: "response.create",
        })
    );
});
```

> [!TIP]
> **Verify**: You should receive a `session.created` event on the WebSocket within a few seconds of connecting.

### End the session and disconnect

End the session with the Hang up endpoint when your application should disconnect the caller. This endpoint can be used to terminate both SIP and WebRTC real-time sessions.

```bash
curl -X POST "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/$CALL_ID/hangup" \
  -H "Authorization: Bearer $TOKEN"
```

The API responds with `200 OK` when it starts tearing down the call.

## Sample webhook endpoint

The following code is a Python example of a `realtime.call.incoming` handler. It accepts the call and then logs all the events from the Realtime API.

```python
from flask import Flask, request, Response
from openai import OpenAI, InvalidWebhookSignatureError
import asyncio
import json
import os
import requests
import time
import threading
import websockets

app = Flask(__name__)
client = OpenAI(
    webhook_secret=os.environ["OPENAI_WEBHOOK_SECRET"]
)

AUTH_HEADER = {
    "api-key": os.getenv("OPENAI_API_KEY")
}

call_accept = {
    "type": "realtime",
    "instructions": "You are a support agent.",
    "model": "gpt-realtime",
}

response_create = {
    "type": "response.create",
    "response": {
        "instructions": (
            "Say to the user 'Thank you for calling, how can I help you'"
        )
    },
}


async def websocket_task(call_id):
    try:
        async with websockets.connect(
            "wss://<your azure resource>.openai.azure.com/openai/v1/realtime?call_id=" + call_id,
            additional_headers=AUTH_HEADER,
        ) as websocket:
            await websocket.send(json.dumps(response_create))

            while True:
                response = await websocket.recv()
                print(f"Received from WebSocket: {response}")
    except Exception as e:
        print(f"WebSocket error: {e}")


@app.route("/", methods=["POST"])
def webhook():
    try:
        event = client.webhooks.unwrap(request.data, request.headers)

        if event.type == "realtime.call.incoming":
            requests.post(
                "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/"
                + event.data.call_id
                + "/accept",
                headers={**AUTH_HEADER, "Content-Type": "application/json"},
                json=call_accept,
            )
            threading.Thread(
                target=lambda: asyncio.run(
                    websocket_task(event.data.call_id)
                ),
                daemon=True,
            ).start()
            return Response(status=200)
    except InvalidWebhookSignatureError as e:
        print("Invalid signature", e)
        return Response("Invalid signature", status=400)


if __name__ == "__main__":
    app.run(port=8000)

```

## Troubleshooting

### Webhook signature verification fails

If you receive `InvalidWebhookSignatureError`:

- Verify your `OPENAI_WEBHOOK_SECRET` environment variable matches the secret from webhook creation.
- Ensure you're passing raw request body bytes to `unwrap()`, not parsed JSON.
- Check that no middleware is modifying the request body before verification.

### SIP calls not reaching webhook

- Verify your SIP trunk is configured to route to `<region>.sip.ai.azure.com`.
- Confirm TLS is enabled (`transport=tls` in SIP URI).
- Check that your project ID format is correct: `proj_<32-character-hex-id>`.

### WebSocket connection fails

- Ensure you're using `wss://` (secure WebSocket), not `ws://`.
- Verify the `call_id` matches an accepted call.
- Check that your API key or token has access to the resource.

### Common SIP status codes

| Code | Meaning | Resolution |
|------|---------|------------|
| 486 | Busy Here | System overloaded; implement retry logic |
| 603 | Decline | Call explicitly rejected; check your accept/reject logic |
| 408 | Request Timeout | Network issue; verify connectivity to Azure |

## Related content

- [Use the Realtime API via WebRTC](./realtime-audio-webrtc.md) for browser-based applications
- [Use the Realtime API via WebSocket](./realtime-audio-websockets.md) for server-to-server scenarios
- [Azure OpenAI webhooks](./webhooks.md) for webhook configuration details
- [Realtime API reference](../realtime-audio-reference.md) for complete API documentation

