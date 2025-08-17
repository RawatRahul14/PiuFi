# === Python Modules ===
import yaml
import json
from pathlib import Path
from typing import Dict

# === Function to retrieve the Prompts ===
def load_prompt(
        name: str,
        path: Path = Path("registry/prompts.yaml")
):
    # === Calling the whole prompt ===
    data = yaml.safe_load(path.read_text(encoding = "utf-8"))

    # === Returning a specific prompt ===
    return data["Prompts"][name]

# === Rendering the Prompt ===
def render_prompt(
        prompt_name: str,
        path: Path = Path("registry/prompts.yaml"),
        **kwargs
):
    # === Loading the full prompt ===
    prompt_def = load_prompt(
        name = prompt_name,
        path = path
    )

    # === Prepare the user prompt by replacing variables ===
    template = prompt_def["template"]

    # === Collect only the variables prompt needs ===
    var_values = {k: v for k, v in kwargs.items()}

    # === Filing the Variables ===
    filled_prompt = template.format(**var_values)

    return {
        "system": prompt_def["system"],
        "user": filled_prompt,
        "output_schema": prompt_def["output_schema"],
        "few_shots": prompt_def.get("few_shots", [])
    }