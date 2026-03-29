---
author: jonburchel
ms.author: jburchel
ms.reviewer: samkemp
ms.topic: include
ms.date: 03/29/2026
---

## Set up the project

[!INCLUDE [JavaScript project setup](../javascript-project-setup.md)]

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

Now create a file called `index.js` and add the following code to read the document:

```javascript
import { readFileSync } from 'fs';

const filePath = process.argv[2] || 'document.txt';
const content = readFileSync(filePath, 'utf-8');

console.log(`Read ${content.length} characters from ${filePath}`);
```

The script accepts an optional file path as a command-line argument and falls back to `document.txt` if none is provided.

## Generate a summary

Initialize the Foundry Local SDK, load a model, and send the document content along with a system prompt that instructs the model to summarize.

Replace the contents of `index.js` with the following code:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';
import { readFileSync } from 'fs';

// Initialize the Foundry Local SDK
const manager = FoundryLocalManager.create({
    appName: 'doc-summarizer',
    logLevel: 'info'
});

// Select and load a model from the catalog
const model = await manager.catalog.getModel('phi-3.5-mini');

await model.download((progress) => {
    process.stdout.write(`\rDownloading model: ${progress.toFixed(2)}%`);
});
console.log('\nModel downloaded.');

await model.load();
console.log('Model loaded and ready.\n');

// Create a chat client
const chatClient = model.createChatClient();

// Read the document
const filePath = process.argv[2] || 'document.txt';
const content = readFileSync(filePath, 'utf-8');

// Summarize the document
const messages = [
    {
        role: 'system',
        content: 'Summarize the following document into concise bullet points. ' +
                 'Focus on the key points and main ideas.'
    },
    { role: 'user', content: content }
];

const response = await chatClient.completeChat(messages);
console.log(response.choices[0]?.message?.content);

// Clean up
await model.unload();
```

The `getModel` method accepts a model alias, which is a short friendly name that maps to a specific model in the catalog. The `download` method fetches the model weights to your local cache (and skips the download if they're already cached), and `load` makes the model ready for inference. The system prompt tells the model to produce bullet-point summaries focused on key ideas.

## Control summary output

Different situations call for different summary styles. You can change the system prompt to control how the model structures its output. Here are three useful variations:

**Bullet points** (default from the previous step):

```javascript
const systemPrompt =
    'Summarize the following document into concise bullet points. ' +
    'Focus on the key points and main ideas.';
```

**One-paragraph summary:**

```javascript
const systemPrompt =
    'Summarize the following document in a single, concise paragraph. ' +
    'Capture the main argument and supporting points.';
```

**Key takeaways:**

```javascript
const systemPrompt =
    'Extract the three most important takeaways from the following document. ' +
    'Number each takeaway and keep each to one or two sentences.';
```

To try a different style, replace the `content` value in the system message with one of the prompts. The model follows the instructions in the system prompt to shape the format and depth of the summary.

## Process multiple documents

Extend the application to summarize every `.txt` file in a directory. This is useful when you have a folder of documents that all need summaries.

The following function iterates over all `.txt` files in a given directory and summarizes each one:

```javascript
import { readdirSync } from 'fs';
import { join, basename } from 'path';

async function summarizeDirectory(chatClient, directory, systemPrompt) {
    const txtFiles = readdirSync(directory)
        .filter(f => f.endsWith('.txt'))
        .sort();

    if (txtFiles.length === 0) {
        console.log(`No .txt files found in ${directory}`);
        return;
    }

    for (const fileName of txtFiles) {
        const fileContent = readFileSync(join(directory, fileName), 'utf-8');
        const msgs = [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: fileContent }
        ];

        console.log(`--- ${fileName} ---`);
        const resp = await chatClient.completeChat(msgs);
        console.log(resp.choices[0]?.message?.content);
        console.log();
    }
}
```

Each file is read, paired with the same system prompt, and sent to the model independently. The model doesn't carry context between files, so each summary is self-contained.

## Complete code

Create a file named `index.js` and add the following complete code:

```javascript
import { FoundryLocalManager } from 'foundry-local-sdk';
import { readFileSync, readdirSync, statSync } from 'fs';
import { join, basename } from 'path';

async function summarizeFile(chatClient, filePath, systemPrompt) {
    const content = readFileSync(filePath, 'utf-8');
    const messages = [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: content }
    ];

    const response = await chatClient.completeChat(messages);
    console.log(response.choices[0]?.message?.content);
}

async function summarizeDirectory(chatClient, directory, systemPrompt) {
    const txtFiles = readdirSync(directory)
        .filter(f => f.endsWith('.txt'))
        .sort();

    if (txtFiles.length === 0) {
        console.log(`No .txt files found in ${directory}`);
        return;
    }

    for (const fileName of txtFiles) {
        console.log(`--- ${fileName} ---`);
        await summarizeFile(chatClient, join(directory, fileName), systemPrompt);
        console.log();
    }
}

// Initialize the Foundry Local SDK
const manager = FoundryLocalManager.create({
    appName: 'doc-summarizer',
    logLevel: 'info'
});

// Select and load a model from the catalog
const model = await manager.catalog.getModel('phi-3.5-mini');

await model.download((progress) => {
    process.stdout.write(`\rDownloading model: ${progress.toFixed(2)}%`);
});
console.log('\nModel downloaded.');

await model.load();
console.log('Model loaded and ready.\n');

// Create a chat client
const chatClient = model.createChatClient();

const systemPrompt =
    'Summarize the following document into concise bullet points. ' +
    'Focus on the key points and main ideas.';

const target = process.argv[2] || 'document.txt';

try {
    const stats = statSync(target);
    if (stats.isDirectory()) {
        await summarizeDirectory(chatClient, target, systemPrompt);
    } else {
        console.log(`--- ${basename(target)} ---`);
        await summarizeFile(chatClient, target, systemPrompt);
    }
} catch {
    console.log(`--- ${basename(target)} ---`);
    await summarizeFile(chatClient, target, systemPrompt);
}

// Clean up
await model.unload();
console.log('\nModel unloaded. Done!');
```

## Run the application

Summarize a single file:

```bash
node index.js document.txt
```

Or summarize every `.txt` file in a directory:

```bash
node index.js ./docs
```

You see output similar to:

```
Downloading model: 100.00%
Model downloaded.
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
