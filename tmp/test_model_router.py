import time
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create the Foundry project client
project = AIProjectClient(
    endpoint="https://model-router-ga-project-resource.services.ai.azure.com/api/projects/model-router-ga-project",
    credential=DefaultAzureCredential(),
)

deployments = ["model-router"]
prompt = "Explain retrieval-augmented generation in one sentence."

print(f"{'Deployment':<22} {'Responded':<22} {'Latency':>8}  Response")
print("-" * 100)

for name in deployments:
    start = time.time()
    with project.get_openai_client() as client:
        response = client.responses.create(model=name, input=prompt)
    elapsed = time.time() - start

    responded_model = response.model
    print(
        f"{name:<22} {responded_model:<22} {elapsed:>7.2f}s  "
        f"{response.output_text[:60]}"
    )
