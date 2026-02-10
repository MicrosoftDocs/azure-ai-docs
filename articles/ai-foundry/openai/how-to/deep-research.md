---
title: Deep research with the Responses API
description: Learn how to use Azure OpenAI deep research
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/10/2026
author: mrbullwinkle    
ms.author: mbullwin
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Deep research

The o3-deep-research model is designed for advanced research tasks. It can browse, analyze, and synthesize information from hundreds of sources to produce a comprehensive, citation-rich report. This model uses multi-step reasoning, web search, and remote Model Context Protocol (MCP) servers to gather and process data. It can also run code for complex analysis.

Use deep research when you need:

* Legal or scientific research
* Market and competitive analysis
* Reports based on large sets of internal or public data

To start, call the **Responses API** with the model set to your o3-deep-research deployment name. Include at least one data source: web search or a remote MCP server. Optionally, add the code interpreter tool for advanced analysis.

## Prerequisites

- An Azure OpenAI resource with a deployment of the o3-deep-research model.
- An authentication method:
  - API key, or
  - Microsoft Entra ID.
- At least one data source configured in your request:
  - `web_search_preview` (see [Web search (preview)](web-search.md)), and/or
  - A remote MCP server (see [Research with your own data](#research-with-your-own-data)).

## Start a deep research task

Replace `o3-deep-research` with your model deployment name.

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
        "model": "o3-deep-research",
        "background": true,
        "tools": [
            { "type": "web_search_preview" },
            { "type": "code_interpreter", "container": {"type": "auto"} }
        ],
        "input": "Research the economic impact of semaglutide on global healthcare systems. Include specific figures, trends, statistics, and measurable outcomes. Prioritize reliable, up-to-date sources: peer-reviewed research, health organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical earnings reports. Include inline citations and return all source metadata. Be analytical, avoid generalities, and ensure that each section supports data-backed reasoning that could inform healthcare policy or financial modeling."
      }'
```

```python
import os
from openai import OpenAI

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)

input_text = """
Research the economic impact of semaglutide on global healthcare systems.
Do:
- Include specific figures, trends, statistics, and measurable outcomes.
- Prioritize reliable, up-to-date sources: peer-reviewed research, health
  organizations (e.g., WHO, CDC), regulatory agencies, or pharmaceutical
  earnings reports.
- Include inline citations and return all source metadata.

Be analytical, avoid generalities, and ensure that each section supports
data-backed reasoning that could inform healthcare policy or financial modeling.
"""

response = client.responses.create(
  model="o3-deep-research",  # Replace with your model deployment name.
    input=input_text,
    background=True,
    tools=[
        { "type": "web_search_preview" },
        { "type": "code_interpreter", "container": {"type": "auto"} }
    ],
)

print(response.output_text)
```

> [!NOTE]
> Deep research requests can take time. Run them in `background` mode, then poll the response status until it reaches a terminal state.

## Get the response status and results

Use the `GET` endpoint to retrieve a response by ID. Continue polling while the status is `queued` or `in_progress`.

```bash
curl -X GET https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses/{response_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN"
```

```python
from time import sleep
import os
from openai import OpenAI

client = OpenAI(
  base_url="https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

input_text = "Research the economic impact of semaglutide on global healthcare systems."

response = client.responses.create(
  model="o3-deep-research",  # Replace with your model deployment name.
  input=input_text,
  background=True,
  tools=[
    {"type": "web_search_preview"},
    {"type": "code_interpreter", "container": {"type": "auto"}},
  ],
)

while response.status in {"queued", "in_progress"}:
  sleep(2)
  response = client.responses.retrieve(response.id)

print(response.output_text)
```

## Output structure

Deep research responses follow the standard Responses API format. Pay attention to the output array—it lists all tool calls made during the process, such as:

* **web_search_call**: Actions using the web search tool (for example, search, open_page, find_in_page).
* **code_interpreter_call**: Code execution steps.
* **mcp_tool_call**: Actions performed on remote MCP servers.
* **message**: The model’s final answer with inline citations.

Example `web_search_call` (search action):

```json
{
    "id": "ws_0caf37305fe587b600690a7050f1008196804b303b95135978",
    "action": {
        "query": "positive news story November 4 2025 good news",
        "type": "search",
        "sources": null
    },
    "status": "completed",
    "type": "web_search_call"
}
```

Example `message` (final answer):

```json
{
  "id": "msg_0caf37305fe587b600690a70bbd9948196916fd9037096ba88",
  "content": [
    {
      "annotations": [
        {
          "end_index": 564,
          "start_index": 333,
          "title": "The world of AI",
          "type": "url_citation",
          "url": "https://foo.bar.com"
        }
      ],
      "text": "... answer to the query with inline citations ....",
      "type": "output_text",
      "logprobs": []
    }
  ],
  "role": "assistant",
  "status": "completed",
  "type": "message"
}
```

## Best practices

* Use background mode to avoid timeouts.
* Poll the response status while it's `queued` or `in_progress`.
* Increase timeout settings if not using background mode.
* Use `max_tool_calls` to control tool usage and manage cost/latency.

## Creating optimized prompts

For best results, use this three-step process:

1. **Clarify intent**: Use a smaller model (for example, gpt-4.1 or gpt-5) to gather details from the user.
2. **Rewrite prompt**: Use a smaller model to create a detailed, structured prompt.
3. **Run deep research**: Pass the optimized prompt to o3-deep-research.

These steps are optional but recommended for high-quality outputs.

### Ask clarifying questions

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
        "model": "gpt-4.1",
  "input": "Research surfboards for me. I'm interested in ...",
        "instructions": "You are talking to a user who is asking for a research task to be conducted. Your job is to gather more information from the user to successfully complete the task. GUIDELINES: - Be concise while gathering all necessary information** - Make sure to gather all the information needed to carry out the research task in a concise, well-structured manner. - Use bullet points or numbered lists if appropriate for clarity. - Don't ask for unnecessary information, or information that the user has already provided. IMPORTANT: Do NOT conduct any research yourself, just gather information that will be given to a researcher to conduct the research task."
    }'
```

```python
import os
from openai import OpenAI

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)

instructions = """
You are talking to a user who is asking for a research task to be conducted. Your job is to gather more information from the user to successfully complete the task.

GUIDELINES:
- Be concise while gathering all necessary information**
- Make sure to gather all the information needed to carry out the research task in a concise, well-structured manner.
- Use bullet points or numbered lists if appropriate for clarity.
- Don't ask for unnecessary information, or information that the user has already provided.

IMPORTANT: Do NOT conduct any research yourself, just gather information that will be given to a researcher to conduct the research task.
"""

input_text = "Research surfboards for me. I'm interested in ..."

response = client.responses.create(
    model="gpt-4.1",
    input=input_text,
    instructions=instructions,
)

print(response.output_text)
```

### Optimize the prompt

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses?api-version=preview \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
        "model": "gpt-4.1",
  "input": "Research surfboards for me. I'm interested in ...",
        "instructions": "You will be given a research task by a user. Your job is to produce a set of instructions for a researcher that will complete the task. Do NOT complete the task yourself, just provide instructions on how to complete it.  GUIDELINES: 1. **Maximize Specificity and Detail** - Include all known user preferences and explicitly list key attributes or   dimensions to consider. - It is of utmost importance that all details from the user are included in   the instructions.  2. **Fill in Unstated But Necessary Dimensions as Open-Ended** - If certain attributes are essential for a meaningful output but the user   has not provided them, explicitly state that they are open-ended or default   to no specific constraint.  3. **Avoid Unwarranted Assumptions** - If the user has not provided a particular detail, do not invent one. - Instead, state the lack of specification and guide the researcher to treat   it as flexible or accept all possible options.  4. **Use the First Person** - Phrase the request from the perspective of the user.  5. **Tables** - If you determine that including a table will help illustrate, organize, or   enhance the information in the research output, you must explicitly request   that the researcher provide them.  Examples: - Product Comparison (Consumer): When comparing different smartphone models,   request a table listing each model's features, price, and consumer ratings   side-by-side. - Project Tracking (Work): When outlining project deliverables, create a table   showing tasks, deadlines, responsible team members, and status updates. - Budget Planning (Consumer): When creating a personal or household budget,   request a table detailing income sources, monthly expenses, and savings goals. - Competitor Analysis (Work): When evaluating competitor products, request a   table with key metrics, such as market share, pricing, and main differentiators.  6. **Headers and Formatting** - You should include the expected output format in the prompt. - If the user is asking for content that would be best returned in a   structured format (e.g. a report, plan, etc.), ask the researcher to format   as a report with the appropriate headers and formatting that ensures clarity   and structure.  7. **Language** - If the user input is in a language other than English, tell the researcher   to respond in this language, unless the user query explicitly asks for the   response in a different language.  8. **Sources** - If specific sources should be prioritized, specify them in the prompt. - For product and travel research, prefer linking directly to official or   primary websites (e.g., official brand sites, manufacturer pages, or   reputable e-commerce platforms like Amazon for user reviews) rather than   aggregator sites or SEO-heavy blogs. - For academic or scientific queries, prefer linking directly to the original   paper or official journal publication rather than survey papers or secondary   summaries. - If the query is in a specific language, prioritize sources published in that   language." 
    }'
```

```python
import os
from openai import OpenAI

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)

instructions = """
You will be given a research task by a user. Your job is to produce a set of
instructions for a researcher that will complete the task. Do NOT complete the
task yourself, just provide instructions on how to complete it.

GUIDELINES:
1. **Maximize Specificity and Detail**
- Include all known user preferences and explicitly list key attributes or
  dimensions to consider.
- It is of utmost importance that all details from the user are included in
  the instructions.

2. **Fill in Unstated But Necessary Dimensions as Open-Ended**
- If certain attributes are essential for a meaningful output but the user
  has not provided them, explicitly state that they are open-ended or default
  to no specific constraint.

3. **Avoid Unwarranted Assumptions**
- If the user has not provided a particular detail, do not invent one.
- Instead, state the lack of specification and guide the researcher to treat
  it as flexible or accept all possible options.

4. **Use the First Person**
- Phrase the request from the perspective of the user.

5. **Tables**
- If you determine that including a table will help illustrate, organize, or
  enhance the information in the research output, you must explicitly request
  that the researcher provide them.

Examples:
- Product Comparison (Consumer): When comparing different smartphone models,
  request a table listing each model's features, price, and consumer ratings
  side-by-side.
- Project Tracking (Work): When outlining project deliverables, create a table
  showing tasks, deadlines, responsible team members, and status updates.
- Budget Planning (Consumer): When creating a personal or household budget,
  request a table detailing income sources, monthly expenses, and savings goals.
- Competitor Analysis (Work): When evaluating competitor products, request a
  table with key metrics, such as market share, pricing, and main differentiators.

6. **Headers and Formatting**
- You should include the expected output format in the prompt.
- If the user is asking for content that would be best returned in a
  structured format (e.g. a report, plan, etc.), ask the researcher to format
  as a report with the appropriate headers and formatting that ensures clarity
  and structure.

7. **Language**
- If the user input is in a language other than English, tell the researcher
  to respond in this language, unless the user query explicitly asks for the
  response in a different language.

8. **Sources**
- If specific sources should be prioritized, specify them in the prompt.
- For product and travel research, prefer linking directly to official or
  primary websites (e.g., official brand sites, manufacturer pages, or
  reputable e-commerce platforms like Amazon for user reviews) rather than
  aggregator sites or SEO-heavy blogs.
- For academic or scientific queries, prefer linking directly to the original
  paper or official journal publication rather than survey papers or secondary
  summaries.
- If the query is in a specific language, prioritize sources published in that
  language.
"""

input_text = "Research surfboards for me. I'm interested in ..."

response = client.responses.create(
    model="gpt-4.1",
    input=input_text,
    instructions=instructions,
)

print(response.output_text)
```

## Research with your own data

Deep research can use public and private data. For private data, connect a remote MCP server that supports `search` and `fetch` interfaces.

### Remote MCP servers

Requirements:

* A `search` interface to return results for a query.
* A `fetch` interface to retrieve documents by ID.
* `require_approval` must be set to never.

#### Remote MCP server with deep research

```bash
curl https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_OPENAI_AUTH_TOKEN" \
  -d '{
        "model": "o3-deep-research",
        "background": true,
        "tools": [
            {
              "type": "mcp",
              "server_label": "mycompany_mcp_server",
              "server_url": "https://mycompany.com/mcp",
              "require_approval": "never"
            }
        ],
        "input": "What similarities are in the notes for our closed/lost sales opportunities?"
    }'
```

```python
import os
from openai import OpenAI

client = OpenAI(  
  base_url = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/",
  api_key=os.getenv("AZURE_OPENAI_API_KEY")  
)

response = client.responses.create(
    model="o3-deep-research",
    input="What similarities are in the notes for our closed/lost sales opportunities?",
    background=True,
  tools=[
        {
            "type": "mcp",
            "server_label": "mycompany_mcp_server",
            "server_url": "https://mycompany.com/mcp",
            "require_approval": "never"
        }
    ],
)

print(response.output_text)
```

## Safety risks and mitigations

Enabling web search and MCP servers introduces security risks. Follow these best practices:

* Connect only trusted MCP servers.
* Log and review all tool calls and model outputs.
* Stage workflows: run public research with web access first, then private MCP with no web access.
* Validate tool arguments with schemas or regex.
* Screen links before opening or sharing.

## Troubleshooting

- **Request takes too long or times out**: Set `background` to `true`, then poll the response until completion.
- **No web search or MCP calls appear in the output**: Confirm you include at least one tool in `tools`.
- **MCP calls fail**: Confirm the MCP server is reachable and `require_approval` is set to `never`.

## Next steps

> [!div class="nextstepaction"]
> [Use the Azure OpenAI Responses API](responses.md)

> [!div class="nextstepaction"]
> [Web search (preview)](web-search.md)
