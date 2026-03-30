---
title: "How to use JSON mode with Azure OpenAI in Microsoft Foundry Models"
description: "Learn how to improve your chat completions with Azure OpenAI JSON mode"
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 12/6/2025
author: mrbullwinkle
ms.author: mbullwin
recommendations: false
ai-usage: ai-assisted

ms.custom:
  - classic-and-new
  - doc-kit-assisted
---

# Learn how to use JSON mode

[!INCLUDE [json-mode 1](../includes/how-to-json-mode-1.md)]

## Example

Before you run the examples:

- Replace `YOUR-RESOURCE-NAME` with your Azure OpenAI resource name.
- Replace `YOUR-MODEL_DEPLOYMENT_NAME` with the name of your model deployment.

The examples below show JSON mode using the Python and .NET SDKs, and PowerShell for direct REST interaction.

# [Python](#tab/python)

```python
import os
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.chat.completions.create(
  model="YOUR-MODEL_DEPLOYMENT_NAME", # Model = should match the deployment name you chose for your model deployment
  response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
    {"role": "user", "content": "Who won the world series in 2020?"}
  ]
)
print(response.choices[0].message.content)
```

### Output

```json
{
  "winner": "Los Angeles Dodgers",
  "event": "World Series",
  "year": 2020
}
```

# [C#](#tab/csharp)

Add the following packages to your project:

```dotnetcli
dotnet add package OpenAI
dotnet add package Azure.Identity
```

```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Chat;
using System.ClientModel;
using System.Text.Json;

ChatClient client = new(
    model: "YOUR-MODEL_DEPLOYMENT_NAME",
    credential: new ApiKeyCredential(
        Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")),
    options: new OpenAIClientOptions()
    {
        Endpoint = new Uri(
            "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/")
    }
);

ChatCompletionOptions options = new()
{
    ResponseFormat = ChatResponseFormat.CreateJsonObjectFormat()
};

ChatCompletion completion = client.CompleteChat(
    [
        new SystemChatMessage(
            "You are a helpful assistant designed to output JSON."),
        new UserChatMessage("Who won the world series in 2020?")
    ],
    options);

Console.WriteLine(completion.Content[0].Text);
```

### Output

```json
{
  "winner": "Los Angeles Dodgers",
  "event": "World Series",
  "year": 2020
}
```

# [PowerShell](#tab/powershell)

In this example, the user asks for historical information in a specific JSON schema
because they plan to use the output for further scripting.

```powershell-interactive
$openai = @{
   api_key     = $Env:AZURE_OPENAI_API_KEY
   api_base    = 'https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/'
   name        = 'YOUR-DEPLOYMENT-NAME-HERE' # name you chose for your deployment
}

$headers = @{
  'api-key' = $openai.api_key
}

$messages  = @()
$messages += @{
  role     = 'system'
  content  = 'You are a helpful assistant designed to output JSON.'
}
$messages += @{
  role     = 'user'
  content  = 'Who threw the final pitch during the world series each year from 1979 to 1989?'
}
$messages += @{
  role     = 'user'
  content  = 'Respond using schema. response:{year, team, player, player_height}.'
}

$body      = @{
  response_format = @{type = 'json_object'}
  messages = $messages
} | ConvertTo-Json

$url = "$($openai.api_base)/chat/completions"

$response = Invoke-RestMethod -Uri $url -Headers $headers -Body $body -Method Post -ContentType 'application/json'
$response.choices[0].message.content
```

### Output

The JSON output capability makes it easy for PowerShell to convert the response into a .NET object.
Pass the data through a `|` pipe to run more scripting steps such as sorting.

```powershell
if ($response.choices[0].finish_reason -eq 'stop') {
  $response.choices[0].message.content | ConvertFrom-Json | ForEach-Object response | Sort player_height -Descending
} else { write-warning 'the JSON response was incomplete'}

year team                  player           player_height
---- ----                  ------           -------------
1979 Pittsburgh Pirates    Kent Tekulve     6' 4"
1984 Detroit Tigers        Willie Hernandez 6' 3"
1988 Los Angeles Dodgers   Orel Hershiser   6' 3"
1982 St. Louis Cardinals   Bruce Sutter     6' 2"
1985 Kansas City Royals    Dan Quisenberry  6' 2"
1986 New York Mets         Jesse Orosco     6' 2"
1989 Oakland Athletics     Dennis Eckersley 6' 2"
1981 Los Angeles Dodgers   Steve Howe       6' 1"
1980 Philadelphia Phillies Tug McGraw       6' 0"
1987 Minnesota Twins       Jeff Reardon     6' 0"
1983 Baltimore Orioles     Tippy Martinez   5' 10"
```

---

Two requirements must both be met to use JSON mode successfully:

- Set the response format to `json_object` in your request. In Python, pass `response_format={ "type": "json_object" }`; in .NET, use `ChatResponseFormat.CreateJsonObjectFormat()`; in PowerShell, set `response_format = @{type = 'json_object'}`.
- Include the word "JSON" somewhere in the messages conversation (typically the system message).

Including guidance to the model that it should produce JSON as part of the messages conversation is **required**. We recommend adding this instruction as part of the system message. According to OpenAI, failure to add this instruction can cause the model to *"generate an unending stream of whitespace and the request could run continually until it reaches the token limit."*

Failure to include "JSON" within the messages returns:

### Output

```output
BadRequestError: Error code: 400 - {'error': {'message': "'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.", 'type': 'invalid_request_error', 'param': 'messages', 'code': None}}
```

[!INCLUDE [json-mode 2](../includes/how-to-json-mode-2.md)]
