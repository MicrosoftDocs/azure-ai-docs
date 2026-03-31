---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

## Set up the project


## Samples repository

[!INCLUDE [samples-repo](../samples-repo.md)]

Navigate to the sample for this article:

```bash
cd python/tutorial-document-summarizer
```

[!INCLUDE [Python project setup](../python-project-setup.md)]

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

Now create a file called `main.py` and add the following code to read the document:

:::code language="python" source="~/foundry-local-main/samples/python/tutorial-document-summarizer/src/app.py" id="file_reading":::

The script accepts an optional file path as a command-line argument and falls back to `document.txt` if none is provided. The `Path.read_text` method reads the entire file into a string.

## Generate a summary

Initialize the Foundry Local SDK, load a model, and send the document content along with a system prompt that instructs the model to summarize.

Replace the contents of `main.py` with the following code:

:::code language="python" source="~/foundry-local-main/samples/python/tutorial-document-summarizer/src/app.py" id="summarization":::

The `get_model` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `download` method fetches the model weights to your local cache (and skips the download if they're already cached), and `load` makes the model ready for inference. The system prompt tells the model to produce bullet-point summaries focused on key ideas.

## Control summary output

Different situations call for different summary styles. You can change the system prompt to control how the model structures its output. Here are three useful variations:

**Bullet points** (default from the previous step):

```python
system_prompt = (
    "Summarize the following document into concise bullet points. "
    "Focus on the key points and main ideas."
)
```

**One-paragraph summary:**

```python
system_prompt = (
    "Summarize the following document in a single, concise paragraph. "
    "Capture the main argument and supporting points."
)
```

**Key takeaways:**

```python
system_prompt = (
    "Extract the three most important takeaways from the following document. "
    "Number each takeaway and keep each to one or two sentences."
)
```

To try a different style, replace the `"content"` value in the system message with one of the prompts. The model follows the instructions in the system prompt to shape the format and depth of the summary.

## Process multiple documents

Extend the application to summarize every `.txt` file in a directory. This is useful when you have a folder of documents that all need summaries.

The following function iterates over all `.txt` files in a given directory and summarizes each one:

```python
async def summarize_directory(client, directory):
    txt_files = sorted(Path(directory).glob("*.txt"))

    if not txt_files:
        print(f"No .txt files found in {directory}")
        return

    for txt_file in txt_files:
        content = txt_file.read_text(encoding="utf-8")
        messages = [
            {
                "role": "system",
                "content": "Summarize the following document into concise bullet points. "
                           "Focus on the key points and main ideas."
            },
            {"role": "user", "content": content}
        ]

        print(f"--- {txt_file.name} ---")
        response = client.complete_chat(messages)
        print(response.choices[0].message.content)
        print()
```

Each file is read, paired with the same system prompt, and sent to the model independently. The model doesn't carry context between files, so each summary is self-contained.

## Complete code

Create a file named `main.py` and add the following complete code:

:::code language="python" source="~/foundry-local-main/samples/python/tutorial-document-summarizer/src/app.py" id="complete_code":::

## Run the application

Summarize a single file:

```bash
python main.py document.txt
```

Or summarize every `.txt` file in a directory:

```bash
python main.py ./docs
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
