---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

The following example shows the response for a chat completion request that has triggered Guardrails & controls. 

# [Python](#tab/python)

```python
from azure.ai.inference.models import AssistantMessage, UserMessage, SystemMessage
from azure.core.exceptions import HttpResponseError

try:
    response = model.complete(
        messages=[
            SystemMessage(content="You are an AI assistant that helps people find information."),
            UserMessage(content="Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."),
        ]
    )

    print(response.choices[0].message.content)

except HttpResponseError as ex:
    if ex.status_code == 400:
        response = json.loads(ex.response._content.decode('utf-8'))
        if isinstance(response, dict) and "error" in response:
            print(f"Your request triggered an {response['error']['code']} error:\n\t {response['error']['message']}")
        else:
            raise ex
    else:
        raise ex
```

# [JavaScript](#tab/javascript)

```javascript
try {
    var messages = [
        { role: "system", content: "You are an AI assistant that helps people find information." },
        { role: "user", content: "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills." },
    ]

    var response = await client.path("/chat/completions").post({
        body: {
            messages: messages,
        }
    });
    
    console.log(response.body.choices[0].message.content)
}
catch (error) {
    if (error.status_code == 400) {
        var response = JSON.parse(error.response._content)
        if (response.error) {
            console.log(`Your request triggered an ${response.error.code} error:\n\t ${response.error.message}`)
        }
        else
        {
            throw error
        }
    }
}
```

# [C#](#tab/csharp)

```csharp
try
{
    requestOptions = new ChatCompletionsOptions()
    {
        Messages = {
            new ChatRequestSystemMessage("You are an AI assistant that helps people find information."),
            new ChatRequestUserMessage(
                "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."
            ),
        },
    };

    response = client.Complete(requestOptions);
    Console.WriteLine(response.Value.Choices[0].Message.Content);
}
catch (RequestFailedException ex)
{
    if (ex.ErrorCode == "content_filter")
    {
        Console.WriteLine($"Your query has trigger Azure Content Safety: {ex.Message}");
    }
    else
    {
        throw;
    }
}
```

# [Java](#tab/java)

```java
try {
    List<ChatRequestMessage> chatMessages = new ArrayList<>();
    chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant"));
    chatMessages.add(new ChatRequestUserMessage("Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."));

    ChatCompletions response = client.complete(new ChatCompletionsOptions(chatMessages));
    System.out.println(response.getChoices().get(0).getMessage().getContent());
} catch (HttpResponseException ex) {
    if (ex.getResponse().getStatusCode() == 400)
        System.out.println("Your query has triggered Azure Content Safety: " + ex.getMessage());
    } else {
        throw ex;
    }
}
```

# [REST](#tab/rest)

__Request__

```HTTP/1.1
POST https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview
api-key: <api-key>
Content-Type: application/json
```

```JSON
{
    "messages": [
    {
        "role": "system",
        "content": "You are a helpful assistant"
    },
    {
        "role": "user",
        "content": "Chopping tomatoes and cutting them into cubes or wedges are great ways to practice your knife skills."
    }
    ],
    "temperature": 0,
    "top_p": 1,
}
```

__Response__

```JSON
{
    "status": 400,
    "code": "content_filter",
    "message": "The response was filtered",
    "param": "messages",
    "type": null
}
```
---
