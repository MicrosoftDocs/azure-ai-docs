---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 8/11/2024
ms.author: eur
---

Your application must be authenticated to access Azure AI services resources. This article shows you how to use environment variables to store your credentials. You can then access the environment variables from your code to authenticate your application. For production, use a more secure way to store and access your credentials. 

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/microsoft-entra-id-akv.md)]

To set the environment variables, open a console window, and follow the instructions for your operating system and development environment.

- To set the `AZURE_OPENAI_API_KEY` environment variable, replace `your-openai-key` with one of the keys for your resource.
- To set the `AZURE_OPENAI_ENDPOINT` environment variable, replace `your-openai-endpoint` with one of the regions for your resource.
- To set the `AZURE_OPENAI_CHAT_DEPLOYMENT` environment variable, replace `your-openai-deployment-name` with one of the regions for your resource.
- To set the `SPEECH_KEY` environment variable, replace `your-speech-key` with one of the keys for your resource.
- To set the `SPEECH_REGION` environment variable, replace `your-speech-region` with one of the regions for your resource.

#### [Windows](#tab/windows)

```console
setx AZURE_OPENAI_API_KEY your-openai-key
setx AZURE_OPENAI_ENDPOINT your-openai-endpoint
setx AZURE_OPENAI_CHAT_DEPLOYMENT your-openai-deployment-name
setx SPEECH_KEY your-speech-key
setx SPEECH_REGION your-speech-region
```

> [!NOTE]
> If you only need to access the environment variable in the current running console, set the environment variable with `set` instead of `setx`.

After you add the environment variables, you might need to restart any running programs that need to read the environment variable, including the console window. For example, if Visual Studio is your editor, restart Visual Studio before running the example.

#### [Linux](#tab/linux)

```bash
export AZURE_OPENAI_API_KEY=your-openai-key
export AZURE_OPENAI_ENDPOINT=your-openai-endpoint
export AZURE_OPENAI_CHAT_DEPLOYMENT=your-openai-deployment-name
export SPEECH_KEY=your-speech-key
export SPEECH_REGION=your-speech-region
```

After you add the environment variables, run `source ~/.bashrc` from your console window to make the changes effective.

#### [macOS](#tab/macos)
##### Bash

Edit your *.bash_profile*, and add the environment variables:

```bash
export AZURE_OPENAI_API_KEY=your-openai-key
export AZURE_OPENAI_ENDPOINT=your-openai-endpoint
export AZURE_OPENAI_CHAT_DEPLOYMENT=your-openai-deployment-name # For example, "gpt-4o-mini"
export SPEECH_KEY=your-speech-key
export SPEECH_REGION=your-speech-region
```

After you add the environment variables, run `source ~/.bash_profile` from your console window to make the changes effective.

##### Xcode

For iOS and macOS development, set the environment variables in Xcode. For example, follow these steps to set the environment variable in Xcode 13.4.1.

1. Select **Product** > **Scheme** > **Edit scheme**.
1. Select **Arguments** on the **Run** (Debug Run) page.
1. Under **Environment Variables** select the plus (+) sign to add a new environment variable.
1. Enter `SPEECH_KEY` for the **Name** and enter your Speech resource key for the **Value**.

Repeat the steps to set other required environment variables.

For more configuration options, see the [Xcode documentation](https://help.apple.com/xcode/#/dev745c5c974).
***
