---
title: Real-time synthesis for text to speech avatar - Speech service
titleSuffix: Foundry Tools
description: Learn how to use text to speech avatar with real-time synthesis.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 08/07/2025
ms.author: pafarley
author: PatrickFarley
---

# How to use text to speech avatar with real-time synthesis

This guide shows you how to use text to speech avatar with real-time synthesis. The avatar video is generated almost instantly after you enter text.

Text to speech avatar can be used in the Voice Live API to create a more personalized voice conversation. See [Voice Live API overview](../voice-live.md) and [Avatar in Voice Live sample code](../voice-live-how-to.md#azure-text-to-speech-avatar) to learn more

## Prerequisites

You need:

- **Azure subscription:** [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- **Foundry resource:** [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) in one of the supported regions. For more information about region availability, see [Text to speech avatar regions](../regions.md).

 Or, if you use Speech Studio:
- **Speech resource:** [Create a speech resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal. Select the **Standard S0** pricing tier to access avatars.
- **Speech resource key and region:** After deployment, select **Go to resource** to view and manage your keys.


## Set up environment

To use real-time avatar synthesis, install the Speech SDK for JavaScript for your webpage. See [Install the Speech SDK](/azure/ai-services/speech-service/quickstarts/setup-platform?pivots=programming-language-javascript&tabs=windows%2Cubuntu%2Cdotnetcli%2Cdotnet%2Cjre%2Cmaven%2Cbrowser%2Cmac%2Cpypi#install-the-speech-sdk-for-javascript).

Real-time avatar works on these platforms and browsers:

| Platform | Chrome | Microsoft Edge | Safari | Firefox | Opera |
|----------|--------|---------------|--------|---------|-------|
| Windows  |   Y    |      Y        |  N/A   |   Y¹    |   Y   |
| Android  |   Y    |      Y        |  N/A   |   Y¹²   |   N   |
| iOS      |   Y    |      Y        |   Y    |   Y     |   Y   |
| macOS    |   Y    |      Y        |   Y    |   Y¹    |   Y   |

¹ Doesn't work with ICE server by Communication Service, but works with Coturn.
² Background transparency doesn't work.

## Select text to speech language and voice

Speech service supports many [languages and voices](../language-support.md?tabs=tts). See the full list or try them in the [Voice Gallery](https://speech.microsoft.com/portal/voicegallery).

To match your input text and use a specific voice, set the `SpeechSynthesisLanguage` or `SpeechSynthesisVoiceName` properties in the `SpeechConfig` object:

```JavaScript
const speechConfig = SpeechSDK.SpeechConfig.fromSubscription("YourSpeechKey", "YourSpeechRegion");
// Set either the `SpeechSynthesisVoiceName` or `SpeechSynthesisLanguage`.
speechConfig.speechSynthesisLanguage = "en-US";
speechConfig.speechSynthesisVoiceName = "en-US-AvaMultilingualNeural";   
```

All neural voices are multilingual and fluent in their own language and English. For example, if you select **es-ES-ElviraNeural** and enter English text, the avatar speaks English with a Spanish accent.

If the voice doesn't support the input language, the Speech service doesn't create audio. See [Language and voice support](../language-support.md?tabs=tts) for the full list.

Default voice selection:
- If you don't set `SpeechSynthesisVoiceName` or `SpeechSynthesisLanguage`, the default voice in `en-US` is used.
- If you set only `SpeechSynthesisLanguage`, the default voice in that locale is used.
- If you set both, `SpeechSynthesisVoiceName` takes priority.
- If you use SSML to set the voice, both properties are ignored.

## Select avatar character and style

See [supported standard avatars](standard-avatars.md).

Set avatar character and style:

```JavaScript
const avatarConfig = new SpeechSDK.AvatarConfig(
    "lisa", // Set avatar character here.
    "casual-sitting", // Set avatar style here.
);  
```
Set photo avatar:

```JavaScript
const avatarConfig = new SpeechSDK.AvatarConfig(
    "anika", // Set photo avatar character here.
);
avatarConfig.photoAvatarBaseModel = "vasa-1"; // Set photo avatar base model here.
```

## Set up connection to real-time avatar

Real-time avatar uses the WebRTC protocol to stream video. Set up the connection with the avatar service using a WebRTC peer connection.

First, create a WebRTC peer connection object. WebRTC is peer-to-peer and relies on an ICE server for network relay. Speech service provides a REST API to get ICE server info. We recommend fetching ICE server details from Speech service, but you can use your own.

Sample request to fetch ICE info:

```HTTP
GET /cognitiveservices/avatar/relay/token/v1 HTTP/1.1

Host: westus2.tts.speech.microsoft.com
Ocp-Apim-Subscription-Key: YOUR_RESOURCE_KEY
```

Create the WebRTC peer connection using the ICE server URL, username, and credential from the previous response:

```JavaScript
// Create WebRTC peer connection
peerConnection = new RTCPeerConnection({
    iceServers: [{
        urls: [ "Your ICE server URL" ],
        username: "Your ICE server username",
        credential: "Your ICE server credential"
    }]
})
```

> [!NOTE]
>  The ICE server URL can start with `turn` (for example, `turn:relay.communication.microsoft.com:3478`) or `stun` (for example, `stun:relay.communication.microsoft.com:3478`). For `urls`, include only the `turn` URL.

Next, set up the video and audio player elements in the `ontrack` callback of the peer connection. This callback runs twice—once for video, once for audio. Create both player elements in the callback:

```JavaScript
// Fetch WebRTC video/audio streams and mount them to HTML video/audio player elements
peerConnection.ontrack = function (event) {
    if (event.track.kind === 'video') {
        const videoElement = document.createElement(event.track.kind)
        videoElement.id = 'videoPlayer'
        videoElement.srcObject = event.streams[0]
        videoElement.autoplay = true
    }

    if (event.track.kind === 'audio') {
        const audioElement = document.createElement(event.track.kind)
        audioElement.id = 'audioPlayer'
        audioElement.srcObject = event.streams[0]
        audioElement.autoplay = true
    }
}

// Offer to receive one video track, and one audio track
peerConnection.addTransceiver('video', { direction: 'sendrecv' })
peerConnection.addTransceiver('audio', { direction: 'sendrecv' })
```

Then, use Speech SDK to create an avatar synthesizer and connect to the avatar service with the peer connection:

```JavaScript
// Create avatar synthesizer
var avatarSynthesizer = new SpeechSDK.AvatarSynthesizer(speechConfig, avatarConfig)

// Start avatar and establish WebRTC connection
avatarSynthesizer.startAvatarAsync(peerConnection).then(
    (r) => { console.log("Avatar started.") }
).catch(
    (error) => { console.log("Avatar failed to start. Error: " + error) }
);
```

The real-time API disconnects after 5 minutes of idle or after 30 minutes of connection. To keep the avatar running longer, enable automatic reconnect. See this [JavaScript sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/js/browser/avatar/README.md) (search "auto reconnect").

## Synthesize talking avatar video from text input

After setup, the avatar video plays in your browser. The avatar blinks and moves slightly, but doesn't speak until you send text input.

Send text to the avatar synthesizer to make the avatar speak:

```JavaScript
var spokenText = "I'm excited to try text to speech avatar."
avatarSynthesizer.speakTextAsync(spokenText).then(
    (result) => {
        if (result.reason === SpeechSDK.ResultReason.SynthesizingAudioCompleted) {
            console.log("Speech and avatar synthesized to video stream.")
        } else {
            console.log("Unable to speak. Result ID: " + result.resultId)
            if (result.reason === SpeechSDK.ResultReason.Canceled) {
                let cancellationDetails = SpeechSDK.CancellationDetails.fromResult(result)
                console.log(cancellationDetails.reason)
                if (cancellationDetails.reason === SpeechSDK.CancellationReason.Error) {
                    console.log(cancellationDetails.errorDetails)
                }
            }
        }
}).catch((error) => {
    console.log(error)
    avatarSynthesizer.close()
});
```

## Close the real-time avatar connection

To avoid extra costs, close the connection when you're done:

- Closing the browser releases the WebRTC peer connection and closes the avatar connection after a few seconds.
- The connection closes automatically if the avatar is idle for 5 minutes.
- You can close the avatar connection manually:

   ```javascript
   avatarSynthesizer.close()
   ```

## Edit background

### Set background color

Set the background color of the avatar video using the `backgroundColor` property of `AvatarConfig`:

```JavaScript
const avatarConfig = new SpeechSDK.AvatarConfig(
    "lisa", // Set avatar character here.
    "casual-sitting", // Set avatar style here.
)
avatarConfig.backgroundColor = '#00FF00FF' // Set background color to green
```

> [!NOTE]
>  The color string should be in the format `#RRGGBBAA`. The alpha channel (`AA`) is ignored—transparent backgrounds aren't supported for real-time avatar.


### Set background image

Set the background image using the `backgroundImage` property of `AvatarConfig`. Upload your image to a public URL and assign it to `backgroundImage`:

```JavaScript
const avatarConfig = new SpeechSDK.AvatarConfig(
    "lisa", // Set avatar character here.
    "casual-sitting", // Set avatar style here.
)
avatarConfig.backgroundImage = "https://www.example.com/1920-1080-image.jpg" // A public accessiable URL of the image.
```

### Set background video

The API doesn't support background video directly, but you can customize the background on the client side:

- Set the background color to green (for easy matting).
- Create a canvas element the same size as the avatar video.
- For each frame, set green pixels to transparent and draw the frame to the canvas.
- Hide the original video.

This gives you a transparent avatar on a canvas. See [JavaScript sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/js/browser/avatar/js/basic.js#L142).

You can then place any dynamic content (like a video) behind the canvas.

## Crop video

The avatar video is 16:9 by default. To crop to a different aspect ratio, specify the rectangle area using the coordinates of the top-left and bottom-right corners:

```JavaScript
const videoFormat = new SpeechSDK.AvatarVideoFormat()
const topLeftCoordinate = new SpeechSDK.Coordinate(640, 0) // coordinate of top-left vertex, with X=640, Y=0
const bottomRightCoordinate = new SpeechSDK.Coordinate(1320, 1080) // coordinate of bottom-right vertex, with X=1320, Y=1080
videoFormat.setCropRange(topLeftCoordinate, bottomRightCoordinate)
const avatarConfig = new SpeechSDK.AvatarConfig(
    "lisa", // Set avatar character here.
    "casual-sitting", // Set avatar style here.
    videoFormat, // Set video format here.
)
```

For a full sample, see our [code example](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/js/browser/avatar/js/basic.js) and search for `crop`.

## Set video resolution
A 4K resolution avatar's default output resolution is 3840x2160. However, you can adjust the output resolution while maintaining the original aspect ratio to suit your requirements. For instance, setting the output resolution to 1920x1080 during streaming can reduce network bandwidth consumption. 

```JavaScript
const videoFormat = new SpeechSDK.AvatarVideoFormat();
videoFormat.width = 1920;
videoFormat.height = 1080;
```

For further details, see the [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/0d852b2115e780cfb4b65343e6c23e67953e8f4e/samples/js/browser/avatar/js/basic.js#L224C1-L225C1).

## Set avatar scene for photo avatar

For photo avatars, you can configure the scene by adjusting zoom, position, and rotation parameters. This allows you to customize how the avatar appears in the video output.

Create an `AvatarSceneConfig` object with the following parameters:
- **zoom**: A value between 0 and 1, where 1.0 represents 100% zoom (default).
- **positionX**: Horizontal position offset, ranging from -1 to 1, where 0 is centered.
- **positionY**: Vertical position offset, ranging from -1 to 1, where 0 is centered.
- **rotationX**: Rotation around the X-axis in radians.
- **rotationY**: Rotation around the Y-axis in radians.
- **rotationZ**: Rotation around the Z-axis in radians.
- **amplitude**: Amplitude of the avatar movement, ranging from 0 to 1, where values less than 1 reduce movement amplitude and 1.0 (default) means full amplitude.

Set the initial scene configuration when creating the avatar config:

```JavaScript
const avatarConfig = new SpeechSDK.AvatarConfig(
    "anika", // Set photo avatar character here.
);
avatarConfig.photoAvatarBaseModel = "vasa-1";
avatarConfig.scene = new SpeechSDK.AvatarSceneConfig(
    1.0,  // zoom: 100%
    0.0,  // positionX: centered
    0.0,  // positionY: centered
    0.0,  // rotationX: no rotation
    0.0,  // rotationY: no rotation
    0.0,  // rotationZ: no rotation
    1.0   // amplitude: full movement
);
```

You can also update the scene dynamically after the avatar session has started using the `updateSceneAsync` method:

```JavaScript
// Convert percentage and degree values to normalized values
const zoom = 0.85; // 85% zoom
const positionX = 0.1; // 10% offset to the right
const positionY = -0.05; // 5% offset upward
const rotationX = 10 * Math.PI / 180; // 10 degrees in radians
const rotationY = 0;
const rotationZ = 0;
const amplitude = 0.8; // 80% movement amplitude

const sceneConfig = new SpeechSDK.AvatarSceneConfig(
    zoom,
    positionX,
    positionY,
    rotationX,
    rotationY,
    rotationZ,
    amplitude
);
```

> [!NOTE]
> The scene configuration is only available for photo avatars. Video avatars don't support this feature.

## Code samples

Find text to speech avatar code samples in the Speech SDK GitHub repository. These samples show how to use real-time avatars in web and mobile apps:

- **Server + client**
    - [Python (server) + JavaScript (client)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/python/web/avatar)
    - [C# (server) + JavaScript (client)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/csharp/web/avatar)
    - [Node.js (server) + JavaScript (client)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/node/web/avatar)
- **Client only**
    - [JavaScript](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar)
    - [Android](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/java/android/avatar)
    - [iOS](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/swift/ios/avatar)
- **Voice Live**
    - [Node.js](https://github.com/azure-ai-foundry/voicelive-samples/tree/main/javascript/voice-live-avatar)

## Next steps

* [What is text to speech avatar](what-is-text-to-speech-avatar.md)
* [Install the Speech SDK](/azure/ai-services/speech-service/quickstarts/setup-platform?pivots=programming-language-javascript&tabs=windows%2Cubuntu%2Cdotnetcli%2Cdotnet%2Cjre%2Cmaven%2Cbrowser%2Cmac%2Cpypi#install-the-speech-sdk-for-javascript)

