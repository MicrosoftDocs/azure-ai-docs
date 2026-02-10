---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 1/29/2026
ms.author: pafarley
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/java.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites-resourcekey-endpoint.md)]

## Set up the environment

To set up your environment, [install the Speech SDK](~/articles/ai-services/speech-service/quickstarts/setup-platform.md?pivots=programming-language-java&tabs=jre). The sample in this quickstart works with the [Java Runtime](/azure/cognitive-services/speech-service/quickstarts/setup-platform?pivots=programming-language-java&tabs=jre).

1. Install [Apache Maven](https://maven.apache.org/install.html). Then run `mvn -v` to confirm successful installation.

1. Create a new `pom.xml` file in the root of your project, and copy the following into it:

    ```xml
    <project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
        <groupId>com.microsoft.cognitiveservices.speech.samples</groupId>
        <artifactId>quickstart-eclipse</artifactId>
        <version>1.0.0-SNAPSHOT</version>
        <build>
            <sourceDirectory>src</sourceDirectory>
            <plugins>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.7.0</version>
                <configuration>
                <source>1.8</source>
                <target>1.8</target>
                </configuration>
            </plugin>
            </plugins>
        </build>
        <dependencies>
            <dependency>
            <groupId>com.microsoft.cognitiveservices.speech</groupId>
            <artifactId>client-sdk</artifactId>
            <version>1.43.0</version>
            </dependency>
        </dependencies>
    </project>
    ```

1. Install the Speech SDK and dependencies.

    ```console
    mvn clean dependency:copy-dependencies
    ```

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables-resourcekey-endpoint.md)]

## Implement diarization from file with conversation transcription

Follow these steps to create a console application for conversation transcription.

1. Create a new file named `ConversationTranscription.java` in the same project root directory.

1. Copy the following code into `ConversationTranscription.java`:

    ```java
    import com.microsoft.cognitiveservices.speech.*;
    import com.microsoft.cognitiveservices.speech.audio.AudioConfig;
    import com.microsoft.cognitiveservices.speech.transcription.*;
    
    import java.net.URI;
    import java.net.URISyntaxException;
    import java.util.concurrent.Semaphore;
    import java.util.concurrent.ExecutionException;
    import java.util.concurrent.Future;
    
    public class ConversationTranscription {
        // This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
        private static String speechKey = System.getenv("SPEECH_KEY");
        private static String endpoint = System.getenv("ENDPOINT");
    
        public static void main(String[] args) throws InterruptedException, ExecutionException, URISyntaxException {
            
            SpeechConfig speechConfig = SpeechConfig.fromEndpoint(new URI(endpoint), speechKey);
            speechConfig.setSpeechRecognitionLanguage("en-US");
            AudioConfig audioInput = AudioConfig.fromWavFileInput("katiesteve.wav");
            speechConfig.setProperty(PropertyId.SpeechServiceResponse_DiarizeIntermediateResults, "true");
            
            Semaphore stopRecognitionSemaphore = new Semaphore(0);
    
            ConversationTranscriber conversationTranscriber = new ConversationTranscriber(speechConfig, audioInput);
            {
                // Subscribes to events.
                conversationTranscriber.transcribing.addEventListener((s, e) -> {
                    System.out.println("TRANSCRIBING: Text=" + e.getResult().getText() + " Speaker ID=" + e.getResult().getSpeakerId() );
                });
    
                conversationTranscriber.transcribed.addEventListener((s, e) -> {
                    if (e.getResult().getReason() == ResultReason.RecognizedSpeech) {
                        System.out.println();
                        System.out.println("TRANSCRIBED: Text=" + e.getResult().getText() + " Speaker ID=" + e.getResult().getSpeakerId() );
                        System.out.println();
                    }
                    else if (e.getResult().getReason() == ResultReason.NoMatch) {
                        System.out.println("NOMATCH: Speech could not be transcribed.");
                    }
                });
    
                conversationTranscriber.canceled.addEventListener((s, e) -> {
                    System.out.println("CANCELED: Reason=" + e.getReason());
    
                    if (e.getReason() == CancellationReason.Error) {
                        System.out.println("CANCELED: ErrorCode=" + e.getErrorCode());
                        System.out.println("CANCELED: ErrorDetails=" + e.getErrorDetails());
                        System.out.println("CANCELED: Did you update the Speech resource info?");
                    }
    
                    stopRecognitionSemaphore.release();
                });
    
                conversationTranscriber.sessionStarted.addEventListener((s, e) -> {
                    System.out.println("\n    Session started event.");
                });
    
                conversationTranscriber.sessionStopped.addEventListener((s, e) -> {
                    System.out.println("\n    Session stopped event.");
                });
    
                conversationTranscriber.startTranscribingAsync().get();
    
                // Waits for completion.
                stopRecognitionSemaphore.acquire();
    
                conversationTranscriber.stopTranscribingAsync().get();
            }
    
            speechConfig.close();
            audioInput.close();
            conversationTranscriber.close();
    
            System.exit(0);
        }
    }
    ```

1. Get the [sample audio file](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/audiofiles/katiesteve.wav) or use your own `.wav` file. Replace `katiesteve.wav` with the path and name of your `.wav` file.

   The application recognizes speech from multiple participants in the conversation. Your audio file should contain multiple speakers.

1. To change the speech recognition language, replace `en-US` with another [supported language](/azure/cognitive-services/speech-service/supported-languages). For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language. For details about how to identify one of multiple languages that might be spoken, see [language identification](/azure/cognitive-services/speech-service/language-identification).

1. Run your new console application to start conversation transcription:

   ```console
   javac ConversationTranscription.java -cp ".;target\dependency\*"
   java -cp ".;target\dependency\*" ConversationTranscription
   ```

> [!IMPORTANT]
> Make sure that you set the `SPEECH_KEY` and `ENDPOINT` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

The transcribed conversation should be output as text:

```output
TRANSCRIBING: Text=good morning Speaker ID=Unknown
TRANSCRIBING: Text=good morning steve Speaker ID=Unknown
TRANSCRIBING: Text=good morning steve how Speaker ID=Guest-1
TRANSCRIBING: Text=good morning steve how are you doing Speaker ID=Guest-1
TRANSCRIBING: Text=good morning steve how are you doing today Speaker ID=Guest-1

TRANSCRIBED: Text=Good morning, Steve. How are you doing today? Speaker ID=Guest-1

TRANSCRIBING: Text=good morning katie i hope Speaker ID=Guest-2
TRANSCRIBING: Text=good morning katie i hope you're having a Speaker ID=Guest-2
TRANSCRIBING: Text=good morning katie i hope you're having a great Speaker ID=Guest-2
TRANSCRIBING: Text=good morning katie i hope you're having a great start to Speaker ID=Guest-2
TRANSCRIBING: Text=good morning katie i hope you're having a great start to your day Speaker ID=Guest-2

TRANSCRIBED: Text=Good morning, Katie. I hope you're having a great start to your day. Speaker ID=Guest-2

TRANSCRIBING: Text=have you tried Speaker ID=Unknown
TRANSCRIBING: Text=have you tried the latest Speaker ID=Unknown
TRANSCRIBING: Text=have you tried the latest real Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what in Speaker ID=Guest-1
TRANSCRIBING: Text=have you tried the latest real time diarization in microsoft speech service which can tell you who said what in real time Speaker ID=Guest-1

TRANSCRIBED: Text=Have you tried the latest real time diarization in Microsoft Speech Service which can tell you who said what in real time? Speaker ID=Guest-1

TRANSCRIBING: Text=not yet Speaker ID=Unknown
TRANSCRIBING: Text=not yet i Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch trans Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization function Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces di Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to di Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize in real Speaker ID=Guest-2
TRANSCRIBING: Text=not yet i've been using the batch transcription with diarization functionality but it produces diarization results after the whole audio is processed is the new feature able to diarize in real time Speaker ID=Guest-2

TRANSCRIBED: Text=Not yet. I've been using the batch transcription with diarization functionality, but it produces diarization results after the whole audio is processed. Is the new feature able to diarize in real time? Speaker ID=Guest-2

TRANSCRIBING: Text=absolutely Speaker ID=Unknown
TRANSCRIBING: Text=absolutely i recom Speaker ID=Guest-1
TRANSCRIBING: Text=absolutely i recommend Speaker ID=Guest-1
TRANSCRIBING: Text=absolutely i recommend you Speaker ID=Guest-1
TRANSCRIBING: Text=absolutely i recommend you give it a try Speaker ID=Guest-1

TRANSCRIBED: Text=Absolutely, I recommend you give it a try. Speaker ID=Guest-1

TRANSCRIBING: Text=that's exc Speaker ID=Unknown
TRANSCRIBING: Text=that's exciting Speaker ID=Unknown
TRANSCRIBING: Text=that's exciting let me try Speaker ID=Guest-2
TRANSCRIBING: Text=that's exciting let me try it right now Speaker ID=Guest-2

TRANSCRIBED: Text=That's exciting. Let me try it right now. Speaker ID=Guest-2
```

Speakers are identified as Guest-1, Guest-2, and so on, depending on the number of speakers in the conversation.

> [!NOTE]
> You might see `Speaker ID=Unknown` in some of the early intermediate results when the speaker isn't yet identified. Without intermediate diarization results (if you don't set the `PropertyId.SpeechServiceResponse_DiarizeIntermediateResults` property to "true"), the speaker ID is always "Unknown."

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]

