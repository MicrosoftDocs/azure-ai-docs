---
manager: nitinme
author: goergenj
ms.author: jagoerge
ms.service: azure-ai-speech
ms.topic: include
ms.date: 01/31/2026
---

[Reference documentation](/java/api/overview/azure/ai-speech-transcription-readme) | [Package (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-speech-transcription) | [GitHub Samples](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/transcription/azure-ai-speech-transcription/src/samples/java/com/azure/ai/speech/transcription/README.md)

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.oracle.com/java/technologies/downloads/" target="_blank">Java Development Kit (JDK) 8 or later</a>.
- <a href="https://maven.apache.org/download.cgi" target="_blank">Apache Maven</a> for dependency management and building the project.
- A [Microsoft Foundry resource](../../../multi-service-resource.md) in one of the supported regions. For more information about region availability, see [Speech service supported regions](../../regions.md).
- A sample `.wav` audio file to transcribe.

## Set up the environment

1. Create a new folder named `transcription-quickstart` and navigate to it:

    ```shell
    mkdir transcription-quickstart && cd transcription-quickstart
    ```

1. Create a `pom.xml` file in the root of your project directory with the following content:

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <modelVersion>4.0.0</modelVersion>
    
        <groupId>com.example</groupId>
        <artifactId>transcription-quickstart</artifactId>
        <version>1.0.0</version>
        <packaging>jar</packaging>
    
        <name>Speech Transcription Quickstart</name>
        <description>Quickstart sample for Azure Speech Transcription client library.</description>
        <url>https://github.com/Azure/azure-sdk-for-java</url>
    
        <properties>
            <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        </properties>
    
        <dependencies>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-ai-speech-transcription</artifactId>
                <version>1.0.0-beta.2</version>
            </dependency>
            <dependency>
                <groupId>com.azure</groupId>
                <artifactId>azure-identity</artifactId>
                <version>1.18.1</version>
            </dependency>
        </dependencies>
    
        <build>
            <sourceDirectory>.</sourceDirectory>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.11.0</version>
                    <configuration>
                        <source>1.8</source>
                        <target>1.8</target>
                    </configuration>
                </plugin>
                <plugin>
                    <groupId>org.codehaus.mojo</groupId>
                    <artifactId>exec-maven-plugin</artifactId>
                    <version>3.1.0</version>
                    <configuration>
                        <mainClass>TranscriptionQuickstart</mainClass>
                    </configuration>
                </plugin>
            </plugins>
        </build>
    </project>
    ```

    > [!NOTE]
    > The `<sourceDirectory>.</sourceDirectory>` configuration tells Maven to look for Java source files in the current directory instead of the default `src/main/java` structure. This configuration change allows for a simpler flat project structure.

1. Install the dependencies:

    ```shell
    mvn clean install
    ```

## Set environment variables

Your application must be authenticated to access the Speech service. The SDK supports both API key and Microsoft Entra ID authentication. It automatically detects which method to use based on the environment variables you set.

First, set the endpoint for your Speech resource. Replace `<your-speech-endpoint>` with your actual resource name:

# [Windows](#tab/windows)

```powershell
$env:AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
```

# [Linux](#tab/linux)

```bash
export AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
```

# [macOS](#tab/macos)

```bash
export AZURE_SPEECH_ENDPOINT="<your-speech-endpoint>"
```

---

Then, choose one of the following authentication methods:

### Option 1: API key authentication (recommended for getting started)

Set the API key environment variable:

# [Windows](#tab/windows)

```powershell
$env:AZURE_SPEECH_API_KEY="<your-speech-key>"
```

# [Linux](#tab/linux)

```bash
export AZURE_SPEECH_API_KEY=<your-speech-key>
```

# [macOS](#tab/macos)

```bash
export AZURE_SPEECH_API_KEY=<your-speech-key>
```

---

### Option 2: Microsoft Entra ID authentication (recommended for production)

Instead of setting `AZURE_SPEECH_API_KEY`, configure one of the following credential sources:

- **Azure CLI**: Run `az login` on your development machine.
- **Managed Identity**: For apps running in Azure (App Service, Azure Functions, VMs).
- **Environment Variables**: Set `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and `AZURE_CLIENT_SECRET`.
- **Visual Studio Code or IntelliJ**: Sign in through your IDE.

You also need to assign the **Cognitive Services User** role to your identity:

```azurecli
az role assignment create --assignee <your-identity> \
    --role "Cognitive Services User" \
    --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<speech-resource-name>
```

> [!NOTE]
> After setting environment variables on Windows, restart any running programs that need to read them, including the console window. On Linux or macOS, run `source ~/.bashrc` (or your equivalent shell configuration file) to make the changes effective.

## Create the application

Create a file named `TranscriptionQuickstart.java` in your project directory with the following code:

```java
import com.azure.ai.speech.transcription.TranscriptionClient;
import com.azure.ai.speech.transcription.TranscriptionClientBuilder;
import com.azure.ai.speech.transcription.models.AudioFileDetails;
import com.azure.ai.speech.transcription.models.TranscriptionOptions;
import com.azure.ai.speech.transcription.models.TranscriptionResult;
import com.azure.core.credential.KeyCredential;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class TranscriptionQuickstart {
    public static void main(String[] args) {
        try {
            // Get credentials from environment variables
            String endpoint = System.getenv("AZURE_SPEECH_ENDPOINT");
            String apiKey = System.getenv("AZURE_SPEECH_API_KEY");

            // Create client with API key or Entra ID authentication
            TranscriptionClientBuilder builder = new TranscriptionClientBuilder()
                .endpoint(endpoint);

            TranscriptionClient client;
            if (apiKey != null && !apiKey.isEmpty()) {
                // Use API key authentication
                client = builder.credential(new KeyCredential(apiKey)).buildClient();
            } else {
                // Use Entra ID authentication
                client = builder.credential(new DefaultAzureCredentialBuilder().build()).buildClient();
            }

            // Load audio file
            String audioFilePath = "<path-to-your-audio-file.wav>";
            byte[] audioData = Files.readAllBytes(Paths.get(audioFilePath));

            // Create audio file details
            AudioFileDetails audioFileDetails = new AudioFileDetails(BinaryData.fromBytes(audioData));

            // Transcribe
            TranscriptionOptions options = new TranscriptionOptions(audioFileDetails);
            TranscriptionResult result = client.transcribe(options);

            // Print result
            System.out.println("Transcription:");
            result.getCombinedPhrases().forEach(phrase ->
                System.out.println(phrase.getText())
            );

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

Replace `<path-to-your-audio-file.wav>` with the path to your audio file.


## Run the application

Run the application using Maven:

```shell
mvn compile exec:java
```




## Request configuration options

TBD 
Here are some property options to configure a transcription when you call the [Transcriptions - Transcribe](/rest/api/speechtotext/transcriptions/transcribe) operation.

| Property | Description | Required or optional |
|----------|-------------|----------------------|
| `channels` | The list of zero-based indices of the channels to be transcribed separately. Up to two channels are supported unless diarization is enabled. By default, the fast transcription API merges all input channels into a single channel and then performs the transcription. If this isn't desirable, channels can be transcribed independently without merging.<br/><br/>If you want to transcribe the channels from a stereo audio file separately, you need to specify `[0,1]`, `[0]`, or `[1]`. Otherwise, stereo audio is merged to mono and only a single channel is transcribed.<br/><br/>If the audio is stereo and diarization is enabled, then you can't set the `channels` property to `[0,1]`. The Speech service doesn't support diarization of multiple channels.<br/><br/>For mono audio, the `channels` property is ignored, and the audio is always transcribed as a single channel.| Optional |
| `diarization` | The diarization configuration. Diarization is the process of recognizing and separating multiple speakers in one audio channel. For example, specify `"diarization": {"maxSpeakers": 2, "enabled": true}`. Then the transcription file contains `speaker` entries (such as `"speaker": 0` or `"speaker": 1`) for each transcribed phrase. | Optional |
| `locales` | The list of locales that should match the expected locale of the audio data to transcribe.<br/><br/>If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency. If a single locale is specified, that locale is used for transcription.<br/><br/>But if you're not sure about the locale, you can specify multiple locales to use language identification. Language identification might be more accurate with a more precise list of candidate locales.<br/><br/>If you don't specify any locale, then the Speech service will use the latest multi-lingual model to identify the locale and transcribe continuously.<br/><br/> You can get the latest supported languages via the [Transcriptions - List Supported Locales](/rest/api/speechtotext/transcriptions/list-supported-locales) REST API (API version 2024-11-15 or later). For more information about locales, see the [Speech service language support](../../language-support.md?tabs=stt) documentation.| Optional but recommended if you know the expected locale. |
| `phraseList` |Phrase list is a list of words or phrases provided ahead of time to help improve their recognition. Adding a phrase to a phrase list increases its importance, thus making it more likely to be recognized. For example, specify `phraseList":{"phrases":["Contoso","Jessie","Rehaan"]}`. Phrase List is supported via API version 2025-10-15. For more information, see [Improve recognition accuracy with phrase list](../../improve-accuracy-phrase-list.md#implement-phrase-list-in-fast-transcription). | Optional |
| `profanityFilterMode` |Specifies how to handle profanity in recognition results. Accepted values are `None` to disable profanity filtering, `Masked` to replace profanity with asterisks, `Removed` to remove all profanity from the result, or `Tags` to add profanity tags. The default value is `Masked`. | Optional |


## Clean up resources

When you're done with the quickstart, you can delete the project folder:

```shell
rm -rf transcription-quickstart
```