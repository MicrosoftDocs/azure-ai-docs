---
title: "Return generated images from hosted agents in Microsoft Foundry"
description: "Return Code Interpreter PNG files from Python hosted agents in Microsoft Foundry with Responses annotations, authenticated downloads, and Teams image display."
author: comacgin
ms.author: comacgin
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 10/08/2026
ms.custom: dev-focus
ai-usage: ai-assisted
#CustomerIntent: As an agent developer, I want my hosted agent to return generated images so that users can view and download them securely.
---

# Return generated images from hosted agents in Microsoft Foundry

Use this guide when a Python hosted agent generates a PNG with Code Interpreter
but users receive only a file name, a sandbox link, or text instead of an image.
Configure the agent to return generated-file references through the Responses
protocol, and verify that the client retrieves the image with authentication.

This guide covers Microsoft Agent Framework agents that use Microsoft Foundry
Toolbox Code Interpreter, custom Responses clients, and Microsoft Teams through
Foundry's Activity Protocol translation. It doesn't cover processing uploaded
photos, image-generation models, other frameworks, or Microsoft 365 Copilot
image rendering.

## Prerequisites

- A Python hosted agent that uses the Responses protocol. Start with the
  [Agent Framework toolbox sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/04-foundry-toolbox).
  Use the Python version and dependencies required by the sample.
- A Foundry project with a deployed model and a toolbox that includes Code
  Interpreter. Follow [Use Code Interpreter](tools/code-interpreter.md) and
  [Use a toolbox with a hosted agent](tools/use-toolbox-hosted-agent.md).
- An authenticated development identity with permission to invoke the agent
  and retrieve container files in that project. Review
  [Foundry role-based access control](../../concepts/rbac-foundry.md).
  Permission to call the agent doesn't make generated files public.
- For the Python download example, `azure-ai-projects`, `azure-identity`, and
  `openai` installed in your client environment, and `FOUNDRY_PROJECT_ENDPOINT`
  set to your project's HTTPS endpoint.
- For Teams verification, an agent already published and accessible to the
  intended user. Complete [Publish agents to Teams](publish-copilot.md)
  separately.

## Check Python hosting package versions

Check your lockfile and deployed environment, not just the sample's dependency
range. Older package sets can return toolbox file metadata without preserving
it as assistant annotations.

The [October 8, 2026 Agent Framework release notes](https://github.com/microsoft/agent-framework/blob/main/python/CHANGELOG.md#1210---2026-10-08)
list a fix to preserve Foundry Toolbox container-file citations. The published
[`agent-framework-foundry-hosting` version `1.0.0b261008`](https://pypi.org/project/agent-framework-foundry-hosting/1.0.0b261008/)
requires `agent-framework-core>=1.20.0,<2`.
Review the release's migration changes before updating an older application.

Use the maintained toolbox sample and validate the response after a package
update. The release-note guidance doesn't replace end-to-end verification
with your deployed package set and client.
Don't assume that a hosting package adds image or download Markdown, or
annotates every occurrence of a file name.

> [!NOTE]
> The `1.0.0b261008` guidance is based on published package metadata and release
> notes, not independent inspection of the package archive or runtime validation
> of that version. Verify your deployed response and client behavior before
> relying on an upgrade as the complete fix.

## Configure the agent to generate an image

Generating a file and delivering it to a user are separate operations. The
toolbox, hosted agent, and client each have a responsibility:

| Component | Responsibility |
| --- | --- |
| Toolbox Code Interpreter | Create the file and return its actual container ID, file ID, and file name. |
| Hosted agent | Preserve that metadata and expose the referenced file in the assistant's `output_text.annotations`. |
| Client or channel | Retrieve file bytes with an authorized identity, then display the image or provide a download action. |

1. Connect `FoundryToolbox` to your agent and serve it with
   `ResponsesHostServer`, as shown in
   [Use a toolbox with a hosted agent](tools/use-toolbox-hosted-agent.md).
   Keep the sample's authentication and per-request toolbox context handling.
1. Add instructions that ask Code Interpreter to save the requested PNG and
   identify it in the final answer. For example:

   ```text
   Use Code Interpreter for chart requests. Save the requested chart as
   /mnt/data/chart.png. Report the saved path in the tool output, and mention
   chart.png in your final answer. Don't claim the file is available if code
   execution or file creation fails.
   ```

1. Send a small test request, such as:

   ```text
   Create a blue bar chart with values Q1=125, Q2=158, Q3=143, and Q4=192.
   Save it as /mnt/data/chart.png and return the generated image.
   ```

Printing the saved path can help identify the output, but it isn't a guarantee
that the tool returns file metadata. Inspect the actual tool result before
changing client rendering or publishing settings.

## Check the generated-file metadata

Compare the tool result with the assistant message. They aren't interchangeable.

1. Find the Code Interpreter tool call and its corresponding result. When the
   Responses transcript contains `function_call` and `function_call_output`
   items, correlate them by `call_id`.
1. Inspect the generated-file metadata, including MCP metadata preserved by
   the framework. A decoded Code Interpreter result can contain this shape:

   ```json
   {
     "container_id": "cntr_example",
     "container_file_citations": [
       {
         "container_id": "cntr_example",
         "file_id": "cfile_example",
         "filename": "chart.png"
       }
     ]
   }
   ```

   These IDs are placeholders. Use the IDs returned by your tool invocation.
   This fragment describes file metadata, not an assistant annotation.

   Reference: [Toolbox MCP results](tools/toolbox.md).

1. Confirm that the referenced file matches `chart.png` uniquely. Code
   Interpreter can return other outputs, including automatically saved plots.
   Don't select the first file, invent an ID, or search unrelated tool output
   for a convenient file name.
1. If the result contains only `container_id`, check code execution and file
   creation. Don't assume that a file reference exists merely because a
   sandbox path appears in text.

Metadata inside `function_call_output.output` doesn't automatically become
`output_text.annotations`. Preserve the complete MCP result when adapting tool
output, rather than retaining only its display text.

## Check the assistant's file annotations

Clients need a standard file reference on the assistant message. A Markdown
link such as `[chart.png](sandbox:/mnt/data/chart.png)` isn't an externally
downloadable address.

1. Inspect the response's `output` array. Find an item with `type: "message"`
   and `role: "assistant"`, then inspect each `output_text` content part.
1. Confirm that its `annotations` array contains a `container_file_citation`
   with the real container ID, file ID, and file name.
1. Confirm that `start_index` and `end_index` identify the referenced span in
   that content part's final text.

The following assistant-message fragment shows the required annotation fields.
It isn't a complete response, and its IDs are placeholders:

```json
{
  "id": "msg_example",
  "type": "message",
  "role": "assistant",
  "status": "completed",
  "content": [
    {
      "type": "output_text",
      "text": "Generated chart.png.",
      "annotations": [
        {
          "type": "container_file_citation",
          "container_id": "cntr_example",
          "file_id": "cfile_example",
          "filename": "chart.png",
          "start_index": 10,
          "end_index": 19
        }
      ],
      "logprobs": []
    }
  ]
}
```

Reference: [Responses output schema](https://developers.openai.com/api/reference/resources/responses/methods/create).

For a custom Responses producer, emit annotations through its supported
response-building API. Keep streamed text, annotation events, completed content
parts, completed message items, and the final response consistent.
Check `response.output_text.annotation.added`, `response.content_part.done`,
`response.output_item.done`, and `response.completed` when you inspect SSE.
An annotation added only to a final JSON object doesn't fix earlier streamed
content with missing annotations or different text offsets.

Reference: [Hosted agent runtime contract](../concepts/hosted-agent-contract.md#responses-protocol).

If tool metadata exists but assistant annotations are absent, diagnose the
framework-to-host conversion. Changing the prompt or appending another
Markdown link isn't a substitute for preserving structured file references.
Don't patch installed SDK files or assume that an undocumented hosting
override is a supported integration point.

## Download the image from a custom client

Retrieve the bytes from the same Foundry project that generated the file.
Use the container ID and file ID from the assistant annotation:

```http
GET {project_endpoint}/openai/v1/containers/{container_id}/files/{file_id}/content
Authorization: Bearer <access-token>
```

Reference: [Download a generated chart](tools/code-interpreter.md#download-the-generated-chart).

The project endpoint has the form
`https://<account>.services.ai.azure.com/api/projects/<project>`.
Use a Microsoft Entra token for the `https://ai.azure.com` audience, or the
`https://ai.azure.com/.default` SDK scope. Don't substitute a resource-level
Azure OpenAI endpoint or its authentication configuration.

A successful authenticated Responses request doesn't make a later browser
image or hyperlink request authenticated. Don't put bearer tokens in response
text, image URLs, query strings, or logs, and don't make files public to work
around a failed download.

### Download with Python

Save the complete JSON response as `response.json` in your client directory.
The following example selects the named PNG from assistant annotations,
deduplicates references to the same file, and retrieves it through an
authenticated project client:

```python
import json
import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

response = json.loads(Path("response.json").read_text(encoding="utf-8"))
filename = "chart.png"
files = set()

for item in response["output"]:
    if item.get("type") != "message" or item.get("role") != "assistant":
        continue
    for part in item.get("content", []):
        if part.get("type") != "output_text":
            continue
        for annotation in part.get("annotations", []):
            if (
                annotation.get("type") == "container_file_citation"
                and annotation.get("filename") == filename
            ):
                files.add((annotation["container_id"], annotation["file_id"]))

if len(files) != 1:
    raise ValueError("Expected one uniquely identified chart.png annotation.")

container_id, file_id = files.pop()
with DefaultAzureCredential() as credential:
    with AIProjectClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        credential=credential,
    ) as project:
        with project.get_openai_client() as client:
            content = client.containers.files.content.retrieve(
                container_id=container_id, file_id=file_id
            )
            image_bytes = content.read()

if not image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
    raise ValueError("The downloaded content doesn't have a PNG signature.")

with Path(filename).open("xb") as destination:
    destination.write(image_bytes)

print(f"Saved {filename}")
```

Reference: [AIProjectClient.get_openai_client](/python/api/azure-ai-projects/azure.ai.projects.aiprojectclient#get-openai-client),
[DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential),
and [Code Interpreter file downloads](tools/code-interpreter.md).

The expected result is a local `chart.png` that opens as an image. The example
fails explicitly if the annotation is missing or ambiguous, the downloaded
bytes lack a PNG signature, or the destination file already exists.

### Display in a browser client

After an authorized download, your application can create a browser
[object URL](https://developer.mozilla.org/docs/Web/API/URL/createObjectURL_static)
from the image bytes in a `Blob`. Reuse that local URL for image display and a
download action, then revoke it when the image is no longer needed.
An object URL isn't an Azure Blob Storage URL and doesn't make the file public.

If browser network or cross-origin restrictions prevent a direct API call,
retrieve the file through your application's authorized backend. Enforce each
user's access instead of sharing one user's generated-file bytes with others.

## Verify image delivery in Teams

For a published Responses-based hosted agent, Foundry's Activity Protocol
translation handles the Teams channel. You don't need to replace your
Responses container with a native Activity Protocol implementation.

1. Confirm that the published stable endpoint selects the agent version you
   tested. Updating the active version doesn't require republishing unchanged
   Teams app metadata.
1. In Teams, start a conversation with that agent and request the test PNG.
   Complete any required sign-in.
1. Check that the reply contains a native image attachment, not just a
   `sandbox:` link or file name.
1. Open the image in the Teams image viewer and select **Download**.
   Confirm that the saved file opens as the requested PNG.

In the current Teams integration, standard container-file annotations can
produce an authenticated file retrieval and a native image attachment.
This path is different from opening a raw container-content API hyperlink.
Verify it in Teams; successful API retrieval alone doesn't prove channel
rendering.

Numbered file references in the reply aren't separate download buttons.
A custom producer that annotates two text spans for the same PNG can produce
two numbered references but one image attachment. Don't depend on that
reference count or promise a clickable file-download footnote. Use the native
image viewer's **Download** action and test the client you're targeting.

This behavior is specific to the current Teams integration. It doesn't
establish equivalent image support in Microsoft 365 Copilot.

For private-network projects, verify the channel route and generated-file
retrieval separately. These image-delivery checks don't establish
private-network end-to-end support. Follow the networking requirements in
[Publish agents by using the REST API](publish-copilot-virtual-network.md).

## Troubleshooting

Check the failing boundary before changing publishing, permissions, or code.

| Symptom | What to check | Resolution |
| --- | --- | --- |
| The tool returns only a container ID. | Code execution and generated-file metadata. | Confirm that the script saves the PNG and identifies the saved path. Inspect the result again; don't fabricate a citation. |
| Tool metadata includes the PNG, but the assistant has no annotations. | Framework and hosting package versions, and preservation of MCP metadata. | Inspect the framework-to-Responses conversion. Use a version with file-citation support and recheck the wire response. A prompt change or plain link alone doesn't fix this boundary. |
| The wrong image appears. | File-name matching and all returned file IDs. | Require a unique match to the requested file. Don't choose an automatic plot or the first returned file. |
| A sandbox link doesn't open. | Whether the assistant has a standard file annotation. | Retrieve the actual container file through an authenticated client or the Teams attachment path. A sandbox path isn't a public URL. |
| A raw API link returns `401`. | The file request's authorization header and token audience. | Authenticate the file request separately for the Foundry project. Don't embed a token in the link. |
| File retrieval returns `403`. | The download identity's access to the project and file. | Check the caller's permissions and identity. Agent invocation authorization and file access are separate checks. |
| File retrieval fails with the correct identity. | Project endpoint, container ID, file ID, and container availability. | Use IDs from the current response and the project that owns the file. If the sandbox is no longer available, generate a fresh output. |
| Nonstreaming works, but streaming loses file references. | Annotation events and completed content, item, and response payloads. | Preserve the same text and annotations throughout the SSE stream and final response. |
| API download works, but Teams shows text only. | Assistant annotations on the served version and Teams attachment delivery. | Verify the active version, inspect the channel failure, and repeat the Teams image-viewer check. Don't assume publishing again fixes a missing annotation. |
| A file footnote isn't clickable. | Whether the reply contains a native image attachment. | Open the attachment and use **Download**. A file reference isn't a raw API download control. |

## Related content

- [Use a toolbox with a hosted agent](tools/use-toolbox-hosted-agent.md) for
  connection and authentication setup.
- [Use Code Interpreter](tools/code-interpreter.md) for tool configuration,
  supported file types, and generated-chart downloads.
- [Publish agents to Microsoft Copilot and Teams](publish-copilot.md) for
  channel setup and active-version selection.
