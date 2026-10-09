---
title: "Deploy and use Microsoft-Decision-1 in Microsoft Foundry"
description: "Deploy Microsoft-Decision-1 in Microsoft Foundry and use typed questions to classify, score, and route text or JSON."
ms.service: microsoft-foundry
ms.subservice: foundry-models
ms.topic: how-to
ms.date: 10/07/2026
author: siddharthsi
ms.author: siddharthsi
ai-usage: ai-assisted

#CustomerIntent: As a developer, I want to use Microsoft-Decision-1 in Microsoft Foundry so I can add fast, structured decisions to my application.
---

# Deploy and use Microsoft-Decision-1 in Microsoft Foundry

`Microsoft-Decision-1` is available in Microsoft Foundry for classification,
routing, ranking, grading, and binary decisions. Use it to triage support
tickets, prioritize incidents, filter content, evaluate model output, or
select a model, tool, or agent for a request.

Unlike a generative large language model (LLM), `Microsoft-Decision-1` doesn't
generate a free-form response or written rationale. It makes a focused
judgment about text or JSON and returns a typed, numerical decision. This
approach is useful when your application needs a predictable response shape
and probabilities that it can threshold or rank.

In this article, you deploy `Microsoft-Decision-1` in Microsoft Foundry, call
the decision API, and build a support-ticket classifier.

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an
  Azure subscription, create a
  [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- Access to Microsoft Foundry.
- A [Microsoft Foundry project](../../how-to/create-projects.md).
- Permission to create and manage model deployments. The **Cognitive Services
  Contributor** role lets you deploy models. For more information, see
  [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).
- An authentication method: Microsoft Entra ID (recommended) or an API key.
- Python 3.10 or later to run the quickstart.
- The Azure Identity library:

  ```bash
  pip install azure-identity
  ```

## Choose a question type

`Microsoft-Decision-1` accepts a `state` value and one or more typed questions.
The state can be text or JSON. Choose the question type based on the decision
your application needs. The request pattern is similar to a system-one API:
your application supplies the state and bounded questions, and the model
returns decisions instead of generated prose.

| Question | Type | Result |
| --- | --- | --- |
| Is this true? | `noul` | A probability from 0 through 1. |
| Which option is it? | `choice` | One selected option and the probability for each option. |
| How much? | `score` | A value on an ordered scale and the probability for each level. |

The response `answers` object uses the question names from your request. The
response also includes the deployed model name and token usage.

### Use Noul for gates and filters

Use a `noul` question for a yes-or-no condition, such as whether a tool call
touches production data, a document contains a prompt injection, or a support
reply promises a refund.

```json
{
  "state": "I refunded your $200. You don't need to contact billing.",
  "questions": {
    "promises_refund": {
      "type": "noul",
      "instructions": "Does this reply promise the customer a refund?",
      "criteria": {
        "true": "Commits to returning money",
        "false": "Makes no commitment about money"
      }
    }
  }
}
```

The `criteria` field is optional. Define the true and false conditions to make
borderline questions more precise. Choose a probability threshold based on
your workload, and validate it against labeled examples before you automate a
gate.

### Use Choice for classification and routing

Use a `choice` question to select exactly one label from a fixed set. Common
uses include routing tickets, classifying intent or document type, selecting a
model or tool, and sorting alerts by cause.

```json
{
  "state": "The API returns 500 on every call.",
  "questions": {
    "team": {
      "type": "choice",
      "instructions": "Which team should handle this ticket?",
      "criteria": {
        "billing": "Charges, invoices, and refunds",
        "engineering": "Bugs, errors, and outages",
        "support": "How-to and account questions"
      }
    }
  }
}
```

Describe each option clearly. The response contains the selected option and a
probability for every option. Use a low top probability as a signal to
escalate the decision to a person or another model.

### Use Score for ranking and grading

Use a `score` question to place an item on an ordered scale. Common uses
include prioritizing a queue, grading model output, and measuring qualities
such as severity, helpfulness, or frustration.

```json
{
  "state": "Checkout is down for all EU customers since 09:00.",
  "questions": {
    "severity": {
      "type": "score",
      "instructions": "How severe is this incident?",
      "criteria": [
        "Cosmetic",
        "Minor",
        "Major",
        "Critical"
      ]
    }
  }
}
```

List the levels from lowest to highest. The returned score is the
probability-weighted average of the level indexes. For example, a four-level
scale runs from `0` through `3`, and the result can fall between levels.
Validate scores on your own labeled examples. Prefer scores for relative
ordering and thresholds rather than as absolute, calibrated ratings.

## Microsoft-Decision-1 at a glance

| Model name | Model version | Deployment type | API type |
| --- | --- | --- | --- |
| `Microsoft-Decision-1` | 1 | `DataZoneStandard` in selected regions; `GlobalStandard` | Decision |

To minimize network latency between your application and Foundry, create the
Foundry resource in a region close to your application and users, and call
that resource's endpoint. For locality-sensitive workloads, use
`DataZoneStandard` in the data zone closest to your application when it's
available. This deployment type keeps inference processing within that data
zone and can reduce long-distance routing. Benchmark your workload because a
deployment type doesn't guarantee lower latency.

`GlobalStandard` is also supported and provides access to global capacity.
Because inference can be processed in any supported Azure region, latency
might be higher or more variable. For more information, see
[Deployment types for Microsoft Foundry Models](../concepts/deployment-types.md)
and [region availability for Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure-region-availability.md).

## Deploy Microsoft-Decision-1

Deploy the model from the Foundry model catalog.

1. Open the [Foundry portal](https://ai.azure.com), and go to your project.
1. Select **Model catalog**.
1. Search for and select **Microsoft-Decision-1**.
1. Select **Deploy**, configure the deployment, and then select **Deploy**.
1. On the deployment details page, copy the resource endpoint, deployment
   name, and API key.

For more information about the portal workflow, see
[Deploy Microsoft Foundry Models](deploy-foundry-models.md).

Alternatively, deploy the model by using the Azure CLI. Replace
`<ACCOUNT_NAME>`, `<RESOURCE_GROUP>`, and `<DEPLOYMENT_NAME>` with your values.

```azurecli
az cognitiveservices account deployment create \
  --name <ACCOUNT_NAME> \
  --resource-group <RESOURCE_GROUP> \
  --deployment-name <DEPLOYMENT_NAME> \
  --model-name "Microsoft-Decision-1" \
  --model-format Microsoft \
  --model-version "1" \
  --sku-name GlobalStandard \
  --sku-capacity 1
```

**Reference:** [az cognitiveservices account deployment create](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-create)

The example uses `GlobalStandard`. To keep inference processing within the
data zone closest to your application, change `--sku-name` to
`DataZoneStandard` when that deployment type is available in your region.

To list all available deployments on your resource:

```azurecli
az cognitiveservices account deployment list \
  --resource-group <RESOURCE_GROUP> \
  --name <ACCOUNT_NAME> \
  --output table
```

**Reference:** [az cognitiveservices account deployment list](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-list)

## Call the decision API

Send requests to the Microsoft provider's decision endpoint on your Foundry
resource:

```text
<your-foundry-resource-endpoint>/providers/microsoft/v1/systemone
```

The request's `model` value is your deployment name, not the underlying model
name. For example, a deployment named `pi-decision-1` uses
`"model": "pi-decision-1"`. The response's `model` field identifies the
underlying model, so it can contain a different value, such as
`microsoft-decision-1`.

Set the values that you copied from the deployment details page:

```bash
export AZURE_ENDPOINT="<your-foundry-resource-endpoint>"
export DEPLOYMENT_NAME="<your-deployment-name>"
```

For Microsoft Entra ID authentication, sign in with the Azure CLI, and get an
access token:

```bash
az login
export AZURE_ENTRA_TOKEN=$(az account get-access-token \
  --resource https://cognitiveservices.azure.com \
  --query accessToken \
  --output tsv)
```

**Reference:** [az account get-access-token](/cli/azure/account#az-account-get-access-token)

Call the endpoint with Microsoft Entra ID:

```bash
curl "$AZURE_ENDPOINT/providers/microsoft/v1/systemone" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_ENTRA_TOKEN" \
  -d '{
    "model": "'"$DEPLOYMENT_NAME"'",
    "state": "The API returns 500 on every call.",
    "questions": {
      "team": {
        "type": "choice",
        "instructions": "Which team should handle this ticket?",
        "criteria": {
          "billing": "Charges, invoices, and refunds",
          "engineering": "Bugs, errors, and outages",
          "support": "How-to and account questions"
        }
      }
    }
  }'
```

To use an API key instead, replace the `Authorization` header with:

```bash
export AZURE_API_KEY="<your-api-key>"
-H "api-key: $AZURE_API_KEY"
```

For more information about authentication, see
[Configure Microsoft Entra ID authentication](configure-entra-id.md).

## Classify support tickets

This quickstart uses a `choice` question to route customer support requests to
the billing, technical, or account team. It also measures accuracy and median
request latency across a small set of labeled examples.

1. Create a file named `support_ticket_classifier.py`.
1. Add the following code:

    ```python
    import json
    import os
    import urllib.error
    import urllib.request
    from collections.abc import Mapping
    from statistics import median
    from time import perf_counter
    from typing import Any

    from azure.identity import DefaultAzureCredential


    OPTIONS = {
        "billing": "Charges, invoices, refunds, or subscription payments",
        "technical": "Software errors, bugs, or integration failures",
        "account": "Sign-in, password, or account-access problems",
    }

    EXAMPLES = [
        ("I was charged twice.", "billing"),
        ("The integration crashes during checkout.", "technical"),
        ("I cannot sign in after resetting my password.", "account"),
    ]

    AZURE_ENDPOINT = os.environ["AZURE_ENDPOINT"].rstrip("/")
    DEPLOYMENT_NAME = os.environ["DEPLOYMENT_NAME"]
    TIMEOUT_SECONDS = 60
    TOKEN_SCOPE = "https://cognitiveservices.azure.com/.default"
    CREDENTIAL = DefaultAzureCredential()


    class DecisionAPIError(RuntimeError):
        """Raised when the API can't return a valid classification."""


    def read_choice(
        payload: Any,
        options: Mapping[str, str],
    ) -> str:
        if not isinstance(payload, dict):
            raise DecisionAPIError("The API returned an invalid response.")

        answers = payload.get("answers")
        if not isinstance(answers, dict):
            raise DecisionAPIError("The API returned no answers object.")

        answer = answers.get("team")
        if not isinstance(answer, dict) or answer.get("type") != "choice":
            raise DecisionAPIError("The API returned an invalid answer.")

        choice = answer.get("choice")
        if not isinstance(choice, str) or choice not in options:
            raise DecisionAPIError(
                f"The API selected an unsupported team: {choice!r}."
            )
        return choice


    def predict(
        text: str,
        options: Mapping[str, str],
    ) -> str:
        if not text.strip():
            raise ValueError("text must not be empty.")
        if len(options) < 2:
            raise ValueError("options must contain at least two choices.")

        body = json.dumps(
            {
                "model": DEPLOYMENT_NAME,
                "state": text,
                "questions": {
                    "team": {
                        "type": "choice",
                        "instructions": (
                            "Which team should handle this customer support "
                            "request? Select exactly one team based on the "
                            "primary problem."
                        ),
                        "criteria": dict(options),
                    }
                },
            }
        ).encode("utf-8")
        access_token = CREDENTIAL.get_token(TOKEN_SCOPE).token

        request = urllib.request.Request(
            f"{AZURE_ENDPOINT}/providers/microsoft/v1/systemone",
            data=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=TIMEOUT_SECONDS,
            ) as response:
                response_body = response.read()
        except urllib.error.HTTPError as exc:
            raise DecisionAPIError(
                f"The API returned HTTP {exc.code}."
            ) from exc
        except urllib.error.URLError as exc:
            raise DecisionAPIError(
                f"Couldn't reach the API: {exc.reason}."
            ) from exc

        try:
            payload = json.loads(response_body)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise DecisionAPIError(
                "The API returned invalid JSON."
            ) from exc
        return read_choice(payload, options)


    def main() -> None:
        correct = 0
        latencies_ms = []

        for text, expected in EXAMPLES:
            start = perf_counter()
            predicted = predict(text, OPTIONS)
            elapsed_ms = (perf_counter() - start) * 1000

            correct += int(predicted == expected)
            latencies_ms.append(elapsed_ms)
            print(
                f"Expected={expected}, predicted={predicted}, "
                f"latency={elapsed_ms:.1f} ms"
            )

        accuracy = correct / len(EXAMPLES)
        print(f"Accuracy: {accuracy:.1%}")
        print(
            "Median request latency: "
            f"{median(latencies_ms):.1f} ms"
        )


    if __name__ == "__main__":
        main()
    ```

1. Set the environment variables from
   [Call the decision API](#call-the-decision-api).
1. Run the sample:

    ```bash
    python support_ticket_classifier.py
    ```

The script prints the expected and predicted team for each request. It then
prints accuracy and median latency for the sample set. Replace `EXAMPLES` with
representative, labeled examples from your workload before you use the
measurements to make deployment decisions.

## Combine decisions in one request

Questions that use the same state can share one request. For example, route a
ticket with `choice`, rate its severity with `score`, and check whether it's a
repeat contact with `noul`.

```json
{
  "model": "<deployment-name>",
  "state": {
    "message": "Checkout is down again. This is my third request.",
    "customer_contact_count": 3
  },
  "questions": {
    "team": {
      "type": "choice",
      "instructions": "Which team should handle this request?",
      "criteria": {
        "billing": "Charges, invoices, and refunds",
        "engineering": "Bugs, errors, and outages",
        "support": "How-to and account questions"
      }
    },
    "severity": {
      "type": "score",
      "instructions": "How severe is this issue?",
      "criteria": ["Cosmetic", "Minor", "Major", "Critical"]
    },
    "repeat_contact": {
      "type": "noul",
      "instructions": "Has the customer contacted support before?"
    }
  }
}
```

Combining related questions reduces the number of requests and keeps the
decision context consistent.

## Interpret decisions

`Microsoft-Decision-1` returns numerical decisions without a written rationale.
Use the probabilities to decide whether your application acts automatically,
requests another evaluation, or sends the item to a person.

## When to use Microsoft-Decision-1

Use `Microsoft-Decision-1` when your application needs one or more bounded,
typed decisions about the same input. It works well for high-volume workflows
where your application needs to act on a probability, selected option, or
ordered score instead of displaying generated text.

Common use cases include:

- **Gates and filters**: Check whether content meets a condition before a
  workflow continues.
- **Classification and routing**: Send tickets, alerts, documents, or requests
  to one option from a known set.
- **Ranking and prioritization**: Order incidents, leads, search results, or
  review queues by an application-defined scale.
- **Evaluation and grading**: Score model output against an ordered rubric.
- **Model, tool, or agent selection**: Choose the component that should handle
  a request.

Use a generative LLM instead when the application needs to create, summarize,
rewrite, or explain content. You can also combine the two approaches. Use
`Microsoft-Decision-1` to route or gate a request, and then send approved
requests to a generative model.

## Known limitations and risks

- **Fairness**: The model might reflect biases from its base model and training data. Don't use its scores as the sole basis for decisions about individuals.
- **Wording sensitivity**: Scores can change based on how you phrase or order questions and options. Poorly framed questions still return scores.
- **Reliability**: Calibration is strongest on familiar task types. The model doesn't provide explanations and might rely on outdated knowledge.
- **Harmful content**: When you use the model as a safety filter, it might miss subtle harmful content or flag benign content.

## Best practices

Before you use `Microsoft-Decision-1` in an application, evaluate the model
for your intended scenario.

- Validate the model on data that's representative of your use case.
- Tune the `state`, `instructions`, and options for each primitive. You can
  improve task definition with structured or code-enriched state and
  parameterized options. Use coding agents to generate candidate
  configurations, evaluate them against labeled examples, and compare
  results. Review agent-generated changes before you use them in production.
- Set confidence thresholds based on the cost of false positives and false
  negatives. Include an abstention option, such as `cannot tell`, when the
  model shouldn't make a forced choice.
- Use clear, neutral wording for questions and options. Consider randomizing
  option order, and test whether changing the order affects results.
- For consequential decisions about people, such as decisions involving
  credit, employment, housing, healthcare, or legal matters, use the model for
  decision support with meaningful human review. Don't use it as the sole
  decision-maker.
- Avoid sensitive attributes that aren't necessary for the use case. Monitor
  outcomes for errors and unfair disparities.
- Tell affected users when AI contributes to a decision.

## Troubleshoot

| Error | Possible cause | Resolution |
| --- | --- | --- |
| 400 Bad Request | The request uses an invalid question type or shape. | Check `state`, `questions`, `type`, and `criteria`. |
| 401 Unauthorized | The credential is missing, invalid, or expired. | Refresh the token, or verify the API key and authentication header. |
| 403 Forbidden | The identity doesn't have access to the deployment. | Verify the role assignment and deployment access. |
| 404 Not Found | The resource endpoint or API path is incorrect. | Verify the endpoint on the deployment details page. |
| 422 Unprocessable Entity | The deployment name or question definition isn't supported. | Verify the `model` value and each question definition. |
| 429 Too Many Requests | The deployment rate limit was exceeded. | Retry with exponential backoff, or request more quota. |

## Related content

- [Deploy Microsoft Foundry Models](deploy-foundry-models.md)
- [Configure Microsoft Entra ID authentication](configure-entra-id.md)
- [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md)
