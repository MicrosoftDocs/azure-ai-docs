---
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 1/21/2025
ms.author: fasantia
author: santiagxf
---

# [Python](#tab/python)

```python
response = client.chat.completions.create(
    model="deepseek-v3-0324", # Replace with your model deployment name.
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain Riemann's conjecture in 1 paragraph"}
    ]
)

print(response.model_dump_json(indent=2)
```

# [JavaScript](#tab/javascript)

```javascript
var messages = [
    { role: "system", content: "You are a helpful assistant" },
    { role: "user", content: "Explain Riemann's conjecture in 1 paragraph" },
];

const response = await client.chat.completions.create({ messages, model: "deepseek-v3-0324" });

console.log(response.choices[0].message.content)
```

# [C#](#tab/csharp)

```csharp
ChatCompletion response = chatClient.CompleteChat(
    [
        new SystemChatMessage("You are a helpful assistant."),
        new UserChatMessage("Explain Riemann's conjecture in 1 paragraph"),
    ]);

Console.WriteLine($"{response.Role}: {response.Content[0].Text}");
```

# [Java](#tab/java)

```java
List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant"));
chatMessages.add(new ChatRequestUserMessage("Explain Riemann's conjecture in 1 paragraph"));

ChatCompletions chatCompletions = client.getChatCompletions("deepseek-v3-0324",
    new ChatCompletionsOptions(chatMessages));

System.out.printf("Model ID=%s is created at %s.%n", chatCompletions.getId(), chatCompletions.getCreatedAt());
for (ChatChoice choice : chatCompletions.getChoices()) {
    ChatResponseMessage message = choice.getMessage();
    System.out.printf("Index: %d, Chat Role: %s.%n", choice.getIndex(), message.getRole());
    System.out.println("Message:");
    System.out.println(message.getContent());
}
```

Here, `deepseek-v3-0324` is the name of a model deployment in the Microsoft Foundry resource.

# [REST](#tab/rest)

__Request__

```HTTP/1.1
POST https://<resource>.services.ai.azure.com/openai/deployments/deepseek-v3-0324/chat/completions?api-version=2024-10-21
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
            "content": "Explain Riemann's conjecture in 1 paragraph"
        }
    ]
}
```

Here, `deepseek-v3-0324` is the name of a model deployment in the Foundry resource.

---
