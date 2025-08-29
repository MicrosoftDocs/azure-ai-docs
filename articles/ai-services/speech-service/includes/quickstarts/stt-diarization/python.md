---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/16/2025
ms.author: pafarley
---

[!INCLUDE [Header](../../common/python.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites-resourcekey-endpoint.md)]

## Set up the environment

The Speech SDK for Python is available as a [Python Package Index (PyPI) module](https://pypi.org/project/azure-cognitiveservices-speech/). The Speech SDK for Python is compatible with Windows, Linux, and macOS.

- Install the [Microsoft Visual C++ Redistributable for Visual Studio 2015, 2017, 2019, and 2022](/cpp/windows/latest-supported-vc-redist?view=msvc-170&preserve-view=true) for your platform. Restart your machine if this is your first installation of the package.
- Use the x64 target architecture on Linux.

Install a version of [Python from 3.7 or later](https://www.python.org/downloads/). First check the [SDK installation guide](../../../quickstarts/setup-platform.md?pivots=programming-language-python) for any more requirements. 

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables-resourcekey-endpoint.md)]

## Implement diarization from file with conversation transcription

Follow these steps to create a new console application.

1. Open a command prompt window where you want the new project, and create a new file named `conversation_transcription.py`.

1. Run this command to install the Speech SDK:  

    ```console
    pip install azure-cognitiveservices-speech
    ```

1. Copy the following code into `conversation_transcription.py`:

    ```Python
    import os
    import time
    import azure.cognitiveservices.speech as speechsdk

    def conversation_transcriber_recognition_canceled_cb(evt: speechsdk.SessionEventArgs):
        print('Canceled event')

    def conversation_transcriber_session_stopped_cb(evt: speechsdk.SessionEventArgs):
        print('SessionStopped event')

    def conversation_transcriber_transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        print('\nTRANSCRIBED:')
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print('\tText={}'.format(evt.result.text))
            print('\tSpeaker ID={}\n'.format(evt.result.speaker_id))
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print('\tNOMATCH: Speech could not be TRANSCRIBED: {}'.format(evt.result.no_match_details))

    def conversation_transcriber_transcribing_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        print('TRANSCRIBING:')
        print('\tText={}'.format(evt.result.text))
        print('\tSpeaker ID={}'.format(evt.result.speaker_id))

    def conversation_transcriber_session_started_cb(evt: speechsdk.SessionEventArgs):
        print('SessionStarted event')

    def recognize_from_file():
        # This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
        # Replace with your own subscription key and endpoint, the endpoint is like : "https://YourServiceRegion.api.cognitive.microsoft.com"
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), endpoint=os.environ.get('ENDPOINT'))
        speech_config.speech_recognition_language="en-US"
        speech_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceResponse_DiarizeIntermediateResults, value='true')

        audio_config = speechsdk.audio.AudioConfig(filename="katiesteve.wav")
        conversation_transcriber = speechsdk.transcription.ConversationTranscriber(speech_config=speech_config, audio_config=audio_config)

        transcribing_stop = False

        def stop_cb(evt: speechsdk.SessionEventArgs):
            #"""callback that signals to stop continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            nonlocal transcribing_stop
            transcribing_stop = True

        # Connect callbacks to the events fired by the conversation transcriber
        conversation_transcriber.transcribed.connect(conversation_transcriber_transcribed_cb)
        conversation_transcriber.transcribing.connect(conversation_transcriber_transcribing_cb)
        conversation_transcriber.session_started.connect(conversation_transcriber_session_started_cb)
        conversation_transcriber.session_stopped.connect(conversation_transcriber_session_stopped_cb)
        conversation_transcriber.canceled.connect(conversation_transcriber_recognition_canceled_cb)
        # stop transcribing on either session stopped or canceled events
        conversation_transcriber.session_stopped.connect(stop_cb)
        conversation_transcriber.canceled.connect(stop_cb)

        conversation_transcriber.start_transcribing_async()

        # Waits for completion.
        while not transcribing_stop:
            time.sleep(.5)

        conversation_transcriber.stop_transcribing_async()

    # Main

    try:
        recognize_from_file()
    except Exception as err:
        print("Encountered exception. {}".format(err))
    ```

1. Get the [sample audio file](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/audiofiles/katiesteve.wav) or use your own `.wav` file. Replace `katiesteve.wav` with the path and name of your `.wav` file.

   The application recognizes speech from multiple participants in the conversation. Your audio file should contain multiple speakers.

1. To change the speech recognition language, replace `en-US` with another [supported language](/azure/cognitive-services/speech-service/supported-languages). For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language. For details about how to identify one of multiple languages that might be spoken, see [language identification](/azure/cognitive-services/speech-service/language-identification).

1. Run your new console application to start conversation transcription:

   ```console
   python conversation_transcription.py
   ```

> [!IMPORTANT]
> Make sure that you set the `SPEECH_KEY` and `ENDPOINT` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

The transcribed conversation should be output as text:

```output
TRANSCRIBING:
        Text=good morning
        Speaker ID=Unknown
TRANSCRIBING:
        Text=good morning steve
        Speaker ID=Unknown
TRANSCRIBING:
        Text=good morning steve how are
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=good morning steve how are you doing today
        Speaker ID=Guest-1

TRANSCRIBED:
        Text=Good morning, Steve. How are you doing today?
        Speaker ID=Guest-1

TRANSCRIBING:
        Text=good morning katie
        Speaker ID=Unknown
TRANSCRIBING:
        Text=good morning katie i hope you're having a
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=good morning katie i hope you're having a great start to
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=good morning katie i hope you're having a great start to your day
        Speaker ID=Guest-2

TRANSCRIBED:
        Text=Good morning, Katie. I hope you're having a great start to your day.
        Speaker ID=Guest-2

TRANSCRIBING:
        Text=have you
        Speaker ID=Unknown
TRANSCRIBING:
        Text=have you tried
        Speaker ID=Unknown
TRANSCRIBING:
        Text=have you tried the latest
        Speaker ID=Unknown
TRANSCRIBING:
        Text=have you tried the latest real
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech service
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech service which
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech service which can
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech service which can tell you
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said        
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what   
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what in
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what in real time
        Speaker ID=Guest-1

TRANSCRIBED:
        Text=Have you tried the latest real time diarization in Microsoft Speech Service which can tell you who said what in real time?
        Speaker ID=Guest-1

TRANSCRIBING:
        Text=not yet
        Speaker ID=Unknown
TRANSCRIBING:
        Text=not yet i
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch trans
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization function
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces di
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization     
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to di
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize in real
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize in real time
        Speaker ID=Guest-2

TRANSCRIBED:
        Text=Not yet. I've been using the batch transcription with diarization functionality, but it produces diarization results after the whole audio is processed. Is the new feature able to diarize in real time?
        Speaker ID=Guest-2

TRANSCRIBING:
        Text=absolutely
        Speaker ID=Unknown
TRANSCRIBING:
        Text=absolutely i
        Speaker ID=Unknown
TRANSCRIBING:
        Text=absolutely i recom
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=absolutely i recommend
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=absolutely i recommend you give it a try
        Speaker ID=Guest-1

TRANSCRIBED:
        Text=Absolutely, I recommend you give it a try.
        Speaker ID=Guest-1

TRANSCRIBING:
        Text=that's exc
        Speaker ID=Unknown
TRANSCRIBING:
        Text=that's exciting
        Speaker ID=Unknown
TRANSCRIBING:
        Text=that's exciting let me
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=that's exciting let me try
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=that's exciting let me try it right now
        Speaker ID=Guest-2

TRANSCRIBED:
        Text=That's exciting. Let me try it right now.
        Speaker ID=Guest-2
```

Speakers are identified as Guest-1, Guest-2, and so on, depending on the number of speakers in the conversation.

> [!NOTE]
> You might see `Speaker ID=Unknown` in some of the early intermediate results when the speaker isn't yet identified. Without intermediate diarization results (if you don't set the `PropertyId.SpeechServiceResponse_DiarizeIntermediateResults` property to "true"), the speaker ID is always "Unknown."

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
