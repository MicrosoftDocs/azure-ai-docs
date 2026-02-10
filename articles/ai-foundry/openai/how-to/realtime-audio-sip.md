---
title: 'Use the GPT Realtime API via SIP'
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Learn how to use the GPT Realtime API for speech and audio via SIP.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/30/2026
author: PatrickFarley
ms.author: pafarley
ms.custom: references_regions
recommendations: false
monikerRange: 'foundry-classic || foundry'

---

# Use the GPT Realtime API via SIP

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Azure OpenAI GPT Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. 

You can use the Realtime API via WebRTC, SIP, or WebSocket to send audio input to the model and receive audio responses in real time. Follow the instructions in this article to get started with the Realtime API via SIP.

SIP is a protocol used to make phone calls over the internet. With SIP and the Realtime API you can direct incoming phone calls to the API.

## Supported models

The GPT real-time models are available for global deployments in [East US 2 and Sweden Central regions](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- `gpt-4o-mini-realtime-preview` (2024-12-17)
- `gpt-4o-realtime-preview` (2024-12-17)
- `gpt-realtime` (version 2025-08-28)
- `gpt-realtime-mini` (version 2025-10-06)
- `gpt-realtime-mini-2025-12-15` (version 2025-12-15)

## Prerequisites

Before you can use GPT real-time audio, you need:


:::moniker range="foundry"
- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) in one of the [supported regions](#supported-models).
- A deployment of the `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model in a supported region as described in the [supported models](#supported-models) section in this article.
    - In the Microsoft Foundry portal, load your project. Select **Build** in the upper right menu, then select the **Models** tab on the left pane, and **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.
:::moniker-end

:::moniker range="foundry-classic"

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](create-resource.md).
- A deployment of the `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model in a supported region as described in the [supported models](#supported-models) section in this article. You can deploy the model from the [Foundry model catalog](../../../ai-foundry/how-to/model-catalog-overview.md) or from your project in Microsoft Foundry portal. 
:::moniker-end

## Connecting to SIP 

If you want to connect a phone number to the Realtime API, use a SIP trunking provider (for example, Twilio). A trunking provider is a service that converts your phone call to IP traffic. After you purchase a phone number from your SIP trunking provider, follow the instructions shown here.

Start by creating a webhook for incoming calls with the Azure OpenAI Webhook Service. We have a [REST API](../../../ai-foundry/openai/how-to/webhooks.md) that allows you to create, update, view and delete webhook endpoints.

Then, point your SIP trunk at the Azure OpenAI SIP endpoint, using the internal ID of your Azure Resource. Example: 

* Get internal ID of your Azure Open AI Resource. You can find the internal ID by clicking on the `JSON View` of your resource.
* Your project ID = `"proj_<internalId>"` This might look like `"proj_88c4a88817034471a0ba0fcae24ceb1b"`

Your sip invites use this project ID as the user: for example, `sip:proj_88c4a88817034471a0ba0fcae24ceb1b@<region>.sip.ai.azure.com;transport=tls`.

The currently supported regions are swedencentral and eastus2. 

## Handling incoming calls

When Azure OpenAI receives SIP traffic associated with your project, your webhook endpoint receives an incoming event message. The event fired for sip calls is type = `realtime.call.incoming` like the example shown here. 

```
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

### Accept the call

Use the Accept call endpoint to approve the inbound call and configure the real-time session that answers it. Send the same parameters you would send in to a create client secret. You can include any values you would use in a session.update message, but type, model and instructions are required.

> [!NOTE]
> For authorization, you can either use the api-key header or the Bearer token as shown here. Remember the model name is actually the name of your deployment. 

```
curl -X POST "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/$CALL_ID/accept" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "type": "realtime",
        "model": "gpt-realtime",
        "instructions": "You are Alex, a friendly concierge for Example Corp."
      }'
```

The request path must include

* The call_id from the realtime.call.incoming webhook event
* Authorization (or api-key) header 

The endpoint returns 200 OK once the SIP leg is ringing and the real-time session is being established.

### Reject the call

Use the Reject call endpoint to decline an invite when you don't want to handle the incoming call (for example, from an unsupported country/region code.) To control the response sent back to the carrier, supply an optional SIP status code along with the required call_id path parameter. The example here shows a request sending 486, which indicates the system is too busy to take the call.

```
curl -X POST "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/$CALL_ID/reject" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status_code": 486}'
```

If no status code is supplied, the sip server sends a status code of 603 to the customer as part of the Decline message. A successful request responds with 200 OK after OpenAI delivers the SIP response.

### Redirect the call
Transfer an active call using the Refer call endpoint. Provide the call_id and the target_uri that should be placed in the SIP Refer-To header (for example tel:+14155550123 or sip:agent@example.com).

```
curl -X POST "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/$CALL_ID/refer" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_uri": "tel:+14155550123"}'
```

OpenAI returns 200 OK once the REFER is relayed to your SIP provider. The downstream system handles the rest of the call flow for the caller.

### Monitor call events and issue session commands and updates

After you accept a call, open a WebSocket connection to the same session to stream events and issue Realtime API commands. To create a websocket to an existing call, you must use the call_id parameter. The model argument isn't used because it's configured as part of the json when accepting the call. The example here shows a common scenario, issuing a "response.create" message to instruct the Realtime API system to "answer the phone and say hello."

Here's a sample of a WebSocket request to a specific SIP call.

```
GET wss://<your azure resource name>.openai.azure.com/openai/v1/realtime?call_id={call_id}
```

**Query parameters**

|Parameter|Type|Description|
|-------|-----|-----------|
|call_id|string|Identifier from the realtime.call.incoming webhook.|

**Headers**

Authorization: Bearer $TOKEN (or api-key: your API key)

The WebSocket behaves exactly like any other Realtime API connection.

You can send messages like 'response.create' or 'session.update' to control the call, and listen for server events being returned to track progress. 

The following code snippet illustrates how a websocket connection is made. 

```
import WebSocket from "ws";

const callId = "rtc_u1_9c6574da8b8a41a18da9308f4ad974ce";
const ws = new WebSocket(`wss://<your azure resource name>.openai.azure.com/openai/v1/realtime?call_id=${callId}`, {
    headers: {
        api-key: `${process.env.OPENAI_API_KEY}`,
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

### Hang up the call

End the session with the Hang up endpoint when your application should disconnect the caller. This endpoint can be used to terminate both SIP and WebRTC real-time sessions.

```
curl -X POST "https://<your azure resource name>.openai.azure.com/openai/v1/realtime/calls/$CALL_ID/hangup" \
  -H "Authorization: Bearer $TOKEN"
The API responds with 200 OK when it starts tearing down the call.
```

## Sample webhook endpoint

The following code is a python example of a realtime.call.incoming handler. It accepts the call and then logs all the events from the Realtime API.

```
from flask import Flask, request, Response, jsonify, make_response
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

## Next steps

You now know how to get a call connected over SIP. The next step is building your real-time application prompts to server your customers.

