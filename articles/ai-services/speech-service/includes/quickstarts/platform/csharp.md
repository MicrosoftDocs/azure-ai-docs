---
author: PatrickFarley
ms.service: azure-ai-speech
ms.custom: linux-related-content
ms.topic: include
ms.date: 3/12/2025
ms.author: pafarley
---

[!INCLUDE [Header](../../common/csharp.md)]

In this quickstart, you install the [Speech SDK](~/articles/ai-services/speech-service/speech-sdk.md) for C#.

## Platform requirements

[!INCLUDE [Requirements](csharp-requirements.md)]

## Install the Speech SDK for C#

The Speech SDK for C# is available as a NuGet package and implements .NET Standard 2.0. For more information, see [Microsoft.CognitiveServices.Speech](https://www.nuget.org/packages/Microsoft.CognitiveServices.Speech).

# [Terminal](#tab/dotnetcli)

The Speech SDK for C# can be installed from the .NET CLI by using the following `dotnet add` command:

```dotnetcli
dotnet add package Microsoft.CognitiveServices.Speech
```

# [PowerShell](#tab/powershell)

The Speech SDK for C# can be installed by using the following `Install-Package` command:

```powershell
Install-Package Microsoft.CognitiveServices.Speech
```

---
