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


WebRTC supports browser-based or native client applications that need low-latency, real-time audio streaming with GPT-Live. Audio travels on a negotiated media track, and session events travel over a data channel.

For server-to-server integrations, see [Use GPT-Live for real-time voice](gpt-live.md) instead.

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal).
- A deployment of the `gpt-live-1` model.
- A trusted backend that holds your API key or Microsoft Entra ID credentials. GPT-Live doesn't support ephemeral client keys, so the browser never authenticates to the service directly.

## How the WebRTC connection is established

GPT-Live doesn't issue ephemeral client keys, so the browser can't create a session directly. Session initialization goes through your trusted backend, while the audio media connects directly between the browser and the service:

1. In the browser, create an `RTCPeerConnection`, add an audio transceiver and a data channel, and create an SDP offer.
1. Send the SDP offer to your backend.
1. Your backend forwards the offer to the service in a session-creation request, authenticated with your API key or Microsoft Entra ID credentials. The response contains the session ID and the SDP answer.
1. Your backend relays the SDP answer to the browser.
1. The browser applies the answer. Audio then flows directly between the browser and the service over the negotiated media track, and the data channel carries JSON events.

### Browser: create the offer

```javascript
const pc = new RTCPeerConnection();
pc.addTransceiver("audio", { direction: "sendrecv" });
const dataChannel = pc.createDataChannel("oai-events");

const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

// Send offer.sdp to your backend and receive the SDP answer.
const answer = await fetch("/live/session", {
  method: "POST",
  headers: { "Content-Type": "application/sdp" },
  body: offer.sdp,
}).then((r) => r.text());

await pc.setRemoteDescription({ type: "answer", sdp: answer });

dataChannel.addEventListener("message", ({ data }) => {
  const event = JSON.parse(data);
  console.log(event.type, event);
});
```

### Backend: create the session

Your backend sends the browser's SDP offer and the session configuration to the service, then returns the SDP answer to the browser. Keep credentials on the backend.

```javascript
const response = await fetch("https://<your-resource-name>.openai.azure.com/openai/v1/live/sessions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    session: {
      model: "gpt-live-1",
      instructions: "Be concise.",
      delegation: { type: "client" },
    },
    transport: { type: "webrtc", sdp: offerSdp },
  }),
});

const { session, transport } = await response.json();
// Save session.id for sideband control; return transport.sdp (the answer) to the browser.
```

Save `session.id` if your backend attaches a [sideband WebSocket](gpt-live.md#observe-a-session-with-a-sideband-websocket) to observe or steer the session.

## Differences from the WebSocket transport

- Don't send `session.input_audio.append` on the WebRTC data channel, and don't expect `session.output_audio.delta` there. Audio flows over the negotiated media track instead.
- Input and output media are synchronized through RTP and don't carry JSON timing fields.
- All other session events—`session.update`, the `session.instructions.append` / `session.thinking.append` / `session.commentary.append` context events, delegation events, transcripts, usage, and errors—use the same schema as WebSocket. See the [GPT-Live event API reference](../gpt-live-reference.md).

## Related content

- [Use GPT-Live for real-time voice](gpt-live.md)
- [Delegate work in GPT-Live](gpt-live-delegation.md)
