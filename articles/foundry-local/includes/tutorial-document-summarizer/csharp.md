---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

## Install packages


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd cs/tutorial-document-summarizer
```

[!INCLUDE [C# project setup](../csharp-project-setup.md)]

## Read a text document

Before you summarize anything, you need a sample document to work with. Create a file called `document.txt` in your project directory and add the following content:

```text
Automated testing is a practice in software development where tests are written and executed
by specialized tools rather than performed manually. There are several categories of automated
tests, including unit tests, integration tests, and end-to-end tests. Unit tests verify that
individual functions or methods behave correctly in isolation. Integration tests check that
multiple components work together as expected. End-to-end tests simulate real user workflows
across the entire application.

Adopting automated testing brings measurable benefits to a development team. It catches
regressions early, before they reach production. It reduces the time spent on repetitive
manual verification after each code change. It serves as living documentation of expected
behavior, which helps new team members understand the codebase. Continuous integration
pipelines rely on automated tests to gate deployments and maintain release quality.

Effective test suites follow a few guiding principles. Tests should be deterministic, meaning
they produce the same result every time they run. Tests should be independent, so that one
failing test does not cascade into false failures elsewhere. Tests should run fast, because
slow tests discourage developers from running them frequently. Finally, tests should be
maintained alongside production code so they stay accurate as the application evolves.
```

Now open `Program.cs` and add the following code to read the document:

:::code language="csharp" source="~/foundry-local-main/samples/cs/tutorial-document-summarizer/Program.cs" id="file_reading":::

The code accepts an optional file path as a command-line argument and falls back to `document.txt` if none is provided.

## Generate a summary

Initialize the Foundry Local SDK, load a model, and send the document content along with a system prompt that instructs the model to summarize.

Replace the contents of `Program.cs` with the following code:

:::code language="csharp" source="~/foundry-local-main/samples/cs/tutorial-document-summarizer/Program.cs" id="summarization":::

The `GetModelAsync` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `DownloadAsync` method fetches the model weights to your local cache (and skips the download if they're already cached), and `LoadAsync` makes the model ready for inference. The system prompt tells the model to produce bullet-point summaries focused on key ideas.

## Control summary output

Different situations call for different summary styles. You can change the system prompt to control how the model structures its output. Here are three useful variations:

**Bullet points** (default from the previous step):

```csharp
var systemPrompt =
    "Summarize the following document into concise bullet points. " +
    "Focus on the key points and main ideas.";
```

**One-paragraph summary:**

```csharp
var systemPrompt =
    "Summarize the following document in a single, concise paragraph. " +
    "Capture the main argument and supporting points.";
```

**Key takeaways:**

```csharp
var systemPrompt =
    "Extract the three most important takeaways from the following document. " +
    "Number each takeaway and keep each to one or two sentences.";
```

To try a different style, replace the `Content` value in the system message with one of the prompts. The model follows the instructions in the system prompt to shape the format and depth of the summary.

## Process multiple documents

Extend the application to summarize every `.txt` file in a directory. This is useful when you have a folder of documents that all need summaries.

The following method iterates over all `.txt` files in a given directory and summarizes each one:

```csharp
async Task SummarizeDirectoryAsync(
    dynamic chatClient,
    string directory,
    string systemPrompt,
    CancellationToken ct)
{
    var txtFiles = Directory.GetFiles(directory, "*.txt")
        .OrderBy(f => f)
        .ToArray();

    if (txtFiles.Length == 0)
    {
        Console.WriteLine($"No .txt files found in {directory}");
        return;
    }

    foreach (var txtFile in txtFiles)
    {
        var fileContent = await File.ReadAllTextAsync(txtFile, ct);
        var msgs = new List<ChatMessage>
        {
            new ChatMessage { Role = "system", Content = systemPrompt },
            new ChatMessage { Role = "user", Content = fileContent }
        };

        Console.WriteLine($"--- {Path.GetFileName(txtFile)} ---");
        var resp = await chatClient.CompleteChatAsync(msgs, ct);
        Console.WriteLine(resp.Choices[0].Message.Content);
        Console.WriteLine();
    }
}
```

Each file is read, paired with the same system prompt, and sent to the model independently. The model doesn't carry context between files, so each summary is self-contained.

## Complete code

Replace the contents of `Program.cs` with the following complete code:

:::code language="csharp" source="~/foundry-local-main/samples/cs/tutorial-document-summarizer/Program.cs" id="complete_code":::

## Run the application

Summarize a single file:

```bash
dotnet run -- document.txt
```

Or summarize every `.txt` file in a directory:

```bash
dotnet run -- ./docs
```

You see output similar to:

```
Downloading model: 100.00%
Model loaded and ready.

--- document.txt ---
- Automated testing uses specialized tools to execute tests instead of manual verification.
- Tests fall into three main categories: unit tests (individual functions), integration tests
  (component interactions), and end-to-end tests (full user workflows).
- Key benefits include catching regressions early, reducing manual effort, serving as living
  documentation, and gating deployments through continuous integration pipelines.
- Effective test suites should be deterministic, independent, fast, and maintained alongside
  production code.

Model unloaded. Done!
```
