Instructions for Foundry Dev-Focused Chat Mode

# Accelerate time to first success
*    Front-load the code so that developers can begin reading/using it as soon as possible. 
*    Remember that the prerequisite section must be the first h2
*    If possible, start with a basic "hello world" sample to fail or succeed early
*    Save information on edge configurations, troubleshooting, deep dives, etc. for the end of the article or move to concept or reference article
*    Show only the most important code for the concept; link to GitHub for complete examples
*    Show complete imports: Always include all import/using statements at the top of code snippets
*    Clearly describe what each example does and expected results
*    For each code snippet, add a section under it with links to the referenced classes, methods, schemas, etc. Search Microsoft Docs for the relevant links. Use the "Reference: [<class/method/schema name>](url)" format.
*    List any special RBAC requirements that might need to be setup by a subscription owner (such as reader roles) in the prereqs

# Code Best Practices
*    If possible, the article should pull code snippets from a full example that lives in GitHub and is maintained by Engineering.
*    Always show import/using statements at the top of a snippet.
*    After each snippet, list links to referenced classes, methods, schemas, etc.
*    Enforce an 80-character line wrap to eliminate horizontal scrolling for code imported into docs as a snippet.
*    Avoid monolithic scripts and encapsulate logic into clearly named functions and classes.
*    Specify programming language: Use correct devlang tags (JSON, .NET, Python) for all code snippets
*    Show complete context: Include all necessary setup code and dependencies.
*    Always include prerequisites: Add bullet lists with dependencies and assumptions for each code section
*    Clearly explain the input and output of an example; in some cases, the input is "bad" data or the expected output is an error. Call these out so the user understands what the example does and the output to expect. Also to reduce change requests to "fix" bad data.

# Pattern and schema compliance

Ensure that the article complies with the relevant patterns, as listed below. Instructions for the pattern are contained in comments in the referenced file.

## How to articles
For articles with the `ms.topic: how-to` tag, ensure the article follows the How-To Article Pattern. See `.github/patterns/How-to-template.md` for details. 

## Quickstarts
For articles with the `ms.topic: quickstart` tag, ensure the article follows the Quickstart Article Pattern. See `.github/patterns/Quickstart-template.md` for details.

## Tutorials
For articles with the `ms.topic: tutorial` tag, ensure the article follows the Tutorial Article Pattern. See `.github/patterns/Tutorial-template.md` for details.



