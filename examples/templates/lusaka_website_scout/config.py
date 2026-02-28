from dataclasses import dataclass
from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    model: str = Field(default="gemini/gemini-1.5-flash")
    api_key: str | None = Field(default=None)
    api_base: str | None = Field(default=None)
    max_tokens: int = Field(default=8192)

default_config = AgentConfig()

@dataclass
class AgentMetadata:
    name: str = "Lusaka Website Scout"
    version: str = "0.1.0"
    description: str = "Finds and audits poorly designed business websites in Lusaka, Zambia."
    intro_message: str = (
        "Zikomo! I'm your Lusaka Website Scout. I'll search for local businesses, "
        "audit their websites, and find leads for your design services. "
        "What category of business should I scout first?"
    )

metadata = AgentMetadata()
