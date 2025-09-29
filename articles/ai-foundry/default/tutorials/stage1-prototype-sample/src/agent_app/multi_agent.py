"""Conceptual multi-agent creation (connected agents).
[TO VERIFY] Adjust to actual connected-agents API surface.
"""
from .config import settings

try:
    from azure.identity import DefaultAzureCredential  # type: ignore
    from azure.ai.projects import AIProjectClient  # [TO VERIFY]
except Exception:  # pragma: no cover
    DefaultAzureCredential = object  # type: ignore
    AIProjectClient = object  # type: ignore

PRIMARY_INSTRUCTIONS = (
    "Primary coordinator. Delegate factual enrichment to 'research-agent' when queries require external or broad context."
)
RESEARCH_INSTRUCTIONS = (
    "Research agent. Provide concise factual expansions from grounded sources, citing titles."
)

def create_connected_agents():  # [TO VERIFY linking property]
    cred = DefaultAzureCredential()
    client = AIProjectClient(endpoint=settings.project_endpoint, credential=cred)
    research = client.agents.create(  # [TO VERIFY]
        model=settings.model_deployment,
        instructions=RESEARCH_INSTRUCTIONS,
        name="research-agent",
        tools=[],
    )
    primary = client.agents.create(  # [TO VERIFY]
        model=settings.model_deployment,
        instructions=PRIMARY_INSTRUCTIONS,
        name="primary-agent",
        tools=[],
        connected_agents=[research.id]  # [TO VERIFY] property name
    )
    return primary, research


def main():  # pragma: no cover
    settings.validate()
    try:
        primary, research = create_connected_agents()
        print("Primary agent:", getattr(primary, 'id', '[id?]'))
        print("Research agent:", getattr(research, 'id', '[id?]'))
    except Exception as e:  # noqa: BLE001
        print("[INFO] Multi-agent placeholder execution failed (expected pre-verification):", e)

if __name__ == "__main__":
    main()
