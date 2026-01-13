---
title: "Quickstart: The Speech CLI - Speech service"
titleSuffix: Foundry Tools
description: In this Azure Speech in Foundry Tools CLI quickstart, you interact with speech to text, text to speech, and speech translation without having to write code.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: quickstart
ms.date: 08/07/2025
ms.author: pafarley
ms.custom: mode-api
# Customer intent: As a developer, I want to learn how to use the Azure Speech in Foundry Tools CLI to interact with speech to text, text to speech, and speech translation without writing code.
---

# Quickstart: Get started with the Azure Speech in Foundry Tools CLI

In this article, you learn how to use the Azure Speech CLI (also called SPX) to access Speech services such as speech to text, text to speech, and speech translation, without having to write any code. The Speech CLI is production ready, and you can use it to automate simple workflows in the Speech service by using `.bat` or shell scripts.

This article assumes that you have working knowledge of the Command Prompt window, terminal, or PowerShell.

> [!NOTE]
> In PowerShell, the [stop-parsing token](/powershell/module/microsoft.powershell.core/about/about_special_characters#stop-parsing-token---) (`--%`) should follow `spx`. For example, run `spx --% config @region` to view the current region config value.
 
## Download and install

[!INCLUDE [spx-setup](includes/spx-setup.md)]

## Create a resource configuration

# [Terminal](#tab/terminal)

To get started, you need an API key and region identifier (for example, `eastus`, `westus`). Create a Foundry resource for Speech on the [Azure portal](https://portal.azure.com). For more information, see [Create a Foundry resource](../../ai-services/multi-service-resource.md?pivots=azportal).

To configure your resource key and region identifier, run the following commands:  

```console
spx config @key --set SPEECH-KEY
spx config @region --set SPEECH-REGION
```

The key and region are stored for future Speech CLI commands. To view the current configuration, run the following commands:

```console
spx config @key
spx config @region
```

As needed, include the `clear` option to remove either stored value:

```console
spx config @key --clear
spx config @region --clear
```

# [PowerShell](#tab/powershell)

To get started, you need an API key and region identifier (for example, `eastus`, `westus`). Create a Foundry resource for Speech on the [Azure portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry). 

To configure your Speech resource key and region identifier, run the following commands in PowerShell: 

```powershell
spx --% config @key --set SPEECH-KEY
spx --% config @region --set SPEECH-REGION
```

The key and region are stored for future SPX commands. To view the current configuration, run the following commands:

```powershell
spx --% config @key
spx --% config @region
```

As needed, include the `clear` option to remove either stored value:

```powershell
spx --% config @key --clear
spx --% config @region --clear
```

***

## Basic usage

> [!IMPORTANT]
> When you use the Speech CLI in a container, include the `--host` option. You must also specify `--key none` to ensure that the CLI doesn't try to use a Speech key for authentication. For example, run `spx recognize --key none --host wss://localhost:5000/ --file myaudio.wav` to recognize speech from an audio file in a [speech to text container](speech-container-stt.md).

This section shows a few basic SPX commands that are often useful for first-time testing and experimentation. Run the following command to view the in-tool help:

```console
spx
```

You can search help topics by keyword. For example, to see a list of Speech CLI usage examples, run the following command:

```console
spx help find --topics "examples"
```

To see options for the `recognize` command, run the following command:

```console
spx help recognize
```

More help commands are listed in the console output. You can enter these commands to get detailed help about subcommands.

## Speech to text (speech recognition)

> [!TIP]
> If you get stuck or want to learn more about the Speech CLI recognition options, you can run ```spx help recognize```.

### Recognize speech from a microphone

1. Run the following command to start speech recognition from a microphone:

   ```console
   spx recognize --microphone --source en-US
   ```

1. Speak into the microphone, and you see transcription of your words into text in real-time. The Speech CLI stops after a period of silence, 30 seconds, or when you select **Ctrl**+**C**.

   ```output
   Connection CONNECTED...
   RECOGNIZED: I'm excited to try speech to text.
   ```

> [!NOTE]
> You can't use your computer's microphone when you run the Speech CLI within a Docker container. However, you can read from and save audio files in your local mounted directory. 

### Recognize speech from a file

To recognize speech from an audio file, use `--file` instead of `--microphone`. For compressed audio files such as MP4, install GStreamer and use `--format`. For more information, see [How to use compressed input audio](~/articles/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md).

# [Terminal](#tab/terminal)

```console
spx recognize --file YourAudioFile.wav
spx recognize --file YourAudioFile.mp4 --format any
```

# [PowerShell](#tab/powershell)

```powershell
spx recognize --file YourAudioFile.wav
spx --% recognize --file YourAudioFile.mp4 --format any
```

***

### Phrase lists
To improve recognition accuracy of specific words or utterances, use a [phrase list](~/articles/ai-services/speech-service/improve-accuracy-phrase-list.md). You include a phrase list in-line or with a text file along with the `recognize` command:

# [Terminal](#tab/terminal)

```console
spx recognize --microphone --phrases "Contoso;Jessie;Rehaan;"
spx recognize --microphone --phrases @phrases.txt
```

# [PowerShell](#tab/powershell)

```powershell
spx --% recognize --microphone --phrases "Contoso;Jessie;Rehaan;"
spx --% recognize --microphone --phrases @phrases.txt

```

***

### Language support
To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md). For example, use `es-ES` for Spanish (Spain). If you don't specify a language, the default is `en-US`.

```console
spx recognize --microphone --source es-ES
```

### Continuous recognition

For continuous recognition of audio longer than 30 seconds, append `--continuous`:

```console
spx recognize --microphone --source es-ES --continuous
```

## Text to speech (speech synthesis)

> [!TIP]
> If you get stuck or want to learn more about the Speech CLI recognition options, you can run ```spx help synthesize```.

The following command takes text as input and then outputs the synthesized speech to the current active output device (for example, your computer speakers).

```console
spx synthesize --text "Testing synthesis using the Speech CLI" --speakers
```

You can also save the synthesized output to a file. In this example, let's create a file named *my-sample.wav* in the directory where you're running the command.

```console
spx synthesize --text "Enjoy using the Speech CLI." --audio output my-sample.wav
```

These examples presume that you're testing in English. However, Speech service supports speech synthesis in many languages. You can pull down a full list of voices either by running the following command or by visiting the [language support page](./language-support.md?tabs=tts).

```console
spx synthesize --voices
```

Here's a command for using one of the voices you discovered.

```console
spx synthesize --text "Bienvenue chez moi." --voice fr-FR-AlainNeural --speakers
```


## Speech to text translation

> [!TIP]
> If you get stuck or want to learn more about the Speech CLI translation options, you can run ```spx help translate```.

### Translate speech from a microphone

1. Run the following command to start speech translation from a microphone:

   ```console
   spx translate --source en-US --target it --microphone
   ```

1. Speak into the microphone, and you see the transcription of your translated speech in real-time. The Speech CLI stops after a period of silence, 30 seconds, or when you select **Ctrl**+**C**.

   ```output
   Connection CONNECTED...
   TRANSLATING into 'it': Sono (from 'I'm')
   TRANSLATING into 'it': Sono entusiasta (from 'I'm excited to')
   TRANSLATING into 'it': Sono entusiasta di provare la parola (from 'I'm excited to try speech')
   TRANSLATED into 'it': Sono entusiasta di provare la traduzione vocale. (from 'I'm excited to try speech translation.')
   ```

> [!NOTE]
> You can't use your computer's microphone when you run the Speech CLI within a Docker container. However, you can read from and save audio files in your local mounted directory. 

### Translate speech from a file

To translate speech from an audio file, use `--file` instead of `--microphone`. For compressed audio files such as MP4, install GStreamer and use `--format`. For more information, see [How to use compressed input audio](~/articles/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md).

# [Terminal](#tab/terminal)

```console
spx translate --source en-US --target it --file YourAudioFile.wav
spx translate --source en-US --target it --file YourAudioFile.mp4 --format any
```

# [PowerShell](#tab/powershell)

```powershell
spx translate --source en-US --target it --file YourAudioFile.wav
spx translate --source en-US --target it --file YourAudioFile.mp4 --format any
```

***

### Phrase lists
To improve recognition accuracy of specific words or utterances, use a [phrase list](~/articles/ai-services/speech-service/improve-accuracy-phrase-list.md). You include a phrase list in-line or with a text file along with the `translate` command:

# [Terminal](#tab/terminal)

```console
spx translate --source en-US --target it --microphone --phrases "Contoso;Jessie;Rehaan;"
spx translate --source en-US --target it --microphone --phrases @phrases.txt
```

# [PowerShell](#tab/powershell)

```powershell
spx --% translate --source en-US --target it --microphone --phrases "Contoso;Jessie;Rehaan;"
spx --% translate --source en-US --target it --microphone --phrases @phrases.txt

```

***

### Language support
To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md?tabs=stt#supported-languages). Specify the full locale with a dash (`-`) separator. For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language.

```console
spx translate --microphone --source es-ES
```

To change the translation target language, replace `it` with another [supported language](~/articles/ai-services/speech-service/language-support.md?tabs=speech-translation#supported-languages). With few exceptions you only specify the language code that precedes the locale dash (`-`) separator. For example, use `es` for Spanish (Spain) instead of `es-ES`. The default language is `en` if you don't specify a language.

```console
spx translate --microphone --target es
```

### Multiple target languages

When you're translating into multiple languages, separate the language codes with a semicolon (`;`).

```console
spx translate --microphone --source en-US --target 'ru-RU;fr-FR;es-ES'
```

### Save translation output

If you want to save the output of your translation, use the `--output` flag. In this example, you also read from a file.

```console
spx translate --file /some/file/path/input.wav --source en-US --target ru-RU --output file /some/file/path/russian_translation.txt
```

### Continuous translation

For continuous translation of audio longer than 30 seconds, append `--continuous`:

```console
spx translate --source en-US --target it --microphone --continuous
```



## Next steps

* [Install GStreamer to use the Speech CLI with MP3 and other formats](./how-to-use-codec-compressed-audio-input-streams.md)
* [Configuration options for the Speech CLI](./spx-data-store-configuration.md)
* [Batch operations with the Speech CLI](./spx-batch-operations.md)
