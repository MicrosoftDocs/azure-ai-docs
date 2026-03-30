---
title: Include file
description: Include file
author: mrbullwinkle
ms.reviewer: sgilley
ms.author: mbullwin
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Other considerations

You should check `finish_reason` for the value `length` before parsing the response. The model might generate partial JSON. This means that output from the model was larger than the available max_tokens that were set as part of the request, or the conversation itself exceeded the token limit.

JSON mode produces JSON that is valid and parses without error. However, there's no guarantee for
output to match a specific schema, even if requested in the prompt.

## Troubleshooting

- If `finish_reason` is `length`, increase `max_tokens` (or reduce prompt length) and retry. Don't parse partial JSON.
- If you need schema guarantees, switch to [Structured Outputs](../how-to/structured-outputs.md).
