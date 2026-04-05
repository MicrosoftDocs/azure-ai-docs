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

Use `TranscriptionOptions` to customize transcription behavior. The following sections describe each supported configuration and show how to apply it.

### Multi-language detection

When you don't specify a locale, the service automatically detects and transcribes all languages present in the audio. Each returned phrase includes a `locale` field that identifies the detected language.

```java
// No locale specified — service auto-detects all languages in the audio
TranscriptionOptions options = new TranscriptionOptions(audioFileDetails);
TranscriptionResult result = client.transcribe(options);

// Each phrase reports the detected locale
result.getPhrases().forEach(phrase ->
    System.out.println(phrase.getLocale() + ": " + phrase.getText())
);
```

> [!NOTE]
> When no locale is specified, the `locale` field on individual phrases might
> not always accurately reflect the exact language of that specific phrase.
> For highest accuracy, specify the expected locale when you know it.

Reference: [`TranscriptionOptions`](/java/api/com.azure.ai.speech.transcription.models.transcriptionoptions), [`TranscribedPhrase.getLocale()`](/java/api/com.azure.ai.speech.transcription.models.transcribedphrase)

### Speaker diarization

Diarization detects and labels different speakers in a single audio channel. Use `TranscriptionDiarizationOptions` to enable it and set the maximum expected number of speakers (2–36). Each phrase in the result includes a `speaker` identifier.

```java
import com.azure.ai.speech.transcription.models.TranscriptionDiarizationOptions;

// Configure diarization with a maximum of 5 speakers
TranscriptionDiarizationOptions diarizationOptions =
    new TranscriptionDiarizationOptions()
        .setMaxSpeakers(5);

TranscriptionOptions options = new TranscriptionOptions(audioFileDetails)
    .setDiarizationOptions(diarizationOptions);

TranscriptionResult result = client.transcribe(options);

// Each phrase includes the detected speaker ID
result.getPhrases().forEach(phrase ->
    System.out.println(
        "[Speaker " + phrase.getSpeaker() + "] " + phrase.getText()
    )
);
```

> [!NOTE]
> Diarization is only supported on single-channel (mono) audio. If your audio
> is stereo, don't set the `channels` property to `[0,1]` when diarization
> is enabled.

Reference: [`TranscriptionDiarizationOptions`](/java/api/com.azure.ai.speech.transcription.models.transcriptiondiarizationoptions), [`TranscriptionOptions.setDiarizationOptions()`](/java/api/com.azure.ai.speech.transcription.models.transcriptionoptions), [`TranscribedPhrase.getSpeaker()`](/java/api/com.azure.ai.speech.transcription.models.transcribedphrase)

### Phrase list

A phrase list boosts recognition accuracy for domain-specific terms, proper nouns, and uncommon words. Phrases you add are weighted more heavily by the recognizer, making them more likely to be transcribed correctly.

```java
import com.azure.ai.speech.transcription.models.PhraseListOptions;
import java.util.Arrays;

// Add terms that appear in your audio to improve recognition
PhraseListOptions phraseListOptions = new PhraseListOptions()
    .setPhrases(Arrays.asList("Contoso", "Jessie", "Rehaan"));

TranscriptionOptions options = new TranscriptionOptions(audioFileDetails)
    .setPhraseListOptions(phraseListOptions);

TranscriptionResult result = client.transcribe(options);

result.getCombinedPhrases().forEach(phrase ->
    System.out.println(phrase.getText())
);
```

For more information, see [Improve recognition accuracy with phrase list](../../improve-accuracy-phrase-list.md#implement-phrase-list-in-fast-transcription).

Reference: [`PhraseListOptions`](/java/api/com.azure.ai.speech.transcription.models.phraselistoptions), [`TranscriptionOptions.setPhraseListOptions()`](/java/api/com.azure.ai.speech.transcription.models.transcriptionoptions)

### Profanity filtering

Control how profanity appears in the transcription output using `ProfanityFilterMode`. The following modes are available:

| Mode | Behavior |
|------|----------|
| `NONE` | Profanity passes through unchanged. |
| `MASKED` | Profanity is replaced with asterisks (default). |
| `REMOVED` | Profanity is removed from the output entirely. |
| `TAGS` | Profanity is wrapped in XML tags. |

```java
import com.azure.ai.speech.transcription.models.ProfanityFilterMode;

TranscriptionOptions options = new TranscriptionOptions(audioFileDetails)
    .setProfanityFilterMode(ProfanityFilterMode.MASKED);

TranscriptionResult result = client.transcribe(options);

System.out.println(result.getCombinedPhrases().get(0).getText());
```

Reference: [`ProfanityFilterMode`](/java/api/com.azure.ai.speech.transcription.models.profanityfiltermode), [`TranscriptionOptions.setProfanityFilterMode()`](/java/api/com.azure.ai.speech.transcription.models.transcriptionoptions)


## Clean up resources

When you're done with the quickstart, you can delete the project folder:

```shell
rm -rf transcription-quickstart
```