---
title: Batch synthesis properties - Speech service
titleSuffix: Azure AI services
description: Learn about the batch synthesis properties that are available for text to speech avatar.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 9/11/2024
ms.reviewer: v-baolianzou
ms.author: eur
author: eric-urban
---

# Batch synthesis properties for text to speech avatar

Batch synthesis properties can be grouped as: avatar related properties, batch job related properties, and text to speech related properties,  which are described in the following tables.

Some properties in JSON format are required when you create a new batch synthesis job. Other properties are optional. The batch synthesis response includes other properties to provide information about the synthesis status and results. For example, the `outputs.result` property contains the location from where you can download a video file containing the avatar video. From `outputs.summary`, you can access the summary and debug details.

## Avatar properties

The following table describes the avatar properties.

| Property  | Description |
|------------------------------------------|------------------------------------------|
| avatarConfig.talkingAvatarCharacter      | The character name of the talking avatar.<br/><br/>The supported avatar characters can be found [here](avatar-gestures-with-ssml.md#supported-prebuilt-avatar-characters-styles-and-gestures).<br/><br/>This property is required.|
| avatarConfig.talkingAvatarStyle          | The style name of the talking avatar.<br/><br/>The supported avatar styles can be found [here](avatar-gestures-with-ssml.md#supported-prebuilt-avatar-characters-styles-and-gestures).<br/><br/>This property is required for prebuilt avatar, and optional for customized avatar.|
| avatarConfig.customized                  | A bool value indicating whether the avatar to be used is customized avatar or not. True for customized avatar, and false for prebuilt avatar.<br/><br/>This property is optional, and the default value is `false`.|
| avatarConfig.videoFormat                 | The format for output video file, could be mp4 or webm.<br/><br/>The `webm` format is required for transparent background.<br/><br/>This property is optional, and the default value is mp4.|
| avatarConfig.videoCodec                  | The codec for output video, could be h264, hevc, vp9 or av1.<br/><br/>Vp9 is required for transparent background. The synthesis speed will be slower with vp9 codec, as vp9 encoding is slower.<br/><br/>This property is optional, and the default value is hevc.|
| avatarConfig.bitrateKbps                 | The bitrate for output video, which is integer value, with unit kbps.<br/><br/>This property is optional, and the default value is 2000.|
| avatarConfig.videoCrop                   | This property allows you to crop the video output, which means, to output a rectangle subarea of the original video. This property has two fields, which define the top-left vertex and bottom-right vertex of the rectangle.<br/><br/>This property is optional, and the default behavior is to output the full video.|
| avatarConfig.videoCrop.topLeft           |The top-left vertex of the rectangle for video crop. This property has two fields x and y, to define the horizontal and vertical position of the vertex.<br/><br/>This property is required when properties.videoCrop is set.|
| avatarConfig.videoCrop.bottomRight       | The bottom-right vertex of the rectangle for video crop. This property has two fields x and y, to define the horizontal and vertical position of the vertex.<br/><br/>This property is required when properties.videoCrop is set.|
| avatarConfig.subtitleType                | Type of subtitle for the avatar video file could be `external_file`, `soft_embedded`, `hard_embedded`, or `none`.<br/><br/>This property is optional, and the default value is `soft_embedded`.|
| avatarConfig.backgroundImage           | Add a background image using the `avatarConfig.backgroundImage` property. The value of the property should be a URL pointing to the desired image. This property is optional. |
| avatarConfig.backgroundColor             | Background color of the avatar video, which is a string in #RRGGBBAA format. In this string: RR, GG, BB and AA mean the red, green, blue and alpha channels, with hexadecimal value range 00~FF. Alpha channel controls the transparency, with value 00 for transparent, value FF for non-transparent, and value between 00 and FF for semi-transparent.<br/><br/>This property is optional, and the default value is #FFFFFFFF (white).|
| outputs.result                           | The location of the batch synthesis result file, which is a video file containing the synthesized avatar.<br/><br/>This property is read-only.|
| properties.DurationInMilliseconds        | The video output duration in milliseconds.<br/><br/>This property is read-only.  |

## Batch synthesis job properties

The following table describes the batch synthesis job properties.

| Property | Description |
|----------|-------------|
| createdDateTime          | The date and time when the batch synthesis job was created.<br/><br/>This property is read-only.|
| description              | The description of the batch synthesis.<br/><br/>This property is optional.|
| ID                       | The batch synthesis job ID.<br/><br/>This property is read-only.|
| lastActionDateTime       | The most recent date and time when the status property value changed.<br/><br/>This property is read-only.|
| properties               | A defined set of optional batch synthesis configuration settings.  |
| properties.destinationContainerUrl | The batch synthesis results can be stored in a writable Azure container. If you don't specify a container URI with [shared access signatures (SAS)](/azure/storage/common/storage-sas-overview) token, the Speech service stores the results in a container managed by Microsoft. SAS with stored access policies isn't supported. When the synthesis job is deleted, the result data is also deleted.<br/><br/>This optional property isn't included in the response when you get the synthesis job.|
| properties.timeToLiveInHours    |A duration in hours after the synthesis job is created, when the synthesis results will be automatically deleted.  The maximum time to live is 744 hours. The date and time of automatic deletion, for synthesis jobs with a status of "Succeeded" or "Failed" is calculated as the sum of the lastActionDateTime and timeToLive properties.<br/><br/>Otherwise, you can call the [delete synthesis method](../batch-synthesis.md#delete-batch-synthesis) to remove the job sooner. |
| status                   | The batch synthesis processing status.<br/><br/>The status should progress from "NotStarted" to "Running", and finally to either "Succeeded" or "Failed".<br/><br/>This property is read-only.|


## Text to speech properties

The following table describes the text to speech properties.

| Property                 | Description |
|--------------------------|--------------------------|
| customVoices             | A custom neural voice is associated with a name and its deployment ID, like this: "customVoices": {"your-custom-voice-name": "502ac834-6537-4bc3-9fd6-140114daa66d"}<br/><br/>You can use the voice name in your `synthesisConfig.voice` when `inputKind` is set to "PlainText", or within SSML text of inputs when `inputKind` is set to "SSML".<br/><br/>This property is required to use a custom voice. If you try to use a custom voice that isn't defined here, the service returns an error.|
| inputs                   | The plain text or SSML to be synthesized.<br/><br/>When the inputKind is set to "PlainText", provide plain text as shown here: "inputs": [{"content": "The rainbow has seven colors."}]. When the inputKind is set to "SSML", provide text in the Speech Synthesis Markup Language (SSML) as shown here: "inputs": [{"content": "<speak version='\'1.0'\'' xml:lang='\'en-US'\''><voice xml:lang='\'en-US'\'' xml:gender='\'Female'\'' name='\'en-US-AvaMultilingualNeural'\''>The rainbow has seven colors.</voice></speak>"}].<br/><br/>Include up to 1,000 text objects if you want multiple video output files. Here's example input text that should be synthesized to two video output files: "inputs": [{"content": "synthesize this to a file"},{"content": "synthesize this to another file"}].<br/><br/>You don't need separate text inputs for new paragraphs. Within any of the (up to 1,000) text inputs, you can specify new paragraphs using the "\r\n" (newline) string. Here's example input text with two paragraphs that should be synthesized to the same audio output file: "inputs": [{"content": "synthesize this to a file\r\nsynthesize this to another paragraph in the same file"}]<br/><br/>This property is required when you create a new batch synthesis job. This property isn't included in the response when you get the synthesis job.|
| properties.billingDetails | The number of words that were processed and billed by customNeural versus neural (prebuilt) voices.<br/><br/>This property is read-only.|
| synthesisConfig          | The configuration settings to use for batch synthesis of plain text.<br/><br/>This property is only applicable when inputKind is set to "PlainText".|
| synthesisConfig.pitch    | The pitch of the audio output.<br/><br/>For information about the accepted values, see the [adjust prosody](../speech-synthesis-markup-voice.md#adjust-prosody) table in the Speech Synthesis Markup Language (SSML) documentation. Invalid values are ignored.<br/><br/>This optional property is only applicable when inputKind is set to "PlainText".|
| synthesisConfig.rate     | The rate of the audio output.<br/><br/>For information about the accepted values, see the [adjust prosody](../speech-synthesis-markup-voice.md#adjust-prosody) table in the Speech Synthesis Markup Language (SSML) documentation. Invalid values are ignored.<br/><br/>This optional property is only applicable when inputKind is set to "PlainText".|
| synthesisConfig.style    | For some voices, you can adjust the speaking style to express different emotions like cheerfulness, empathy, and calm. You can optimize the voice for different scenarios like customer service, newscast, and voice assistant.<br/><br/>For information about the available styles per voice, see [voice styles and roles](../language-support.md?tabs=tts#voice-styles-and-roles).<br/><br/>This optional property is only applicable when inputKind is set to "PlainText".|
| synthesisConfig.voice    | The voice that speaks the audio output.<br/><br/>For information about the available prebuilt neural voices, see [language and voice support](../language-support.md?tabs=tts). To use a custom voice, you must specify a valid custom voice and deployment ID mapping in the customVoices property.<br/><br/>This property is required when inputKind is set to "PlainText".|
| synthesisConfig.volume   | The volume of the audio output.<br/><br/>For information about the accepted values, see the [adjust prosody](../speech-synthesis-markup-voice.md#adjust-prosody) table in the Speech Synthesis Markup Language (SSML) documentation. Invalid values are ignored.<br/><br/>This optional property is only applicable when inputKind is set to "PlainText".|
| inputKind                 | Indicates whether the inputs text property should be plain text or SSML. The possible case-insensitive values are "PlainText" and "SSML". When the inputKind is set to "PlainText", you must also set the synthesisConfig voice property.<br/><br/>This property is required.|

## How to edit the background

The avatar batch synthesis API currently doesn't support setting background videos; it only supports static background images. However, if you want to add a background for your video during post-production, you can generate videos with a transparent background.

To set a static background image, use the `avatarConfig.backgroundImage` property and specify a URL pointing to the desired image. Additionally, you can set the background color of the avatar video using the `avatarConfig.backgroundColor` property.

To generate a transparent background video, you must set the following properties to the required values in the batch synthesis request:

| Property                | Required values for background transparency |
|-------------------------|---------------------------------------------|
| properties.videoFormat  | webm                                        |
| properties.videoCodec   | vp9                                         |
| properties.backgroundColor | #00000000 (or `transparent`)               |

Clipchamp is one example of a video editing tool that supports the transparent background video generated by the batch synthesis API.

Some video editing software doesn't support the `webm` format directly and only supports `.mov` format transparent background video input like Adobe Premiere Pro. In such cases, you first need to convert the video format from `webm` to `.mov` with a tool such as FFMPEG.

**FFMPEG command line:**

```bash
ffmpeg -vcodec libvpx-vp9 -i <input.webm> -vcodec png -pix_fmt rgba metadata:s:v:0 alpha_mode="1" <output.mov>
```

FFMPEG can be downloaded from [ffmpeg.org](https://ffmpeg.org/download.html). Replace `<input.webm>` and `<output.mov>` with your local path and filename in the command line.

## Next steps

* [Create an avatar with batch synthesis](./batch-synthesis-avatar.md)
* [What is text to speech avatar](what-is-text-to-speech-avatar.md)
