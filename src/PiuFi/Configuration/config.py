# === Basic Python Packages ===
import yaml
from pathlib import Path

class ModelConfig:
    def __init__(
            self,
            yaml_path: Path = Path("registry/models.yaml")
    ):
        with open(yaml_path, "r") as f:
            self.config = yaml.safe_load(f)

    def get_model(
            self,
            alias
    ):
        """
        Get full model details by alias
        """
        return self.config["llm_models"][alias]

    def get_agent_model(
            self,
            agent_name: str
    ) -> str:
        """
        Get the model assigned to a specific agent.
        """
        alias = self.config["agent_model_mapping"].get(agent_name)
        return self.get_model(alias) if alias else None