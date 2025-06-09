---
title: Azure OpenAI Go support
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Azure OpenAI Go support
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/27/2025
---

[Source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/ai/azopenai) | [Package (pkg.go.dev)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai) | [API reference documentation](../../reference.md) | [Package reference documentation](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai)   [Samples](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#pkg-examples)


## Azure OpenAI API version support

Unlike the Azure OpenAI client libraries for Python and JavaScript, the Azure OpenAI Go library is targeted to a specific Azure OpenAI API version. Having access to the latest API versions impacts feature availability.

Current Azure OpenAI API version target: `2025-01-01-preview`

This is defined in the [**custom_client.go**](https://github.com/Azure/azure-sdk-for-go/blob/main/sdk/ai/azopenai/custom_client.go) file.

## Installation

Install the `azopenai` and `azidentity` modules with go get:

```
go get github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai

# optional
go get github.com/Azure/azure-sdk-for-go/sdk/azidentity
```

## Authentication

# [Microsoft Entra ID](#tab/secure)

The [azidentity](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/azidentity) module is used for Azure Active Directory authentication with Azure OpenAI.

```go
package main

import (
	"log"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
)

func main() {
	dac, err := azidentity.NewDefaultAzureCredential(nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	// NOTE: this constructor creates a client that connects to an Azure OpenAI endpoint.
	// To connect to the public OpenAI endpoint, use azopenai.NewClientForOpenAI
	client, err := azopenai.NewClient("https://<your-azure-openai-host>.openai.azure.com", dac, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	_ = client
}
```

For more information about Azure OpenAI keyless authentication, see [Use Azure OpenAI without keys](/azure/developer/ai/keyless-connections?tabs=go%2Cazure-cli). 

# [API Key](#tab/api-key)

```go
package main

import (
	"log"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
)

func main() {
	keyCredential := azcore.NewKeyCredential("<Azure-OpenAI-APIKey>")

	// NOTE: this constructor creates a client that connects to an Azure OpenAI endpoint.
	// To connect to the public OpenAI endpoint, use azopenai.NewClientForOpenAI
	client, err := azopenai.NewClientWithKeyCredential("https://<your-azure-openai-host>.openai.azure.com", keyCredential, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	_ = client
}
```

---

## Audio

### Client.GenerateSpeechFromText

```go
ackage main

import (
	"context"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
)

func main() {
	openAIKey := os.Getenv("OPENAI_API_KEY")

	// Ex: "https://api.openai.com/v1"
	openAIEndpoint := os.Getenv("OPENAI_ENDPOINT")

	modelDeploymentID := "tts-1"

	if openAIKey == "" || openAIEndpoint == "" || modelDeploymentID == "" {
		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
		return
	}

	keyCredential := azcore.NewKeyCredential(openAIKey)

	client, err := azopenai.NewClientForOpenAI(openAIEndpoint, keyCredential, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	audioResp, err := client.GenerateSpeechFromText(context.Background(), azopenai.SpeechGenerationOptions{
		Input:          to.Ptr("i am a computer"),
		Voice:          to.Ptr(azopenai.SpeechVoiceAlloy),
		ResponseFormat: to.Ptr(azopenai.SpeechGenerationResponseFormatFlac),
		DeploymentName: to.Ptr("tts-1"),
	}, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	defer audioResp.Body.Close()

	audioBytes, err := io.ReadAll(audioResp.Body)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	fmt.Fprintf(os.Stderr, "Got %d bytes of FLAC audio\n", len(audioBytes))

}

```

### Client.GetAudioTranscription

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
)

func main() {
	azureOpenAIKey := os.Getenv("AOAI_AUDIO_API_KEY")

	// Ex: "https://<your-azure-openai-host>.openai.azure.com"
	azureOpenAIEndpoint := os.Getenv("AOAI_AUDIO_ENDPOINT")

	modelDeploymentID := os.Getenv("AOAI_AUDIO_MODEL")

	if azureOpenAIKey == "" || azureOpenAIEndpoint == "" || modelDeploymentID == "" {
		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
		return
	}

	keyCredential := azcore.NewKeyCredential(azureOpenAIKey)

	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, keyCredential, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	mp3Bytes, err := os.ReadFile("testdata/sampledata_audiofiles_myVoiceIsMyPassportVerifyMe01.mp3")

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	resp, err := client.GetAudioTranscription(context.TODO(), azopenai.AudioTranscriptionOptions{
		File: mp3Bytes,

		// this will return _just_ the translated text. Other formats are available, which return
		// different or additional metadata. See [azopenai.AudioTranscriptionFormat] for more examples.
		ResponseFormat: to.Ptr(azopenai.AudioTranscriptionFormatText),

		DeploymentName: &modelDeploymentID,
	}, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	fmt.Fprintf(os.Stderr, "Transcribed text: %s\n", *resp.Text)

}
```

## Chat

### Client.GetChatCompletions

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
)

func main() {
	azureOpenAIKey := os.Getenv("AOAI_CHAT_COMPLETIONS_API_KEY")
	modelDeploymentID := os.Getenv("AOAI_CHAT_COMPLETIONS_MODEL")

	// Ex: "https://<your-azure-openai-host>.openai.azure.com"
	azureOpenAIEndpoint := os.Getenv("AOAI_CHAT_COMPLETIONS_ENDPOINT")

	if azureOpenAIKey == "" || modelDeploymentID == "" || azureOpenAIEndpoint == "" {
		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
		return
	}

	keyCredential := azcore.NewKeyCredential(azureOpenAIKey)

	// In Azure OpenAI you must deploy a model before you can use it in your client. For more information
	// see here: https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource
	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, keyCredential, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	// This is a conversation in progress.
	// NOTE: all messages, regardless of role, count against token usage for this API.
	messages := []azopenai.ChatRequestMessageClassification{
		// You set the tone and rules of the conversation with a prompt as the system role.
		&azopenai.ChatRequestSystemMessage{Content: azopenai.NewChatRequestSystemMessageContent("You are a helpful assistant. You will talk like a pirate.")},

		// The user asks a question
		&azopenai.ChatRequestUserMessage{Content: azopenai.NewChatRequestUserMessageContent("Can you help me?")},

		// The reply would come back from the ChatGPT. You'd add it to the conversation so we can maintain context.
		&azopenai.ChatRequestAssistantMessage{Content: azopenai.NewChatRequestAssistantMessageContent("Arrrr! Of course, me hearty! What can I do for ye?")},

		// The user answers the question based on the latest reply.
		&azopenai.ChatRequestUserMessage{Content: azopenai.NewChatRequestUserMessageContent("What's the best way to train a parrot?")},

		// from here you'd keep iterating, sending responses back from ChatGPT
	}

	gotReply := false

	resp, err := client.GetChatCompletions(context.TODO(), azopenai.ChatCompletionsOptions{
		// This is a conversation in progress.
		// NOTE: all messages count against token usage for this API.
		Messages:       messages,
		DeploymentName: &modelDeploymentID,
	}, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	for _, choice := range resp.Choices {
		gotReply = true

		if choice.ContentFilterResults != nil {
			fmt.Fprintf(os.Stderr, "Content filter results\n")

			if choice.ContentFilterResults.Error != nil {
				fmt.Fprintf(os.Stderr, "  Error:%v\n", choice.ContentFilterResults.Error)
			}

			fmt.Fprintf(os.Stderr, "  Hate: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Hate.Severity, *choice.ContentFilterResults.Hate.Filtered)
			fmt.Fprintf(os.Stderr, "  SelfHarm: sev: %v, filtered: %v\n", *choice.ContentFilterResults.SelfHarm.Severity, *choice.ContentFilterResults.SelfHarm.Filtered)
			fmt.Fprintf(os.Stderr, "  Sexual: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Sexual.Severity, *choice.ContentFilterResults.Sexual.Filtered)
			fmt.Fprintf(os.Stderr, "  Violence: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Violence.Severity, *choice.ContentFilterResults.Violence.Filtered)
		}

		if choice.Message != nil && choice.Message.Content != nil {
			fmt.Fprintf(os.Stderr, "Content[%d]: %s\n", *choice.Index, *choice.Message.Content)
		}

		if choice.FinishReason != nil {
			// this choice's conversation is complete.
			fmt.Fprintf(os.Stderr, "Finish reason[%d]: %s\n", *choice.Index, *choice.FinishReason)
		}
	}

	if gotReply {
		fmt.Fprintf(os.Stderr, "Got chat completions reply\n")
	}

}

```

### Client.GetChatCompletionsStream

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
)

func main() {
	azureOpenAIKey := os.Getenv("AOAI_CHAT_COMPLETIONS_API_KEY")
	modelDeploymentID := os.Getenv("AOAI_CHAT_COMPLETIONS_MODEL")

	// Ex: "https://<your-azure-openai-host>.openai.azure.com"
	azureOpenAIEndpoint := os.Getenv("AOAI_CHAT_COMPLETIONS_ENDPOINT")

	if azureOpenAIKey == "" || modelDeploymentID == "" || azureOpenAIEndpoint == "" {
		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
		return
	}

	keyCredential := azcore.NewKeyCredential(azureOpenAIKey)

	// In Azure OpenAI you must deploy a model before you can use it in your client. For more information
	// see here: https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource
	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, keyCredential, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	// This is a conversation in progress.
	// NOTE: all messages, regardless of role, count against token usage for this API.
	messages := []azopenai.ChatRequestMessageClassification{
		// You set the tone and rules of the conversation with a prompt as the system role.
		&azopenai.ChatRequestSystemMessage{Content: azopenai.NewChatRequestSystemMessageContent("You are a helpful assistant. You will talk like a pirate and limit your responses to 20 words or less.")},

		// The user asks a question
		&azopenai.ChatRequestUserMessage{Content: azopenai.NewChatRequestUserMessageContent("Can you help me?")},

		// The reply would come back from the ChatGPT. You'd add it to the conversation so we can maintain context.
		&azopenai.ChatRequestAssistantMessage{Content: azopenai.NewChatRequestAssistantMessageContent("Arrrr! Of course, me hearty! What can I do for ye?")},

		// The user answers the question based on the latest reply.
		&azopenai.ChatRequestUserMessage{Content: azopenai.NewChatRequestUserMessageContent("What's the best way to train a parrot?")},

		// from here you'd keep iterating, sending responses back from ChatGPT
	}

	resp, err := client.GetChatCompletionsStream(context.TODO(), azopenai.ChatCompletionsStreamOptions{
		// This is a conversation in progress.
		// NOTE: all messages count against token usage for this API.
		Messages:       messages,
		N:              to.Ptr[int32](1),
		DeploymentName: &modelDeploymentID,
	}, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	defer resp.ChatCompletionsStream.Close()

	gotReply := false

	for {
		chatCompletions, err := resp.ChatCompletionsStream.Read()

		if errors.Is(err, io.EOF) {
			break
		}

		if err != nil {
			//  TODO: Update the following line with your application specific error handling logic
			log.Printf("ERROR: %s", err)
			return
		}

		for _, choice := range chatCompletions.Choices {
			gotReply = true

			text := ""

			if choice.Delta.Content != nil {
				text = *choice.Delta.Content
			}

			role := ""

			if choice.Delta.Role != nil {
				role = string(*choice.Delta.Role)
			}

			fmt.Fprintf(os.Stderr, "Content[%d], role %q: %q\n", *choice.Index, role, text)
		}
	}

	if gotReply {
		fmt.Fprintf(os.Stderr, "Got chat completions streaming reply\n")
	}

}
```

## Embeddings

### Client.GetEmbeddings

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
)

func main() {
	azureOpenAIKey := os.Getenv("AOAI_EMBEDDINGS_API_KEY")
	modelDeploymentID := os.Getenv("AOAI_EMBEDDINGS_MODEL")

	// Ex: "https://<your-azure-openai-host>.openai.azure.com"
	azureOpenAIEndpoint := os.Getenv("AOAI_EMBEDDINGS_ENDPOINT")

	if azureOpenAIKey == "" || modelDeploymentID == "" || azureOpenAIEndpoint == "" {
		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
		return
	}

	keyCredential := azcore.NewKeyCredential(azureOpenAIKey)

	// In Azure OpenAI you must deploy a model before you can use it in your client. For more information
	// see here: https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource
	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, keyCredential, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	resp, err := client.GetEmbeddings(context.TODO(), azopenai.EmbeddingsOptions{
		Input:          []string{"Testing, testing, 1,2,3."},
		DeploymentName: &modelDeploymentID,
	}, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	for _, embed := range resp.Data {
		// embed.Embedding contains the embeddings for this input index.
		fmt.Fprintf(os.Stderr, "Got embeddings for input %d\n", *embed.Index)
	}

}
```

## Image Generation

### Client.GetImageGenerations

```go
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
)

func main() {
	azureOpenAIKey := os.Getenv("AOAI_DALLE_API_KEY")

	// Ex: "https://<your-azure-openai-host>.openai.azure.com"
	azureOpenAIEndpoint := os.Getenv("AOAI_DALLE_ENDPOINT")

	azureDeployment := os.Getenv("AOAI_DALLE_MODEL")

	if azureOpenAIKey == "" || azureOpenAIEndpoint == "" || azureDeployment == "" {
		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
		return
	}

	keyCredential := azcore.NewKeyCredential(azureOpenAIKey)

	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, keyCredential, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	resp, err := client.GetImageGenerations(context.TODO(), azopenai.ImageGenerationOptions{
		Prompt:         to.Ptr("a cat"),
		ResponseFormat: to.Ptr(azopenai.ImageGenerationResponseFormatURL),
		DeploymentName: &azureDeployment,
	}, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	for _, generatedImage := range resp.Data {
		// the underlying type for the generatedImage is dictated by the value of
		// ImageGenerationOptions.ResponseFormat. In this example we used `azopenai.ImageGenerationResponseFormatURL`,
		// so the underlying type will be ImageLocation.

		resp, err := http.Head(*generatedImage.URL)

		if err != nil {
			// TODO: Update the following line with your application specific error handling logic
			log.Printf("ERROR: %s", err)
			return
		}

		_ = resp.Body.Close()
		fmt.Fprintf(os.Stderr, "Image generated, HEAD request on URL returned %d\n", resp.StatusCode)
	}

}
```


## Completions (legacy)

### Client.GetChatCompletions

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
)

func main() {
	azureOpenAIKey := os.Getenv("AOAI_COMPLETIONS_API_KEY")
	modelDeployment := os.Getenv("AOAI_COMPLETIONS_MODEL")

	// Ex: "https://<your-azure-openai-host>.openai.azure.com"
	azureOpenAIEndpoint := os.Getenv("AOAI_COMPLETIONS_ENDPOINT")

	if azureOpenAIKey == "" || modelDeployment == "" || azureOpenAIEndpoint == "" {
		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
		return
	}

	keyCredential := azcore.NewKeyCredential(azureOpenAIKey)

	// In Azure OpenAI you must deploy a model before you can use it in your client. For more information
	// see here: https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource
	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, keyCredential, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	resp, err := client.GetCompletions(context.TODO(), azopenai.CompletionsOptions{
		Prompt:         []string{"What is Azure OpenAI, in 20 words or less"},
		MaxTokens:      to.Ptr(int32(2048)),
		Temperature:    to.Ptr(float32(0.0)),
		DeploymentName: &modelDeployment,
	}, nil)

	if err != nil {
		// TODO: Update the following line with your application specific error handling logic
		log.Printf("ERROR: %s", err)
		return
	}

	for _, choice := range resp.Choices {
		fmt.Fprintf(os.Stderr, "Result: %s\n", *choice.Text)
	}

}
```

## Error handling

All methods that send HTTP requests return `*azcore.ResponseError` when these requests fail. `ResponseError` has error details and the raw response from the service.

### Logging

This module uses the logging implementation in azcore. To turn on logging for all Azure SDK modules, set AZURE_SDK_GO_LOGGING to all. By default, the logger writes to stderr. Use the azcore/log package to control log output. For example, logging only HTTP request and response events, and printing them to stdout:

```go
import azlog "github.com/Azure/azure-sdk-for-go/sdk/azcore/log"

// Print log events to stdout
azlog.SetListener(func(cls azlog.Event, msg string) {
	fmt.Println(msg)
})

// Includes only requests and responses in credential logs
azlog.SetEvents(azlog.EventRequest, azlog.EventResponse)
```