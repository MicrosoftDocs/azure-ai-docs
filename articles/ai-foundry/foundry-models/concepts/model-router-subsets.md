




# How to

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
