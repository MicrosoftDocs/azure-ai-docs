---
title: "Use GPT-Live via WebRTC"
titleSuffix: Microsoft Foundry
description: Learn how to connect to GPT-Live via WebRTC for low-latency, browser-native audio streaming.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 09/04/2026
author: PatrickFarley
ms.author: pafarley
recommendations: false
ai-usage: ai-assisted
---

# Use GPT-Live via WebRTC

[!INCLUDE [preview-feature](../includes/preview-feature.md)]

WebRTC supports browser-based or native client applications that need low-latency, real-time audio streaming with GPT-Live. Audio travels on a negotiated media track, and session events travel over a data channel.

For server-to-server integrations, see [Use GPT-Live for real-time voice](gpt-live.md) instead.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal).
- A deployment of a GPT-Live model (`gpt-live-1` or `gpt-live-1-mini`).
- An ephemeral client token minted by your trusted backend. The example below uses a placeholder `token` value.

## Create a unified WebRTC session

Unified WebRTC creation sends the SDP offer and the session configuration object together in one request. The HTTP response body is the SDP answer, and the response includes a session ID header. Audio uses the negotiated media track; the data channel carries JSON events.

```javascript
const pc = new RTCPeerConnection();
pc.addTransceiver("audio", { direction: "sendrecv" });
const dataChannel = pc.createDataChannel("oai-events");

const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

const form = new FormData();
form.set("sdp", offer.sdp);
form.set("session", JSON.stringify({
  model: "gpt-live-1",
  instructions: "Be concise.",
  delegation: { type: "client" },
}));

const response = await fetch("https://<your-resource-name>.openai.azure.com/openai/v1/live", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    Accept: "application/sdp",
  },
  body: form,
});

const sessionId = response.headers.get("OpenAI-Session-ID");
await pc.setRemoteDescription({
  type: "answer",
  sdp: await response.text(),
});

dataChannel.addEventListener("message", ({ data }) => {
  const event = JSON.parse(data);
  console.log(sessionId, event.type, event);
});
```

Don't set `Content-Type` manually when using `FormData`; the client must supply the multipart boundary.

## Differences from the WebSocket transport

- Don't send `input_audio.append` on the WebRTC data channel, and don't expect `output_audio.delta` there. Audio flows over the negotiated media track instead.
- Input and output media are synchronized through RTP and don't carry JSON timing fields.
- All other session events—`session.update`, `session.context.append`, delegation events, transcripts, turns, usage, and errors—use the same schema as WebSocket. See the [GPT-Live event API reference](../gpt-live-reference.md).

## Related content

- [Use GPT-Live for real-time voice](gpt-live.md)
- [Delegate work in GPT-Live](gpt-live-delegation.md)
