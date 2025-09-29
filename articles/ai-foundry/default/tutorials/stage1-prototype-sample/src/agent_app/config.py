import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    project_endpoint: str = os.environ.get("PROJECT_ENDPOINT", "")
    model_deployment: str = os.environ.get("MODEL_DEPLOYMENT_NAME", "")
    sharepoint_resource: str = os.environ.get("SHAREPOINT_RESOURCE_NAME", "")
    mcp_endpoint: str = os.environ.get("MCP_ENDPOINT", "")

    def validate(self):
        missing = [k for k, v in self.__dict__.items() if not v]
        if missing:
            raise ValueError(f"Missing required env settings: {missing}")

settings = Settings()
