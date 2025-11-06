


# Model router subsets

Combines Routing mode and Model subsets e2e specs including the deployment section from this spec and the newly implemented Control Plane API request example completed 9/19.

Several customers want to personalize their subset of models for routing based on their preferences and enterprise compliance needs. For example, some enterprise customers want to explicitly select only OpenAI (GPT) and Llama and avoid any new models until they explicitly opt in. In other cases, customers have preferences of models based on their benchmarking and preferences.

## features?

Opt-in by design prevents unexpected additions: New models are not used unless explicitly added to a deployment’s inclusion list.
Lifecycle clarity: No need to chase customers for deprecations or implicit changes; deployments have explicit allow lists.
Value minimization risk: Depending on the customers’ inclusions, the Model Router value prop may be reduced.
Per-request scope considerations: Allowing per-request customization still strains routing and introduces complexity; keep as a P1 option.

## UX Flow
User selects "Create Deployment".
User chooses one of the two options:
Default: "Route to all supported models."
Alternative: "Route to selected models."
If Alternative option selected:
User multi-selects the models from the models list
User saves deployment. Selections apply to all requests for this deployment.
New supported models are not included unless explicitly added later.

```json
{
  "sku": {
    "name": "GlobalStandard",
    "capacity": 10
  },
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "ModelRouter",
      "version": "2025-02-26-preview"
    },
    "routing": {
      "mode": "balanced",
      "models": [
        {
          "format": "OpenAI",
          "name": "babbage",
          "version": "1"
        },
        {
          "format": "OpenAI",
          "name": "ada",
          "version": "1"
        }
      ]
    }
  }
}
```

If routing.models is omitted at creation, the portal snapshots all currently supported models into the deployment’s routing list.

New models introduced later are excluded by default until explicitly added.
