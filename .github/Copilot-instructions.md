When writing documentation, follow these guidelines:

## General style tips

* Get to the point fast. Be concise and clear.
* Talk like a person.
* Simpler is better.
* Be brief. Give customers enough information to make decisions confidently. Prune excess words.
* Break up long sentences.
* Follow the style of the [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/welcome/). If there's a conflict between the following guidelines and the Microsoft Writing Style Guide, ask how to resolve it.

## Grammar

* Use present tense verbs (is, open) instead of past tense (was, opened). For example, "The method returns a value" instead of "The method returns a value."
* Write factual statements and direct commands. Avoid hypotheticals.
* Use active voice where the subject performs the action.
* Write in second person (you) to speak directly to readers.
* Use gender-neutral language.
* Avoid multiple -ing words that could create ambiguity.
* Keep prepositional phrases simple and clear.
* Place modifiers close to what they modify.
* Use a conversational tone with contractions.
* Don't use "we" or "our" to refer to the authors of the documentation.
* Use the imperative mood for instructions. For example, "Call the method" instead of "You should call the method."
* Use "might" instead of "may" to indicate possibility. For example, "This method might throw an exception" instead of "This method may throw an exception."
* Use the Oxford comma in lists of three or more items.

## Capitalization

* Use sentence-style capitalization for everything except proper nouns.
* Always capitalize proper nouns.
* Don’t capitalize the spelled-out form of an acronym unless it's a proper noun.
* Use title-style capitalization for product and service names.
* Don't use all uppercase for emphasis.

## Numbers

* Spell out numbers for zero through nine, unless space is limited. Use numerals for 10 and above.
* Spell out numbers at the beginning of a sentence.
* Spell out ordinal numbers such as first, second, and third. Don't add -ly to form adverbs from ordinal numbers.
* Number ordered list items all as "1." instead of "1.", "2.", etc. Use bullets for unordered lists.

## Punctuation

* Use short, simple sentences.
* End all sentences with a period.
* Use one space after punctuation marks.
* After a colon, capitalize only proper nouns.
* Avoid semicolons - use separate sentences instead.
* Use question marks sparingly.
* Don't use slashes (/) - use "or" instead.

## Text formatting

* UI elements, like menu items, dialog names, and names of text boxes, should be in **bold** text.
* Use `code style` for:
    * Code elements, like method names, property names, and language keywords.
    * SQL commands.
    * NuGet package names.
    * Command-line commands.
    * Database table and column names.
    * Resource names (like virtual machine names) that shouldn't be localized.
    * URLs that you don't want to be selectable.
    * File names and folders, custom types, and other text that should never be localized.
* For code placeholders, if you want users to replace part of an input string with their own values, use angle brackets (less than < and greater than > characters) on that placeholder text.

## Headings

* Headings should be in sentence case, not title case. Don't use gerunds in titles.
* Don't apply an inline style like italic, or bold to headings. But do use inline code style for headings that are code elements, like method names or property names.

## Alerts

* Alerts are a Markdown extension to create block quotes that render with colors and icons that indicate the significance of the content. The following alert types are supported:

    * `[!NOTE]` Information the user should notice even if skimming.
    * `[!TIP]` Optional information to help a user be more successful.
    * `[!IMPORTANT]` Essential information required for user success.
    * `[!CAUTION]` Negative potential consequences of an action.
    * `[!WARNING]` Dangerous certain consequences of an action.

## Adding links

* Add links to related articles and resources where appropriate
* Links to other documentation articles should be relative, not absolute. Start relative links with `/docs/` and include the `.md` suffix
* **For Azure AI documentation specifically**:
  * Link to pricing pages for services with usage-based billing under [Azure Pricing](https://azure.microsoft.com/pricing/)
  * Cross-reference related AI services when applicable
  * Include links to SDK reference documentation
  * Link to Azure AI Foundry portal pages when relevant: `[Azure AI Foundry portal](https://ai.azure.com)`

## Adding new files

* If you add a new Markdown file, it should be named in all lowercase with hyphens separating words. Also, omit any filler words such as "the" or "a" from the file name.

## Images

* Use images only when they add value.
* Images have a descriptive and meaningful alt text that starts with "Screenshot showing" and ends with ".".
* Videos have a descriptive and meaningful alt text or title that starts with "Video showing" and ends with ".".

## Numbered steps

* Write complete sentences with capitalization and periods
* Use imperative verbs
* Clearly indicate where actions take place (UI location)
* For single steps, use a bullet instead of a number
* When allowed, use angle brackets for menu sequences (File > Open)

## Terminology

* Use "Select" instead of "Click" for UI elements like buttons, menu items, links, dropdowns, and checkboxes.

### Azure AI terminology

* **Service names**: Use the full service names consistently on first mention in a specific document. Short names or abbreviations can be used on subsequent mentions within the same document. Use the following full service names:
  * Azure AI Foundry (not "AI Foundry" or "Foundry")
  * Azure AI Document Intelligence (not "Form Recognizer" for current versions)
  * Azure AI Content Safety (not just "Content Safety")
  * Azure AI Language Service (not "Language Understanding")
  * Azure AI Content Understanding
  * Azure OpenAI Service (when referring to the Azure-hosted service)

* **Product references**: When referencing Azure AI services in general, use "Azure AI services" (lowercase "services")

* **Model names**: Use proper capitalization and formatting:
  * GPT-4o, GPT-3.5-turbo (use hyphens, maintain case)
  * Use `code style` for model deployment names and API versions

* **API and SDK references**: 
  * Use "REST API" (not "Rest API" or "rest api")
  * Use proper version formatting: "v4.0 (2024-11-30)" for API versions
  * Use `code style` for SDK package names, method names, and parameters

  ## AI and machine learning content

* **Model and training terminology**:
  * Use "model" (not "AI model" unless distinguishing from other types)
  * Use "training data" and "inference" consistently
  * Use "deployment" for hosted model endpoints
  * Use "prompt" for input text to generative models

* **Accuracy and limitations**:
  * Always include appropriate disclaimers about AI model limitations
  * Use `[!IMPORTANT]` alerts for accuracy-related information
  * Mention confidence scores when relevant to the service

* **Pricing and billing**:
  * Be specific about billing units (tokens, pages, transactions, etc.)
  * Link to current pricing pages for specific cost information
  * Use `[!NOTE]` for pricing-related information that might change

  ## Prerequisites and setup sections

* **Standard prerequisite order**:
  1. Azure subscription and resource requirements
  2. SDK/library installations
  3. Authentication setup (keys, endpoints)
  4. Development environment setup

* **Use consistent section headings**:
  * "Prerequisites" (not "Pre-requisites" or "Requirements")
  * "Set up your programming environment" 
  * "Create your application" or "Build your application"
  * "Next steps"

* **Authentication information**:
  * Always use placeholders in angle brackets: `<your-resource-name>`
  * Include both key-based and Entra ID authentication when available
  * Link to authentication overview docs