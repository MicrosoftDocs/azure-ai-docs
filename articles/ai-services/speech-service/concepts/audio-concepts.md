---
title: Audio concepts in Azure Speech in Foundry Tools
titleSuffix: Foundry Tools
description: An overview of audio concepts in Azure Speech in Foundry Tools.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 11/21/2025
ms.reviewer: jagoerge
ms.author: pafarley
author: PatrickFarley
---

# Audio concepts in Azure Speech in Foundry Tools

The Speech service accepts and provides audio data in multiple formats. Use this guide to understand background information about audio concepts including sampling, formats, and codecs.

## Audio sampling

Human speech is inherently analog information, which can be approximated by converting it to a digital signal via sampling. The sampling rate is the number of times it's sampled per second, and the bit-depth is a measure of how accurate each sample is.
 
### Sample rate

A higher sampling rate more accurately reproduces higher frequency audio, such as music. Humans can typically hear sounds between 20 Hz and 20 kHz but are most sensitive up to 5 kHz. 

The sample rate needs to be twice the highest frequency of the audio. For human speech, a 16 kHz sampling rate is normally adequate, but a higher sampling rate can provide higher quality (though with larger files). The default sampling rate for both speech to text and text to speech is 16 kHz. However, 48 kHz is recommended for audiobooks. Some source audio is in 8 kHz, especially when coming from legacy telecom systems, which results in degraded quality.
 
### Bit depth
Uncompressed audio samples are represented by a number of bits that define their accuracy or resolution. For human speech, 13 bits are needed, which is rounded up to a 16-bit sample. A higher bit depth is needed for professional audio or music. Legacy telephony systems often use 8 bits with compression, but it isn't ideal for quality.
 
### Channels
The Speech service typically expects and provides a mono-channel stream. The behavior of stereo and multichannel files is API-specific. For example, the speech to text REST API splits a stereo file and generates a result for each channel. Text to speech is mono only.
 
## Audio formats and codecs
 
For the Speech service to use audio input, it needs to know how it's encoded. Also, as audio files can be relatively large, it's common to use compression to reduce their size. You can describe audio files and streams by their container format and the audio codec. Common containers are WAV or MP4 and common audio formats are PCM or MP3. 

You normally can't presume that a container uses a specific audio format. For instance, WAV files often contain PCM data but other audio formats are possible.
 
### Uncompressed audio
 
The Speech service internally works on uncompressed audio, which is encoded with Pulse Code Modulation (or PCM). This encoding means that every sample represents the amplitude of the signal. This representation is simple for processing, but not space efficient, so compression is often used for transporting audio.
 
### Lossy compressed audio
 
Lossy algorithms enable greater compression, which results in smaller files or lower bandwidth. This compression can be important on mobile connections or busy networks. A common audio format is MP3, which is an example of lossy compression. MP3 files are significantly smaller than the originals and might sound nearly identical to the original, but you can't recreate the exact source file. Lossy compression works by removing parts of the audio or approximating it. When you encode with a lossy algorithm, you trade off bandwidth for accuracy.
 
MP3 was designed for music rather than speech.

AMR and AMR-WB were designed to efficiently compress speech for mobile phones, and they don't work as well for representing music or noise.

A-Law and Mu-Law are older algorithms that compress each sample by itself. They convert a 16-bit sample to 8-bit by using a logarithmic quantization technique. Use these algorithms only to support legacy systems.
 
### Lossless compressed audio
 
Lossless compression allows you to recreate the original uncompressed file. The compressed file is typically much smaller than the original, without any loss, but the actual compression depends on the input. It achieves compression by using multiple methods to remove redundancy from the file.
 
The most common lossless compression is FLAC.

## Next step

[Use the Speech SDK for audio processing](../audio-processing-speech-sdk.md)
