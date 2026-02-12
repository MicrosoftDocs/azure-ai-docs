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
- A [Speech resource](../../../multi-service-resource.md) in one of the supported regions. For more information about region availability, see [Speech service supported regions](../../regions.md).
- A sample `.wav` audio file to transcribe.

## Set up the environment

1. Create a new folder named `llm-speech-quickstart` and navigate to it:

    ```shell
    mkdir llm-speech-quickstart && cd llm-speech-quickstart
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

```shell
setx AZURE_SPEECH_API_KEY <your-speech-key>
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

## Transcribe audio with LLM speech

LLM speech uses the `EnhancedModeOptions` class to enable large-language-model-enhanced transcription. Enhanced mode is automatically enabled when you create an `EnhancedModeOptions` instance. The model automatically detects the language in your audio.

Create a file named `LlmSpeechQuickstart.java` in your project directory with the following code:

```java
import com.azure.ai.speech.transcription.TranscriptionClient;
import com.azure.ai.speech.transcription.TranscriptionClientBuilder;
import com.azure.ai.speech.transcription.models.AudioFileDetails;
import com.azure.ai.speech.transcription.models.EnhancedModeOptions;
import com.azure.ai.speech.transcription.models.TranscriptionOptions;
import com.azure.ai.speech.transcription.models.TranscriptionResult;
import com.azure.core.credential.KeyCredential;
import com.azure.core.util.BinaryData;
import com.azure.identity.DefaultAzureCredentialBuilder;

import java.nio.file.Files;
import java.nio.file.Paths;

public class LlmSpeechQuickstart {
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

            // Create enhanced mode options for LLM speech transcription
            // Enhanced mode is automatically enabled when you create EnhancedModeOptions
            EnhancedModeOptions enhancedModeOptions = new EnhancedModeOptions()
                .setTask("transcribe");

            // Create transcription options with enhanced mode
            TranscriptionOptions options = new TranscriptionOptions(audioFileDetails)
                .setEnhancedModeOptions(enhancedModeOptions);

            // Transcribe the audio
            TranscriptionResult result = client.transcribe(options);

            // Print result
            System.out.println("Transcription:");
            result.getCombinedPhrases().forEach(phrase ->
                System.out.println(phrase.getText())
            );

            // Print detailed phrase information
            if (result.getPhrases() != null) {
                System.out.println("\nDetailed phrases:");
                result.getPhrases().forEach(phrase ->
                    System.out.println(String.format("  [%dms] (%s): %s",
                        phrase.getOffset(),
                        phrase.getLocale(),
                        phrase.getText()))
                );
            }

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

Replace `<path-to-your-audio-file.wav>` with the path to your audio file. The service supports WAV, MP3, FLAC, OGG, and other common audio formats.


## Run the application

Run the application using Maven:

```shell
mvn compile exec:java
```

## Translate audio by using LLM speech

You can also use LLM speech to translate audio into a target language. Modify the `EnhancedModeOptions` configuration to set the task to `translate` and specify the target language.

Create a file named `LlmSpeechTranslate.java` with the following code:

```java
import com.azure.ai.speech.transcription.TranscriptionClient;
import com.azure.ai.speech.transcription.TranscriptionClientBuilder;
import com.azure.ai.speech.transcription.models.AudioFileDetails;
import com.azure.ai.speech.transcription.models.EnhancedModeOptions;
import com.azure.ai.speech.transcription.models.TranscriptionOptions;
import com.azure.ai.speech.transcription.models.TranscriptionResult;
import com.azure.core.credential.KeyCredential;
import com.azure.core.util.BinaryData;

import java.nio.file.Files;
import java.nio.file.Paths;

public class LlmSpeechTranslate {
    public static void main(String[] args) {
        try {
            // Get credentials from environment variables
            String endpoint = System.getenv("AZURE_SPEECH_ENDPOINT");
            String apiKey = System.getenv("AZURE_SPEECH_API_KEY");

            // Create client
            TranscriptionClient client = new TranscriptionClientBuilder()
                .endpoint(endpoint)
                .credential(new KeyCredential(apiKey))
                .buildClient();

            // Load audio file
            String audioFilePath = "<path-to-your-audio-file.wav>";
            byte[] audioData = Files.readAllBytes(Paths.get(audioFilePath));

            // Create audio file details
            AudioFileDetails audioFileDetails = new AudioFileDetails(BinaryData.fromBytes(audioData));

            // Create enhanced mode options for LLM speech translation
            // Translate to Korean (supported languages: en, zh, de, fr, it, ja, es, pt, ko)
            EnhancedModeOptions enhancedModeOptions = new EnhancedModeOptions()
                .setTask("translate")
                .setTargetLanguage("ko");

            // Create transcription options with enhanced mode
            TranscriptionOptions options = new TranscriptionOptions(audioFileDetails)
                .setEnhancedModeOptions(enhancedModeOptions);

            // Translate the audio
            TranscriptionResult result = client.transcribe(options);

            // Print translation result
            System.out.println("Translation:");
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


To run the translation example, update the `pom.xml` main class configuration or run:

```shell
mvn exec:java -Dexec.mainClass="LlmSpeechTranslate"
```

## Use prompt-tuning

You can provide an optional prompt to guide the output style for transcription or translation tasks.

```java
import java.util.Arrays;

// Create enhanced mode options with prompt-tuning
EnhancedModeOptions enhancedModeOptions = new EnhancedModeOptions()
    .setTask("transcribe")
    .setPrompts(Arrays.asList("Output must be in lexical format."));

// Create transcription options with enhanced mode
TranscriptionOptions options = new TranscriptionOptions(audioFileDetails)
    .setEnhancedModeOptions(enhancedModeOptions);
```

### Best practices for prompts:
- Prompts are subject to a maximum length of 4,096 characters.
- Prompts should preferably be written in English.
- Use `Output must be in lexical format.` to enforce lexical formatting instead of the default display format.
- Use `Pay attention to *phrase1*, *phrase2*, …` to improve recognition of specific phrases or acronyms.

## Clean up resources

When you finish the quickstart, delete the project folder:

```shell
rm -rf llm-speech-quickstart
```
