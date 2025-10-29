---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/12/2025
ms.author: pafarley
---

[!INCLUDE [Introduction](intro.md)]

## Recognize speech from a microphone

Plug in and turn on your PC microphone. Turn off any apps that might also use the microphone. Some computers have a built-in microphone, whereas others require configuration of a Bluetooth device.

Now you're ready to run the Speech CLI to recognize speech from your microphone. From the command line, change to the directory that contains the Speech CLI binary file. Then run the following command:

```bash
spx recognize --microphone
```

> [!NOTE]
> The Speech CLI defaults to English. You can choose a different language [from the speech to text table](../../../../language-support.md?tabs=stt). For example, add `--source de-DE` to recognize German speech.

Speak into the microphone, and you can see transcription of your words into text in real time. The Speech CLI stops after a period of silence, or when you select **Ctrl+C**.

## Recognize speech from a file

The Speech CLI can recognize speech in many file formats and natural languages. In this example, you can use any *.wav* file (16 kHz or 8 kHz, 16-bit, and mono PCM) that contains English speech. Or if you want a quick sample, download the file [whatstheweatherlike.wav](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/csharp/sharedcontent/console/whatstheweatherlike.wav), and copy it to the same directory as the Speech CLI binary file.

Use the following command to run the Speech CLI to recognize speech found in the audio file:

```bash
spx recognize --file whatstheweatherlike.wav
```

> [!NOTE]
> The Speech CLI defaults to English. You can choose a different language [from the speech to text table](../../../../language-support.md?tabs=stt). For example, add `--source de-DE` to recognize German speech.

The Speech CLI shows a text transcription of the speech on the screen.

## Run and use a container

Speech containers provide websocket-based query endpoint APIs that are accessed through the Speech SDK and Speech CLI. By default, the Speech SDK and Speech CLI use the public Speech service. To use the container, you need to change the initialization method. Use a container host URL instead of key and region.

For more information about containers, see Host URLs in [Install and run Speech containers with Docker](../../../speech-container-howto.md#host-urls).
