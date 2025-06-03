---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/1/2024
ms.author: eur
---

[!INCLUDE [Header](../../common/java.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites-resourcekey-endpoint.md)]

## Set up the environment

To set up your environment, [install the Speech SDK](~/articles/ai-services/speech-service/quickstarts/setup-platform.md?pivots=programming-language-java&tabs=jre). The sample in this quickstart works with the Java Runtime.

1. Install [Apache Maven](https://maven.apache.org/install.html). Then run `mvn -v` to confirm successful installation.
1. Create a *pom.xml* file in the root of your project, and copy the following code into it:

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

## Create the application

Follow these steps to create a console application for speech recognition.

1. Create a file named *SpeechSynthesis.java* in the same project root directory.
1. Copy the following code into *SpeechSynthesis.java*:

   ```java
   import com.microsoft.cognitiveservices.speech.*;
   import com.microsoft.cognitiveservices.speech.audio.*;

   import java.util.Scanner;
   import java.util.concurrent.ExecutionException;
    
   public class SpeechSynthesis {
       // This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
       private static String speechKey = System.getenv("SPEECH_KEY");
       private static String endpoint = System.getenv("ENDPOINT");
    
       public static void main(String[] args) throws InterruptedException, ExecutionException {
           SpeechConfig speechConfig = SpeechConfig.fromEndpoint(speechKey, endpoint);
           
           speechConfig.setSpeechSynthesisVoiceName("en-US-AvaMultilingualNeural"); 
    
           SpeechSynthesizer speechSynthesizer = new SpeechSynthesizer(speechConfig);
    
           // Get text from the console and synthesize to the default speaker.
           System.out.println("Enter some text that you want to speak >");
           String text = new Scanner(System.in).nextLine();
           if (text.isEmpty())
           {
               return;
           }
    
           SpeechSynthesisResult speechSynthesisResult = speechSynthesizer.SpeakTextAsync(text).get();
    
           if (speechSynthesisResult.getReason() == ResultReason.SynthesizingAudioCompleted) {
               System.out.println("Speech synthesized to speaker for text [" + text + "]");
           }
           else if (speechSynthesisResult.getReason() == ResultReason.Canceled) {
               SpeechSynthesisCancellationDetails cancellation = SpeechSynthesisCancellationDetails.fromResult(speechSynthesisResult);
               System.out.println("CANCELED: Reason=" + cancellation.getReason());
    
               if (cancellation.getReason() == CancellationReason.Error) {
                   System.out.println("CANCELED: ErrorCode=" + cancellation.getErrorCode());
                   System.out.println("CANCELED: ErrorDetails=" + cancellation.getErrorDetails());
                   System.out.println("CANCELED: Did you set the speech resource key and endpoint values?");
               }
           }
    
           System.exit(0);
       }
   }
   ```

1. To change the speech synthesis language, replace `en-US-AvaMultilingualNeural` with another [supported voice](~/articles/ai-services/speech-service/language-support.md#standard-voices).

   All neural voices are multilingual and fluent in their own language and English. For example, if the input text in English is *I'm excited to try text to speech* and you set `es-ES-ElviraNeural`, the text is spoken in English with a Spanish accent. If the voice doesn't speak the language of the input text, the Speech service doesn't output synthesized audio.

1. Run your console application to output speech synthesis to the default speaker.

   ```console
   javac SpeechSynthesis.java -cp ".;target\dependency\*"
   java -cp ".;target\dependency\*" SpeechSynthesis
   ```

   > [!IMPORTANT]
   > Make sure that you set the `SPEECH_KEY` and `ENDPOINT` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

1. Enter some text that you want to speak. For example, type *I'm excited to try text to speech*. Select the **Enter** key to hear the synthesized speech.

   ```console
   Enter some text that you want to speak >
   I'm excited to try text to speech
   ```

## Remarks

### More speech synthesis options

This quickstart uses the `SpeakTextAsync` operation to synthesize a short block of text that you enter. You can also use long-form text from a file and get finer control over voice styles, prosody, and other settings.

- See [how to synthesize speech](~/articles/ai-services/speech-service/how-to-speech-synthesis.md) and [Speech Synthesis Markup Language (SSML) overview](~/articles/ai-services/speech-service/speech-synthesis-markup.md) for information about speech synthesis from a file and finer control over voice styles, prosody, and other settings.
- See [batch synthesis API for text to speech](~/articles/ai-services/speech-service/batch-synthesis.md) for information about synthesizing long-form text to speech.

### OpenAI text to speech voices in Azure AI Speech

OpenAI text to speech voices are also supported. See [OpenAI text to speech voices in Azure AI Speech](../../../openai-voices.md) and [multilingual voices](../../../language-support.md?tabs=tts#multilingual-voices). You can replace `en-US-AvaMultilingualNeural` with a supported OpenAI voice name such as `en-US-FableMultilingualNeural`.

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
