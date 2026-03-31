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
cd rust/tutorial-document-summarizer
```

[!INCLUDE [Rust project setup](../rust-project-setup.md)]

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

Now open `src/main.rs` and add the following code to read the document:

:::code language="rust" source="~/foundry-local-main/samples/rust/tutorial-document-summarizer/src/main.rs" id="file_reading":::

The code accepts an optional file path as a command-line argument and falls back to `document.txt` if none is provided.

## Generate a summary

Initialize the Foundry Local SDK, load a model, and send the document content along with a system prompt that instructs the model to summarize.

Replace the contents of `src/main.rs` with the following code:

:::code language="rust" source="~/foundry-local-main/samples/rust/tutorial-document-summarizer/src/main.rs" id="summarization":::

The `get_model` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `download` method fetches the model weights to your local cache (and skips the download if they're already cached), and `load` makes the model ready for inference. The system prompt tells the model to produce bullet-point summaries focused on key ideas.

## Control summary output

Different situations call for different summary styles. You can change the system prompt to control how the model structures its output. Here are three useful variations:

**Bullet points** (default from the previous step):

```rust
let system_prompt =
    "Summarize the following document into concise bullet points. \
     Focus on the key points and main ideas.";
```

**One-paragraph summary:**

```rust
let system_prompt =
    "Summarize the following document in a single, concise paragraph. \
     Capture the main argument and supporting points.";
```

**Key takeaways:**

```rust
let system_prompt =
    "Extract the three most important takeaways from the following document. \
     Number each takeaway and keep each to one or two sentences.";
```

To try a different style, replace the system message content with one of the prompts. The model follows the instructions in the system prompt to shape the format and depth of the summary.

## Process multiple documents

Extend the application to summarize every `.txt` file in a directory. This is useful when you have a folder of documents that all need summaries.

The following function iterates over all `.txt` files in a given directory and summarizes each one:

```rust
use std::path::Path;

async fn summarize_directory(
    client: &foundry_local_sdk::ChatClient,
    directory: &Path,
    system_prompt: &str,
) -> anyhow::Result<()> {
    let mut txt_files: Vec<_> = fs::read_dir(directory)?
        .filter_map(|entry| entry.ok())
        .filter(|entry| {
            entry.path().extension()
                .map(|ext| ext == "txt")
                .unwrap_or(false)
        })
        .collect();

    txt_files.sort_by_key(|e| e.path());

    if txt_files.is_empty() {
        println!("No .txt files found in {}", directory.display());
        return Ok(());
    }

    for entry in &txt_files {
        let file_content = fs::read_to_string(entry.path())?;
        let messages: Vec<ChatCompletionRequestMessage> = vec![
            ChatCompletionRequestSystemMessage::new(system_prompt).into(),
            ChatCompletionRequestUserMessage::new(&file_content).into(),
        ];

        let file_name = entry.file_name();
        println!("--- {} ---", file_name.to_string_lossy());
        let resp = client.complete_chat(&messages, None).await?;
        let text = resp.choices[0]
            .message
            .content
            .as_deref()
            .unwrap_or("");
        println!("{}\n", text);
    }

    Ok(())
}
```

Each file is read, paired with the same system prompt, and sent to the model independently. The model doesn't carry context between files, so each summary is self-contained.

## Complete code

Replace the contents of `src/main.rs` with the following complete code:

:::code language="rust" source="~/foundry-local-main/samples/rust/tutorial-document-summarizer/src/main.rs" id="complete_code":::

Summarize a single file:

```bash
cargo run -- document.txt
```

Or summarize every `.txt` file in a directory:

```bash
cargo run -- ./docs
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
