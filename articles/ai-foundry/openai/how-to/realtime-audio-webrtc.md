---
title: 'Use the GPT Realtime API via WebRTC'
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Learn how to use the GPT Realtime API for speech and audio via WebRTC.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/29/2026
author: PatrickFarley
ms.author: pafarley
ms.custom: references_regions
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted

---

# Use the GPT Realtime API via WebRTC

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Azure OpenAI GPT Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. 

You can use the Realtime API via WebRTC, SIP, or WebSocket to send audio input to the model and receive audio responses in real time. Follow the instructions in this article to get started with the Realtime API via WebRTC.

In most cases, use the WebRTC API for real-time audio streaming. The WebRTC API is a web standard that enables real-time communication (RTC) between browsers and mobile applications. Here are some reasons why WebRTC is preferred for real-time audio streaming:
- **Lower latency**: WebRTC is designed to minimize delay, making it more suitable for audio and video communication where low latency is critical for maintaining quality and synchronization.
- **Media handling**: WebRTC has built-in support for audio and video codecs, providing optimized handling of media streams.
- **Error correction**: WebRTC includes mechanisms for handling packet loss and jitter, which are essential for maintaining the quality of audio streams over unpredictable networks.
- **Peer-to-peer communication**: WebRTC allows direct communication between clients, reducing the need for a central server to relay audio data, which can further reduce latency.

Use the [Realtime API via WebSockets](./realtime-audio-websockets.md) if you need to:
- Stream audio data from a server to a client.
- Send and receive data in real time between a client and server.

WebSockets aren't recommended for real-time audio streaming because they have higher latency than WebRTC.


## Supported models

You can access the GPT real-time models for global deployments in the [East US 2 and Sweden Central regions](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- `gpt-4o-mini-realtime-preview` (2024-12-17)
- `gpt-4o-realtime-preview` (2024-12-17)
- `gpt-realtime` (version 2025-08-28)
- `gpt-realtime-mini` (version 2025-10-06)
- `gpt-realtime-mini-2025-12-15` (version 2025-12-15)

You should use API version `2025-08-28` in the URL for the Realtime API. The API version is included in the sessions URL.

For more information about supported models, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md#audio-models).


> [!IMPORTANT]
> Use the GA protocol for WebRTC.
>
> You can still use the beta protocol, but we recommend that you start with the GA Protocol. If you're a current customer, plan to migrate to the GA Protocol. 
>
> This article describes how to use WebRTC with the GA Protocol. We preserve the legacy protocol documentation [here](/previous-versions/azure/foundry-models/realtime-audio-webrtc-legacy).

## Prerequisites

Before you can use GPT real-time audio, you need:

:::moniker range="foundry"
- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) in one of the [supported regions](#supported-models).
- A deployment of the `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model in a supported region as described in the [supported models](#supported-models) section in this article.
    - In the Foundry portal, load your project. Select **Build** in the upper-right menu, then select the **Models** tab on the left pane, and select **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.
:::moniker-end

:::moniker range="foundry-classic"

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](create-resource.md).
- A deployment of the `gpt-4o-realtime-preview`, `gpt-4o-mini-realtime-preview`, `gpt-realtime`, `gpt-realtime-mini`, or `gpt-realtime-mini-2025-12-15` model in a supported region as described in the [supported models](#supported-models) section in this article. You can deploy the model from the [Foundry model catalog](../../../ai-foundry/how-to/model-catalog-overview.md) or from your project in the Foundry portal.
:::moniker-end

## Set up WebRTC

To use WebRTC, you need two pieces of code:

1. A web browser application.
1. A service where your web browser can retrieve an ephemeral token.

Other options:

- Proxy the web browser's session negotiation via Session Description Protocol through the same service retrieving the ephemeral token. This scenario is more secure because the web browser doesn't have access to the ephemeral token.
- Filter the messages going to the web browser by using a query parameter.
- Create an observer WebSocket connection to listen to or record the session.

## Steps

### Step 1: Set up service to procure ephemeral token

The key to generating an ephemeral token is the REST API using 

```
url = https://{your azure resource}.openai.azure.com/openai/v1/realtime/client_secrets
```

You use this URL with either an api-key or Microsoft Entra ID token. This request retrieves an ephemeral token and sets up the session configuration you want the web browser to use, including the prompt instructions and output voice. 

Here's some sample python code for a token service. The web browser application can call this service by using the /token endpoint to retrieve an ephemeral token. This sample code uses the DefaultAzureCredential to authenticate to the RealtimeAPI generating ephemeral tokens.

```
from flask import Flask, jsonify

import os
import requests
import time
import threading

from azure.identity import DefaultAzureCredential

app = Flask(__name__)

# Session configuration
session_config = {
    "session": {
        "type": "realtime",
        "model": "<your model deployment name>",
        "instructions": "You are a helpful assistant.",
        "audio": {
            "output": {
                "voice": "marin",
            },
        },
    },
}

# Get configuration from environment variables
azure_resource = os.getenv('AZURE_RESOURCE')  # e.g., 'your-azure-resource'

# Token caching variables
cached_token = None
token_expiry = 0
token_lock = threading.Lock()

def get_bearer_token(resource_scope: str) -> str:
    """Get a bearer token using DefaultAzureCredential with caching."""
    global cached_token, token_expiry
    
    current_time = time.time()
    
    # Check if we have a valid cached token (with 5 minute buffer before expiry)
    with token_lock:
        if cached_token and current_time < (token_expiry - 300):
            return cached_token
    
    # Get a new token
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token(resource_scope)
        
        with token_lock:
            cached_token = token.token
            token_expiry = token.expires_on
            
        print(f"Acquired new bearer token, expires at: {time.ctime(token_expiry)}")
        return cached_token
        
    except Exception as e:
        print(f"Failed to acquire bearer token: {e}")
        raise

@app.route('/token', methods=['GET'])
def get_token():
    """
    An endpoint which returns the contents of a REST API request to the protected endpoint.
    Uses DefaultAzureCredential for authentication with token caching.
    """
    try:
        # Get bearer token using DefaultAzureCredential
        bearer_token = get_bearer_token("https://cognitiveservices.azure.com/.default")
        
        # Construct the Azure OpenAI endpoint URL
        url = f"https://{azure_resource}.openai.azure.com/openai/v1/realtime/client_secrets"
        
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        }
        
        # Make the request to Azure OpenAI
        response = requests.post(
            url,
            headers=headers,
            json=session_config,
            timeout=30
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Request failed with status {response.status_code}: {response.reason}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response content: {response.text}")
            
        response.raise_for_status()
        
        # Parse the JSON response and extract the ephemeral token
        data = response.json()
        ephemeral_token = data.get('value', '')
        
        if not ephemeral_token:
            print(f"No ephemeral token found in response: {data}")
            return jsonify({"error": "No ephemeral token available"}), 500
        
        # Return the ephemeral token as JSON
        return jsonify({"token": ephemeral_token})
        
    except requests.exceptions.RequestException as e:
        print(f"Token generation error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response reason: {e.response.reason}")
            print(f"Response content: {e.response.text}")
        return jsonify({"error": "Failed to generate token"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Failed to generate token"}), 500

if __name__ == '__main__':
    if not azure_resource:
        print("Error: AZURE_RESOURCE environment variable is required")
        exit(1)
    
    print(f"Starting token service for Azure resource: {azure_resource}")
    print("Using DefaultAzureCredential for authentication")
    print("Production mode - use gunicorn to run this service:")
    
    port = int(os.getenv('PORT', 5000))
    print(f"  gunicorn -w 4 -b 0.0.0.0:{port} --timeout 30 token-service:app")

```

### Step 2: Set up your browser application

Your browser application calls your token service to get the token and then initiates a webRTC connection with the RealtimeAPI. To initiate the webRTC connection, use the following URL with the ephemeral token for authentication.

```
 https://<your azure resource>.openai.azure.com/openai/v1/realtime/calls
 ```

Once connected, the browser application sends text over the data channel and audio over the media channel. Here's a sample HTML document to get you started.

```
html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Azure OpenAI Realtime Session</title>
    </head>
    <body>
        <h1>Azure OpenAI Realtime Session</h1>
        <button onclick="StartSession()">Start Session</button>
    
        <!-- Log container for API messages -->
        <div id="logContainer"></div> 
    
        <script>
           
        const AZURE_RESOURCE = "<your azure resource>"
        const WEBRTC_URL= `https://${AZURE_RESOURCE}.openai.azure.com/openai/v1/realtime/calls?webrtcfilter=on`

        async function StartSession() {
            try {

                // Call our token service to get the ephemeral key
                const tokenResponse = await fetch("/token");
                
                if (!tokenResponse.ok) {
                    throw new Error(`Token service request failed: ${tokenResponse.status}`);
                }

                const tokenData = await tokenResponse.json();
                const ephemeralKey = tokenData.token; 
                console.log("Ephemeral key received from token service");
			
                // Mask the ephemeral key in the log message.
                logMessage("Ephemeral Key Received from Token Service: " + "***");
                
                // Set up the WebRTC connection using the ephemeral key.
                init(ephemeralKey); 

            } catch (error) {
                console.error("Error fetching ephemeral key:", error);
                logMessage("Error fetching ephemeral key: " + error.message);
            }
        }            
        
        async function init(ephemeralKey) {
            logMessage("🚀 Starting WebRTC initialization...");
    
            let peerConnection = new RTCPeerConnection();
            logMessage("✅ RTCPeerConnection created");
    
            // Set up to play remote audio from the model.
            const audioElement = document.createElement('audio');
            audioElement.autoplay = true;
            document.body.appendChild(audioElement);
            logMessage("🔊 Audio element created and added to page");

            peerConnection.ontrack = (event) => {
                logMessage("🎵 Remote track received! Type: " + event.track.kind);
                logMessage("📊 Number of streams: " + event.streams.length);
                
                if (event.streams.length > 0) {
                    audioElement.srcObject = event.streams[0];
                    logMessage("✅ Audio stream assigned to audio element");
                    
                    // Add event listeners to audio element for debugging
                    audioElement.onloadstart = () => logMessage("🔄 Audio loading started");
                    audioElement.oncanplay = () => logMessage("▶️ Audio can start playing");
                    audioElement.onplay = () => logMessage("🎵 Audio playback started");
                    audioElement.onerror = (e) => logMessage("❌ Audio error: " + e.message);
                } else {
                    logMessage("⚠️ No streams in track event");
                }
            };
    
                // Set up data channel for sending and receiving events
            logMessage("🎤 Requesting microphone access...");
            try {
                const clientMedia = await navigator.mediaDevices.getUserMedia({ audio: true });
                logMessage("✅ Microphone access granted");
                
                const audioTrack = clientMedia.getAudioTracks()[0];
                logMessage("🎤 Audio track obtained: " + audioTrack.label);
                
                peerConnection.addTrack(audioTrack);
                logMessage("✅ Audio track added to peer connection");
            } catch (error) {
                logMessage("❌ Failed to get microphone access: " + error.message);
                return;
            }

            const dataChannel = peerConnection.createDataChannel('realtime-channel');
            logMessage("📡 Data channel created");
    
            dataChannel.addEventListener('open', () => {
                logMessage('✅ Data channel is open - ready to send messages');
                
                // Send client events to start the conversation
                logMessage("📝 Preparing to send text input message...");
                const event = {
                    type: "conversation.item.create",
                    item: {
                        type: "message",
                        role: "user",
                        content: [
                            {
                                type: "input_text",
                                text: "hello there! Can you give me some vacation options?",
                            },
                        ],
                    },
                };
                
                logMessage("📤 Sending conversation.item.create event...");
                logMessage("💬 Text content: " + event.item.content[0].text);
                
                try {
                    dataChannel.send(JSON.stringify(event));
                    logMessage("✅ Text input sent successfully!");
                    
                    // Now send response.create to trigger the AI response
                    const responseEvent = {
                        type: "response.create"
                    };
                    
                    logMessage("📤 Sending response.create event to trigger AI response...");
                    dataChannel.send(JSON.stringify(responseEvent));
                    logMessage("✅ Response.create sent successfully!");
                    
                } catch (error) {
                    logMessage("❌ Failed to send text input: " + error.message);
                }
            });                dataChannel.addEventListener('message', (event) => {
                    const realtimeEvent = JSON.parse(event.data); 
                    console.log(realtimeEvent); 
                    logMessage("Received server event: " + JSON.stringify(realtimeEvent, null, 2));
                    if (realtimeEvent.type === "session.update") {
                        const instructions = realtimeEvent.session.instructions;
                        logMessage("Instructions: " + instructions);
                    } else if (realtimeEvent.type === "session.error") {
                        logMessage("Error: " + realtimeEvent.error.message);
                    } else if (realtimeEvent.type === "session.end") {
                        logMessage("Session ended.");
                    }
                });
    
                dataChannel.addEventListener('close', () => {
                    logMessage('Data channel is closed');
                });
    
            // Start the session using the Session Description Protocol (SDP)
            logMessage("🤝 Creating WebRTC offer...");
            const offer = await peerConnection.createOffer();
            await peerConnection.setLocalDescription(offer);
            logMessage("✅ Local description set");

            logMessage("📡 Sending SDP offer to: " + WEBRTC_URL);
            const sdpResponse = await fetch(`${WEBRTC_URL}`, {
                method: "POST",
                body: offer.sdp,
                headers: {
                    Authorization: `Bearer ${ephemeralKey}`,
                    "Content-Type": "application/sdp",
                },
            });

            logMessage("📥 Received SDP response, status: " + sdpResponse.status);
            if (!sdpResponse.ok) {
                logMessage("❌ SDP exchange failed: " + sdpResponse.statusText);
                return;
            }

            const answerSdp = await sdpResponse.text();
            logMessage("✅ Got SDP answer, length: " + answerSdp.length + " chars");
            
            const answer = { type: "answer", sdp: answerSdp };
            await peerConnection.setRemoteDescription(answer);
            logMessage("✅ Remote description set - WebRTC connection should be establishing...");

            // Add connection state logging
            peerConnection.onconnectionstatechange = () => {
                logMessage("🔗 Connection state: " + peerConnection.connectionState);
            };
            
            peerConnection.oniceconnectionstatechange = () => {
                logMessage("🧊 ICE connection state: " + peerConnection.iceConnectionState);
            };                const button = document.createElement('button');
                button.innerText = 'Close Session';
                button.onclick = stopSession;
                document.body.appendChild(button);
    
                
    
                function stopSession() {
                    if (dataChannel) dataChannel.close();
                    if (peerConnection) peerConnection.close();
                    peerConnection = null;
                    logMessage("Session closed.");
                }
    
            }
    
            function logMessage(message) {
                const logContainer = document.getElementById("logContainer");
                const p = document.createElement("p");
                p.textContent = message;
                logContainer.appendChild(p);
            }
        </script>
    </body>
    </html>
```

In the sample, we use the query parameter webrtcfilter=on. This query parameter limits the data channel messages sent to the browser to keep your prompt instructions private. When the filter is turned on, only the following messages are returned to the browser on the data channel: 

* input_audio_buffer.speech_started
* input_audio_buffer.speech_stopped
* output_audio_buffer.started
* output_audio_buffer.stopped
* conversation.item.input_audio_transcription.completed
* conversation.item.added
* conversation.item.created
* response.output_text.delta
* response.output_text.done
* response.output_audio_transcript.delta
* response.output_audio_transcript.done

### Step 3 (optional): Create a websocket observer/controller

If you proxy the session negotiation through your service application, you can parse the Location header that's returned and use it to create a websocket connection to the WebRTC call. This connection can record the WebRTC call and even control it by issuing session.update events and other commands directly.

Here's an updated version of the token_service shown earlier, now with a /connect endpoint that you can use to both get the ephemeral token and negotiate the session initiation. It also includes a websocket connection that listens to the WebRTC session. 

```
from flask import Flask, jsonify, request
#from flask_cors import CORS

import os
import requests
import time
import threading
import asyncio
import json
import websockets

from azure.identity import DefaultAzureCredential

app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes when running locally for testing

# Session configuration
session_config = {
    "session": {
        "type": "realtime",
        "model": "<YOUR MODEL DEPLOYMENT NAME>",
        "instructions": "You are a helpful assistant.",
        "audio": {
            "output": {
                "voice": "marin",
            },
        },
    },
}

# Get configuration from environment variables
azure_resource = os.getenv('AZURE_RESOURCE')  # e.g., 'your-azure-resource'

# Token caching variables
cached_token = None
token_expiry = 0
token_lock = threading.Lock()

def get_bearer_token(resource_scope: str) -> str:
    """Get a bearer token using DefaultAzureCredential with caching."""
    global cached_token, token_expiry
    
    current_time = time.time()
    
    # Check if we have a valid cached token (with 5 minute buffer before expiry)
    with token_lock:
        if cached_token and current_time < (token_expiry - 300):
            return cached_token
    
    # Get a new token
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token(resource_scope)
        
        with token_lock:
            cached_token = token.token
            token_expiry = token.expires_on
            
        print(f"Acquired new bearer token, expires at: {time.ctime(token_expiry)}")
        return cached_token
        
    except Exception as e:
        print(f"Failed to acquire bearer token: {e}")
        raise


def get_ephemeral_token():
    """
    Generate an ephemeral token from Azure OpenAI.
    
    Returns:
        str: The ephemeral token
        
    Raises:
        Exception: If token generation fails
    """
    # Get bearer token using DefaultAzureCredential
    bearer_token = get_bearer_token("https://cognitiveservices.azure.com/.default")
    
    # Construct the Azure OpenAI endpoint URL
    url = f"https://{azure_resource}.openai.azure.com/openai/v1/realtime/client_secrets"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }
    
    # Make the request to Azure OpenAI
    response = requests.post(
        url,
        headers=headers,
        json=session_config,
        timeout=30
    )
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}: {response.reason}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response content: {response.text}")
        
    response.raise_for_status()
    
    # Parse the JSON response and extract the ephemeral token
    data = response.json()
    ephemeral_token = data.get('value', '')
    
    if not ephemeral_token:
        print(f"No ephemeral token found in response: {data}")
        raise Exception("No ephemeral token available")
    
    return ephemeral_token


def perform_sdp_negotiation(ephemeral_token, sdp_offer):
    """
    Perform SDP negotiation with the Azure OpenAI Realtime API.
    
    Args:
        ephemeral_token (str): The ephemeral token for authentication
        sdp_offer (str): The SDP offer to send
        
    Returns:
        tuple: (sdp_answer, location_header) - The SDP answer from the server and Location header for WebSocket
        
    Raises:
        Exception: If SDP negotiation fails
    """
    # Construct the realtime endpoint URL - matching the v1transceiver_test pattern
    realtime_url = f"https://{azure_resource}.openai.azure.com/openai/v1/realtime/calls"
    
    headers = {
        'Authorization': f'Bearer {ephemeral_token}',
        'Content-Type': 'application/sdp'  # Azure OpenAI expects application/sdp, not form data
    }
    
    print(f"Sending SDP offer to: {realtime_url}")
    
    # Send the SDP offer as raw body data (not form data)
    response = requests.post(realtime_url, data=sdp_offer, headers=headers, timeout=30)
    
    if response.status_code == 201:  # Changed from 200 to 201 to match the test expectation
        sdp_answer = response.text
        location_header = response.headers.get('Location', '')
        print(f"Received SDP answer: {sdp_answer[:100]}...")
        if location_header:
            print(f"Captured Location header: {location_header}")
        else:
            print("Warning: No Location header found in response")
        return sdp_answer, location_header
    else:
        error_msg = f"SDP negotiation failed: {response.status_code} - {response.text}"
        print(error_msg)
        raise Exception(error_msg)


@app.route('/token', methods=['GET'])
def get_token():
    """
    An endpoint which returns an ephemeral token for Azure OpenAI Realtime API.
    Uses DefaultAzureCredential for authentication with token caching.
    """
    try:
        ephemeral_token = get_ephemeral_token()
        
        return jsonify({
            "token": ephemeral_token,
            "endpoint": f"https://{azure_resource}.openai.azure.com",
            "deployment": "gpt-4o-realtime-preview"
        })
        
    except requests.exceptions.RequestException as e:
        print(f"Token generation error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response reason: {e.response.reason}")
            print(f"Response content: {e.response.text}")
        return jsonify({"error": "Failed to generate token"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Failed to generate token"}), 500


async def connect_websocket(location_header, bearer_token=None, api_key=None):
    """
    Connect to the WebSocket endpoint using the Location header.
    Similar to the _connect_websocket function in run_v1transceiver_test.py
    
    Args:
        location_header (str): The Location header from the SDP negotiation response
        bearer_token (str, optional): Bearer token for authentication
        api_key (str, optional): API key for authentication (fallback)
    
    Returns:
        None: Just logs messages, doesn't store them
    """
    
    # Extract call_id from location header
    # Example: /v1/realtime/calls/rtc_abc123 -> rtc_abc123
    call_id = location_header.split('/')[-1]
    print(f"Extracted call_id: {call_id}")
    
    # Construct WebSocket URL: wss://<resource>.openai.azure.com/openai/v1/realtime?call_id=<call_id>
    ws_url = f"wss://{azure_resource}.openai.azure.com/openai/v1/realtime?call_id={call_id}"
    print(f"Connecting to WebSocket: {ws_url}")
    
    message_count = 0
    
    try:
        # WebSocket headers - use proper authentication
        headers = {}
        
        if bearer_token is not None:
            print("Using Bearer token for WebSocket authentication")
            headers["Authorization"] = f"Bearer {bearer_token}"
        elif api_key is not None:
            print("Using API key for WebSocket authentication")
            headers["api-key"] = api_key
        else:
            print("Warning: No authentication provided for WebSocket")
        
        async with websockets.connect(ws_url, additional_headers=headers) as websocket:
            print("WebSocket connection established")
            
            # Listen for messages
            try:
                async for message in websocket:
                    try:
                        # Parse JSON message
                        json_data = json.loads(message)
                        msg_type = json_data.get('type', 'unknown')
                        message_count += 1
                        print(f"WebSocket [{message_count}]: {msg_type}")
                        
                        # Handle specific message types with additional details
                        if msg_type == 'response.done':
                            session_status = json_data['response'].get('status', 'unknown')
                            session_details = json_data['response'].get('details', 'No details provided')
                            print(f"  -> Response status: {session_status}, Details: {session_details}")
                            # Continue listening instead of breaking
                        elif msg_type == 'session.created':
                            session_id = json_data.get('session', {}).get('id', 'unknown')
                            print(f"  -> Session created: {session_id}")
                        elif msg_type == 'error':
                            error_message = json_data.get('error', {}).get('message', 'No error message')
                            print(f"  -> Error: {error_message}")
                        
                    except json.JSONDecodeError:
                        message_count += 1
                        print(f"WebSocket [{message_count}]: Non-JSON message: {message[:100]}...")
                    except Exception as e:
                        print(f"Error processing WebSocket message: {e}")
                        
            except websockets.exceptions.ConnectionClosed:
                print(f"WebSocket connection closed by remote (processed {message_count} messages)")
            except Exception as e:
                print(f"WebSocket message loop error: {e}")
                    
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    
    print(f"WebSocket monitoring completed. Total messages processed: {message_count}")



def start_websocket_background(location_header, bearer_token):
    """
    Start WebSocket connection in background thread to monitor/record the call.
    """
    def run_websocket():
        try:
            print(f"Starting background WebSocket monitoring for: {location_header}")
            
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Run the WebSocket connection (now just logs, doesn't return messages)
                loop.run_until_complete(
                    connect_websocket(location_header, bearer_token)
                )
                print("Background WebSocket monitoring completed.")
                
            except Exception as e:
                print(f"Background WebSocket error: {e}")
            finally:
                loop.close()
                
        except Exception as e:
            print(f"Failed to start background WebSocket: {e}")
    
    # Start the WebSocket in a background thread
    websocket_thread = threading.Thread(target=run_websocket, daemon=True)
    websocket_thread.start()
    print("Background WebSocket thread started")


@app.route('/connect', methods=['POST'])
def connect_and_negotiate():
    """
    Get token and perform SDP negotiation.
    Expects multipart form data with 'sdp' field containing the SDP offer.
    Returns SDP answer as plain text (matching the v1transceiver_test behavior).
    Automatically starts WebSocket connection in background to monitor/record the call.
    """
    try:
        # Get the SDP offer from multipart form data
        if 'sdp' not in request.form:
            return jsonify({"error": "Missing 'sdp' field in multipart form data"}), 400
        
        sdp_offer = request.form['sdp']
        print(f"Received SDP offer: {sdp_offer[:100]}...")
        
        # Get ephemeral token using shared function
        ephemeral_token = get_ephemeral_token()
        print(f"Got ephemeral token for SDP negotiation: {ephemeral_token[:20]}...")
        
        # Perform SDP negotiation using shared function
        sdp_answer, location_header = perform_sdp_negotiation(ephemeral_token, sdp_offer)
        
        # Create response headers
        response_headers = {'Content-Type': 'application/sdp'}
        
        # If we have a location header, start WebSocket connection in background to monitor/record the call
        if location_header:
            try:
                # Get a bearer token for WebSocket authentication
                bearer_token = get_bearer_token("https://cognitiveservices.azure.com/.default")
                start_websocket_background(location_header, bearer_token)
            except Exception as e:
                print(f"Failed to start background WebSocket monitoring: {e}")
                # Don't fail the main request if WebSocket setup fails
        
        # Return SDP answer as plain text, just like the v1transceiver_test expects
        return sdp_answer, 201, response_headers
            
    except Exception as e:
        error_msg = f"Error in SDP negotiation: {e}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500


if __name__ == '__main__':
    if not azure_resource:
        print("Error: AZURE_RESOURCE environment variable is required")
        exit(1)
    
    print(f"Starting token service for Azure resource: {azure_resource}")
    print("Using DefaultAzureCredential for authentication")
    
    port = int(os.getenv('PORT', 5000))
    print(f"  gunicorn -w 4 -b 0.0.0.0:{port} --timeout 30 token-service:app")

```

The associated browser changes are shown here. 

```
html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Azure OpenAI Realtime Session - Connect Endpoint</title>
    </head>
    <body>
        <h1>Azure OpenAI Realtime Session - Using /connect Endpoint</h1>
        <button onclick="StartSession()">Start Session</button>
    
        <!-- Log container for API messages -->
        <div id="logContainer"></div> 
    
        <script>
           
        const AZURE_RESOURCE = "YOUR AZURE RESOURCE NAME"

        async function StartSession() {
            try {
                logMessage("🚀 Starting session with /connect endpoint...");

                // Set up the WebRTC connection first
                const peerConnection = new RTCPeerConnection();
                logMessage("✅ RTCPeerConnection created");

                // Get microphone access and add audio track BEFORE creating offer
                logMessage("🎤 Requesting microphone access...");
                try {
                    const clientMedia = await navigator.mediaDevices.getUserMedia({ audio: true });
                    logMessage("✅ Microphone access granted");
                    
                    const audioTrack = clientMedia.getAudioTracks()[0];
                    logMessage("🎤 Audio track obtained: " + audioTrack.label);
                    
                    peerConnection.addTrack(audioTrack);
                    logMessage("✅ Audio track added to peer connection");
                } catch (error) {
                    logMessage("❌ Failed to get microphone access: " + error.message);
                    return;
                }

                // Set up audio playback
                const audioElement = document.createElement('audio');
                audioElement.autoplay = true;
                document.body.appendChild(audioElement);
                logMessage("🔊 Audio element created and added to page");

                peerConnection.ontrack = (event) => {
                    logMessage("🎵 Remote track received! Type: " + event.track.kind);
                    logMessage("📊 Number of streams: " + event.streams.length);
                    
                    if (event.streams.length > 0) {
                        audioElement.srcObject = event.streams[0];
                        logMessage("✅ Audio stream assigned to audio element");
                        
                        // Add event listeners to audio element for debugging
                        audioElement.onloadstart = () => logMessage("🔄 Audio loading started");
                        audioElement.oncanplay = () => logMessage("▶️ Audio can start playing");
                        audioElement.onplay = () => logMessage("🎵 Audio playback started");
                        audioElement.onerror = (e) => logMessage("❌ Audio error: " + e.message);
                    } else {
                        logMessage("⚠️ No streams in track event");
                    }
                };

                // Set up data channel BEFORE SDP exchange
                const dataChannel = peerConnection.createDataChannel('realtime-channel');
                logMessage("📡 Data channel created");

                dataChannel.addEventListener('open', () => {
                    logMessage('✅ Data channel is open - ready to send messages');
                    
                    // Send client events to start the conversation
                    logMessage("📝 Preparing to send text input message...");
                    const event = {
                        type: "conversation.item.create",
                        item: {
                            type: "message",
                            role: "user",
                            content: [
                                {
                                    type: "input_text",
                                    text: "hello there! Can you give me some vacation options?",
                                },
                            ],
                        },
                    };
                    
                    logMessage("📤 Sending conversation.item.create event...");
                    logMessage("💬 Text content: " + event.item.content[0].text);
                    
                    try {
                        dataChannel.send(JSON.stringify(event));
                        logMessage("✅ Text input sent successfully!");
                        
                        // Now send response.create to trigger the AI response
                        const responseEvent = {
                            type: "response.create"
                        };
                        
                        logMessage("📤 Sending response.create event to trigger AI response...");
                        dataChannel.send(JSON.stringify(responseEvent));
                        logMessage("✅ Response.create sent successfully!");
                        
                    } catch (error) {
                        logMessage("❌ Failed to send text input: " + error.message);
                    }
                });
                
                dataChannel.addEventListener('message', (event) => {
                    const realtimeEvent = JSON.parse(event.data); 
                    console.log(realtimeEvent); 
                    logMessage("📥 Received server event: " + realtimeEvent.type);
                    
                    // Log more detail for important events
                    if (realtimeEvent.type === "error") {
                        logMessage("❌ Error: " + realtimeEvent.error.message);
                    } else if (realtimeEvent.type === "session.created") {
                        logMessage("🎉 Session created successfully");
                    } else if (realtimeEvent.type === "response.output_audio_transcript.done") {
                        logMessage("📝 AI transcript complete: " + (realtimeEvent.transcript || ""));
                    } else if (realtimeEvent.type === "response.done") {
                        logMessage("✅ Response completed");
                    }
                });

                dataChannel.addEventListener('close', () => {
                    logMessage('❌ Data channel is closed');
                });
                
                dataChannel.addEventListener('error', (error) => {
                    logMessage('❌ Data channel error: ' + error);
                });

                // Add connection state logging
                peerConnection.onconnectionstatechange = () => {
                    logMessage("🔗 Connection state: " + peerConnection.connectionState);
                };
                
                peerConnection.oniceconnectionstatechange = () => {
                    logMessage("🧊 ICE connection state: " + peerConnection.iceConnectionState);
                };

                // Create offer AFTER setting up data channel
                const offer = await peerConnection.createOffer();
                await peerConnection.setLocalDescription(offer);
                logMessage("🤝 WebRTC offer created with audio track");

                // Prepare multipart form data for /connect endpoint
                const formData = new FormData();
                formData.append('sdp', offer.sdp);
                
                logMessage("📤 Sending SDP via multipart form to /connect endpoint...");

                // Call our /connect endpoint with multipart form data
                const connectResponse = await fetch("/connect", {
                    method: "POST",
                    body: formData  // FormData automatically sets correct Content-Type
                });
                
                if (!connectResponse.ok) {
                    throw new Error(`Connect service request failed: ${connectResponse.status}`);
                }

                // Get the SDP answer directly as text (not JSON)
                const answerSdp = await connectResponse.text();
                logMessage("✅ Got SDP answer from /connect endpoint, length: " + answerSdp.length + " chars");
                
                // Set up the WebRTC connection using the SDP answer
                const answer = { type: "answer", sdp: answerSdp };
                await peerConnection.setRemoteDescription(answer);
                logMessage("✅ Remote description set");
                
                // Add close session button
                const button = document.createElement('button');
                button.innerText = 'Close Session';
                button.onclick = () => stopSession(dataChannel, peerConnection);
                document.body.appendChild(button);
                logMessage("🔴 Close session button added");

                function stopSession(dataChannel, peerConnection) {
                    if (dataChannel) dataChannel.close();
                    if (peerConnection) peerConnection.close();
                    logMessage("Session closed.");
                }

            } catch (error) {
                console.error("Error in StartSession:", error);
                logMessage("Error in StartSession: " + error.message);
            }
        }

        function logMessage(message) {
            const logContainer = document.getElementById("logContainer");
            const p = document.createElement("p");
            p.textContent = message;
            logContainer.appendChild(p);
        }            
        
        async function init(peerConnection) {
            logMessage("� Continuing WebRTC setup with existing peer connection...");
    
            // Set up to play remote audio from the model.
            const audioElement = document.createElement('audio');
            audioElement.autoplay = true;
            document.body.appendChild(audioElement);
            logMessage("🔊 Audio element created and added to page");

            peerConnection.ontrack = (event) => {
                logMessage("🎵 Remote track received! Type: " + event.track.kind);
                logMessage("📊 Number of streams: " + event.streams.length);
                
                if (event.streams.length > 0) {
                    audioElement.srcObject = event.streams[0];
                    logMessage("✅ Audio stream assigned to audio element");
                    
                    // Add event listeners to audio element for debugging
                    audioElement.onloadstart = () => logMessage("🔄 Audio loading started");
                    audioElement.oncanplay = () => logMessage("▶️ Audio can start playing");
                    audioElement.onplay = () => logMessage("🎵 Audio playback started");
                    audioElement.onerror = (e) => logMessage("❌ Audio error: " + e.message);
                } else {
                    logMessage("⚠️ No streams in track event");
                }
            };
    
            const dataChannel = peerConnection.createDataChannel('realtime-channel');
            logMessage("📡 Data channel created");
    
            dataChannel.addEventListener('open', () => {
                logMessage('✅ Data channel is open - ready to send messages');
                
                // Send client events to start the conversation
                logMessage("📝 Preparing to send text input message...");
                const event = {
                    type: "conversation.item.create",
                    item: {
                        type: "message",
                        role: "user",
                        content: [
                            {
                                type: "input_text",
                                text: "hello there! Can you give me some vacation options?",
                            },
                        ],
                    },
                };
                
                logMessage("📤 Sending conversation.item.create event...");
                logMessage("💬 Text content: " + event.item.content[0].text);
                
                try {
                    dataChannel.send(JSON.stringify(event));
                    logMessage("✅ Text input sent successfully!");
                    
                    // Now send response.create to trigger the AI response
                    const responseEvent = {
                        type: "response.create"
                    };
                    
                    logMessage("📤 Sending response.create event to trigger AI response...");
                    dataChannel.send(JSON.stringify(responseEvent));
                    logMessage("✅ Response.create sent successfully!");
                    
                } catch (error) {
                    logMessage("❌ Failed to send text input: " + error.message);
                }
            });

            dataChannel.addEventListener('close', () => {
                logMessage('❌ Data channel is closed');
            });
            
            dataChannel.addEventListener('error', (error) => {
                logMessage('❌ Data channel error: ' + error);
            });            // Add connection state logging
            peerConnection.onconnectionstatechange = () => {
                logMessage("� Connection state: " + peerConnection.connectionState);
            };
            
            peerConnection.oniceconnectionstatechange = () => {
                logMessage("🧊 ICE connection state: " + peerConnection.iceConnectionState);
            };
            
            // Add close session button
            const button = document.createElement('button');
            button.innerText = 'Close Session';
            button.onclick = () => stopSession(dataChannel, peerConnection);
            document.body.appendChild(button);
            logMessage("🔴 Close session button added");

            function stopSession(dataChannel, peerConnection) {
                if (dataChannel) dataChannel.close();
                if (peerConnection) peerConnection.close();
                logMessage("Session closed.");
            }
        }
    
            function logMessage(message) {
                const logContainer = document.getElementById("logContainer");
                const p = document.createElement("p");
                p.textContent = message;
                logContainer.appendChild(p);
            }
        </script>
    </body>
</html>
```

## Related content

* Try the [real-time audio quickstart](../realtime-audio-quickstart.md)
* See the [Realtime API reference](../realtime-audio-reference.md)
* Learn more about Azure OpenAI [quotas and limits](../quotas-limits.md)
